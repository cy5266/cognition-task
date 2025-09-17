

import os, time, json
from urllib.parse import urlencode
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, render_template_string, jsonify, session
import requests

load_dotenv()

# ----- Config -----
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO  = os.getenv("GITHUB_REPO")
DEVIN_API_KEY = os.getenv("DEVIN_API_KEY")
DEVIN_BASE = os.getenv("DEVIN_BASE_URL", "https://api.devin.ai/v1")

assert GITHUB_TOKEN and GITHUB_OWNER and GITHUB_REPO and DEVIN_API_KEY, "Missing .env vars"

GITHUB_API = "https://api.github.com"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "demo-secret-key-for-development")

# In-memory user storage for demo purposes (consistent with SESSION_CACHE pattern)
USERS = {
    "admin": {"password": os.getenv("ADMIN_PASSWORD", "password"), "name": "Admin User"},
    "demo": {"password": os.getenv("DEMO_PASSWORD", "demo"), "name": "Demo User"}
}

# In-memory cache of session results for demo purposes (OK for local / Loom demo)
SESSION_CACHE = {}

# ----- GitHub helpers -----
def gh_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

def list_issues():
    url = f"{GITHUB_API}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues"
    r = requests.get(url, headers=gh_headers(), params={"state": "open", "per_page": 50})
    r.raise_for_status()
    # Drop PRs
    issues = [i for i in r.json() if "pull_request" not in i]
    return [{
        "number": i["number"],
        "title": i["title"],
        "body": i.get("body") or "",
        "html_url": i["html_url"],
        "labels": [l["name"] for l in (i.get("labels") or [])],
    } for i in issues]

def get_issue(number: int):
    url = f"{GITHUB_API}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{number}"
    r = requests.get(url, headers=gh_headers())
    r.raise_for_status()
    i = r.json()
    return {
        "number": i["number"],
        "title": i["title"],
        "body": i.get("body") or "",
        "html_url": i["html_url"],
        "labels": [l["name"] for l in (i.get("labels") or [])],
    }

def find_pr_for_branch(branch: str):
    url = f"{GITHUB_API}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls"
    r = requests.get(url, headers=gh_headers(), params={"state": "open", "head": f"{GITHUB_OWNER}:{branch}"})
    r.raise_for_status()
    prs = r.json()
    return prs[0]["html_url"] if prs else None

# ----- Devin helpers -----
def devin_headers():
    return {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json"
    }

def devin_create_session(prompt, extra=None):
    payload = {"prompt": prompt}
    if extra:
        payload.update(extra)

    r = requests.post(f"{DEVIN_BASE}/sessions", headers=devin_headers(), json=payload)
    if not r.ok:
        raise RuntimeError(f"Devin create session failed: {r.status_code} {r.text}")

    data = r.json()
    print("Devin create session response:", data)  # <-- watch your terminal

    # Try common id field names
    sid = (
        data.get("id")
        or data.get("session_id")
        or data.get("sessionId")
        or (data.get("data", {}) if isinstance(data.get("data"), dict) else {}).get("id")
    )
    if not sid:
        # Surface payload so we can see the real shape
        raise RuntimeError(f"Devin session missing id in response: {data}")

    return {"id": sid, "raw": data}


def devin_get_session(session_id: str):
    r = requests.get(f"{DEVIN_BASE}/sessions/{session_id}", headers=devin_headers())
    if not r.ok:
        raise RuntimeError(f"Devin get session failed: {r.status_code} {r.text}")
    return r.json()

# ----- Authentication helpers -----
def validate_login(username, password):
    """Validate user credentials"""
    user = USERS.get(username)
    return user and user["password"] == password

def login_required(f):
    """Decorator to require login for routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not session.get('username'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ----- Routes -----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        if validate_login(username, password):
            session['logged_in'] = True
            session['username'] = username
            session['user_name'] = USERS[username]["name"]
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password"
            return render_template_string(TPL_LOGIN, error=error)
    
    return render_template_string(TPL_LOGIN, error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/")
@login_required
def home():
    try:
        issues = list_issues()
    except Exception as e:
        issues = []
        error = str(e)
        return f"<h1>Error loading issues</h1><pre>{error}</pre>", 500

    return render_template_string(TPL_INDEX, issues=issues, owner=GITHUB_OWNER, repo=GITHUB_REPO, session=session)

@app.post("/scope/<int:number>")
@login_required
def scope_issue(number: int):
    issue = get_issue(number)
    prompt = f"""
You are scoping GitHub issue #{issue['number']} in {GITHUB_OWNER}/{GITHUB_REPO}.
URL: {issue['html_url']}
Title: {issue['title']}
Body: {issue['body'] or '(no description)'}

Respond ONLY with valid JSON in the following schema:
{{
  "clarifications": [string],
  "plan": [string],
  "effort_hours": number,
  "confidence_score": number,  // float between 0 and 1
  "risks": [string],
  "test_plan": [string]
}}
""".strip()

    session = devin_create_session(prompt=prompt)
    sid = session["id"]  # will raise if missing
    return redirect(url_for("session_status", id=sid, issue=number, type="scope"))


@app.post("/complete/<int:number>")
@login_required
def complete_issue(number: int):
    issue = get_issue(number)
    data = request.get_json(silent=True) or request.form
    action_plan = data.get("action_plan")

    if not action_plan:
        return ("Missing action_plan. Run Scope first, then click "
                "'Complete with this plan' from the session page."), 400

    branch = f"devin/issue-{issue['number']}"
    prompt = f"""
Take the following action plan and COMPLETE GitHub issue #{issue['number']} in {GITHUB_OWNER}/{GITHUB_REPO}.

Ticket:
Title: {issue['title']}
URL: {issue['html_url']}
Body: {issue['body'] or '(no description)'}

Action plan (authoritative; follow these steps explicitly):
{action_plan}

Execution requirements:
- Create branch: {branch}
- Commit changes referencing #{issue['number']}
- Open a PR to default branch with title: "Fix #{issue['number']}: {issue['title']}"
- Run tests and include results
Return JSON: {{"branch": "{branch}", "pr_url": "<link>", "notes": "..." }}
""".strip()

    session = devin_create_session(prompt=prompt)
    sid = session["id"]
    return redirect(url_for("session_status", id=sid, issue=number, type="complete"))


@app.get("/session")
@login_required
def session_status():
    sid = request.args.get("id")
    issue = int(request.args.get("issue", "0"))
    s_type = request.args.get("type", "scope")

    if not sid or sid == "None":
        return "<h2>Error: Missing or invalid session id</h2>", 400

    cached = SESSION_CACHE.get(sid)
    return render_template_string(
        TPL_SESSION,
        sid=sid, issue=issue, s_type=s_type,
        cached=json.dumps(cached or {}, indent=2),
    )

@app.get("/api/devin/status")
@login_required
def api_devin_status():
    sid = request.args.get("id")
    if not sid or sid == "None":
        return jsonify({"error": "missing or invalid session id"}), 400
    try:
        data = devin_get_session(sid)
    except Exception as e:
        return jsonify({"error": str(e)}), 502

    parsed = {}
    try:
        if data.get("structured_output"):
            parsed.update(data["structured_output"])
        else:
            out = data.get("output")
            if isinstance(out, str):
                parsed.update(json.loads(out))
            elif isinstance(out, dict) and isinstance(out.get("text"), str):
                parsed.update(json.loads(out["text"]))
    except Exception as e:
        print("Parse error:", e)

    SESSION_CACHE[sid] = {"raw": data, "parsed": parsed}
    return jsonify({"raw": data, "parsed": parsed})


# ---------- Templates ----------
TPL_INDEX = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Devin × GitHub Issues Dashboard</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; padding: 24px; }
    h1 { margin: 0 0 8px; }
    .card { border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
    .row { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
    .btn { padding: 8px 12px; border-radius: 8px; border: 1px solid #888; background: #fafafa; cursor: pointer; }
    .labels span { display:inline-block; background:#f2f2f2; padding:2px 6px; border-radius:6px; margin-right:6px; font-size:12px;}
    .muted { color: #666; font-size: 12px; }
    form { display:inline; }
  </style>
</head>
<body>
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
    <h1>Issues — {{ owner }}/{{ repo }}</h1>
    <div style="display: flex; align-items: center; gap: 12px;">
      <span class="muted">Welcome, {{ session.user_name }}</span>
      <a href="/logout" class="btn">Logout</a>
    </div>
  </div>
  <p class="muted">Click <strong>Scope</strong> to have Devin produce a plan + confidence score. Click <strong>Complete</strong> to have Devin implement and open a PR.</p>

  {% if issues|length == 0 %}
    <p>No open issues found.</p>
  {% endif %}

  {% for i in issues %}
    <div class="card">
      <div class="row">
        <div>
          <div><strong>#{{ i.number }}</strong> — {{ i.title }}</div>
          <div class="muted"><a href="{{ i.html_url }}" target="_blank">{{ i.html_url }}</a></div>
          {% if i.labels %}
            <div class="labels">
              {% for l in i.labels %}<span>{{ l }}</span>{% endfor %}
            </div>
          {% endif %}
        </div>
        <div>
          <form method="post" action="/scope/{{ i.number }}"><button class="btn" type="submit">Scope</button></form>
          <form method="post" action="/complete/{{ i.number }}"><button class="btn" type="submit">Complete</button></form>
        </div>
      </div>
    </div>
  {% endfor %}
</body>
</html>
"""

TPL_SESSION = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Session {{ sid }}</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; padding: 24px; }
    pre { background:#0b1020; color:#e6edf3; padding:16px; border-radius:12px; overflow:auto; }
    .pill { display:inline-block; background:#eef; padding:4px 8px; border-radius:999px; font-size:12px; }
    .row { display:flex; align-items:center; gap:12px; }
    .btn { padding: 8px 12px; border-radius: 8px; border: 1px solid #888; background: #fafafa; cursor: pointer; }
    .grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
    .card { border:1px solid #ddd; border-radius:12px; padding:12px; }
    .muted { color:#666; font-size:12px; }
  </style>
</head>
<body>
  <div class="row">
    <a class="btn" href="/">← Back to issues</a>
    <div class="pill">Session: {{ sid }}</div>
    <div class="pill">Issue: #{{ issue }}</div>
    <div class="pill">Type: {{ s_type }}</div>
    <button id="refresh" class="btn">Refresh</button>
  </div>

  <div class="grid" style="margin-top:16px;">
    <div class="card">
      <h3>Parsed Output</h3>
      <div id="summary" class="muted">Waiting for Devin…</div>
      <div id="complete_form_mount"></div>
      <pre id="parsed_json">{}</pre>
    </div>
    <div class="card">
      <h3>Raw</h3>
      <pre id="raw">Polling…</pre>
    </div>
  </div>

  <script>
    const sid = "{{ sid }}";
    const rawEl = document.getElementById("raw");
    const parsedEl = document.getElementById("parsed_json");
    const summaryEl = document.getElementById("summary");
    const refreshBtn = document.getElementById("refresh");

    function renderParsed(parsed) {
      // parsed is whatever /api/devin/status extracted (your JSON schema)
      let html = "";
      if (typeof parsed.confidence_score !== "undefined") {
        html += `<p><b>Confidence Score:</b> ${parsed.confidence_score}</p>`;
      }
      if (Array.isArray(parsed.plan) && parsed.plan.length) {
        html += "<b>Plan:</b><ul>" + parsed.plan.map(step => `<li>${step}</li>`).join("") + "</ul>";
      }
      if (!html) html = "<span class='muted'>No structured JSON parsed yet — check Raw.</span>";
      summaryEl.innerHTML = html;
      parsedEl.textContent = JSON.stringify(parsed, null, 2);
      renderCompleteButtonIfPlan(parsed);
    }

    function renderCompleteButtonIfPlan(parsed) {
        const mount = document.getElementById("complete_form_mount");
        mount.innerHTML = ""; // reset
        if (Array.isArray(parsed.plan) && parsed.plan.length) {
            const form = document.createElement("form");
            form.method = "post";
            form.action = `/complete/${encodeURIComponent({{ issue }})}`;

            const ta = document.createElement("textarea");
            ta.name = "action_plan";
            ta.style.display = "none";
            ta.value = JSON.stringify(parsed.plan, null, 2); // send the plan
            form.appendChild(ta);

            const btn = document.createElement("button");
            btn.className = "btn";
            btn.type = "submit";
            btn.textContent = "Complete with this plan";
            form.appendChild(btn);

            mount.appendChild(form);
        }
    }


    async function pollOnce() {
      try {
        const res = await fetch(`/api/devin/status?id=${encodeURIComponent(sid)}`);
        const data = await res.json();
        if (data.error) {
          rawEl.textContent = "Error: " + data.error;
          return {done: true};
        }
        rawEl.textContent = JSON.stringify(data.raw, null, 2);

        // Render parsed (if any)
        if (data.parsed) renderParsed(data.parsed);

        // Stop polling on terminal statuses
        const status = (data.raw && data.raw.status) || "";
        if (["completed","failed","errored"].includes(status)) {
          return {done: true};
        }
        return {done: false};
      } catch (e) {
        rawEl.textContent = "Error: " + e.toString();
        return {done: true};
      }
    }

    async function startPolling() {
      // initial fetch
      let r = await pollOnce();
      if (r.done) return;

      // poll every 3s up to ~3 minutes
      let count = 0;
      const timer = setInterval(async () => {
        count++;
        const res = await pollOnce();
        if (res.done || count > 60) clearInterval(timer);
      }, 3000);
    }

    refreshBtn.onclick = () => { pollOnce(); };
    startPolling();
  </script>
</body>
</html>
"""

TPL_LOGIN = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Login - Devin × GitHub Issues Dashboard</title>
  <style>
    body { 
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; 
      padding: 24px; 
      background: #f8f9fa;
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .login-container {
      background: white;
      border-radius: 12px;
      padding: 32px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      width: 100%;
      max-width: 400px;
    }
    h1 { margin: 0 0 24px; text-align: center; }
    .form-group { margin-bottom: 16px; }
    label { display: block; margin-bottom: 8px; font-weight: 500; }
    input[type="text"], input[type="password"] {
      width: 100%;
      padding: 12px;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 16px;
      box-sizing: border-box;
      -webkit-appearance: none;
    }
    .btn {
      width: 100%;
      padding: 12px;
      background: #007bff;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 16px;
      cursor: pointer;
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
    .btn:hover { background: #0056b3; }
    .btn:active { background: #004085; }
    .error { 
      color: #dc3545; 
      background: #f8d7da; 
      padding: 12px; 
      border-radius: 8px; 
      margin-bottom: 16px; 
    }
    .demo-info {
      margin-top: 24px;
      padding: 16px;
      background: #e7f3ff;
      border-radius: 8px;
      font-size: 14px;
    }
    @media (max-width: 480px) {
      body { padding: 16px; }
      .login-container { padding: 24px; }
    }
  </style>
</head>
<body>
  <div class="login-container">
    <h1>Login</h1>
    {% if error %}
      <div class="error">{{ error }}</div>
    {% endif %}
    <form method="post" action="/login">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required autocomplete="username" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required autocomplete="current-password" />
      </div>
      <button type="submit" class="btn">Login</button>
    </form>
    <div class="demo-info">
      <strong>Demo Credentials:</strong><br>
      Username: admin, Password: password<br>
      Username: demo, Password: demo
    </div>
  </div>
</body>
</html>
"""

if __name__ == "__main__":
    # Run: FLASK_APP=app.py flask run  (or) python app.py
    app.run(host="0.0.0.0", port=5000, debug=True)
