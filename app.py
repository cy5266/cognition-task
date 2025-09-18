# app_streamlit.py
import os
import time
import json
from urllib.parse import urlencode
from dotenv import load_dotenv
import requests
import streamlit as st

load_dotenv()

# ----- Config -----
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO  = os.getenv("GITHUB_REPO")
DEVIN_API_KEY = os.getenv("DEVIN_API_KEY")
DEVIN_BASE = os.getenv("DEVIN_BASE_URL", "https://api.devin.ai/v1")

GITHUB_API = "https://api.github.com"

if "SESSION_CACHE" not in st.session_state:
    st.session_state.SESSION_CACHE = {}

SESSION_CACHE = st.session_state.SESSION_CACHE


def needs_config() -> bool:
    missing = []
    for k, v in {
        "GITHUB_TOKEN": GITHUB_TOKEN,
        "GITHUB_OWNER": GITHUB_OWNER,
        "GITHUB_REPO": GITHUB_REPO,
        "DEVIN_API_KEY": DEVIN_API_KEY,
    }.items():
        if not v:
            missing.append(k)
    if missing:
        st.error(f"Missing required env vars: {', '.join(missing)}")
        return True
    return False


def gh_headers():
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if GITHUB_TOKEN:
        h["Authorization"] = f"token {GITHUB_TOKEN}"
    return h

# List out all of the issues from the attached Github repository
def list_issues():
    url = f"{GITHUB_API}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues"
    r = requests.get(url, headers=gh_headers(), params={"state": "open", "per_page": 50})
    r.raise_for_status()
    issues = [i for i in r.json() if "pull_request" not in i]
    return [{
        "number": i["number"],
        "title": i["title"],
        "body": i.get("body") or "",
        "html_url": i["html_url"],
        "labels": [l["name"] for l in (i.get("labels") or [])],
    } for i in issues]

# Get all of information needed for the issues on Github including taggs, number, url, and more.
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


def devin_headers():
    return {"Authorization": f"Bearer {DEVIN_API_KEY}", "Content-Type": "application/json"}


def devin_create_session(prompt, extra=None):
    payload = {"prompt": prompt}
    if extra:
        payload.update(extra)

    r = requests.post(f"{DEVIN_BASE}/sessions", headers=devin_headers(), json=payload)
    if not r.ok:
        raise RuntimeError(f"Devin create session failed: {r.status_code} {r.text}")

    data = r.json()
    # Try common id field names
    sid = (
        data.get("id")
        or data.get("session_id")
        or data.get("sessionId")
        or (data.get("data", {}) if isinstance(data.get("data"), dict) else {}).get("id")
    )
    if not sid:
        raise RuntimeError(f"Devin session missing id in response: {data}")
    return {"id": sid, "raw": data}


def devin_get_session(session_id: str):
    r = requests.get(f"{DEVIN_BASE}/sessions/{session_id}", headers=devin_headers())
    if not r.ok:
        raise RuntimeError(f"Devin get session failed: {r.status_code} {r.text}")
    return r.json()

def close_issue(number: int, comment: str = None):  
    url = f"{GITHUB_API}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{number}"  
    payload = {"state": "closed"}  
    if comment:  
        # Add a comment before closing  
        comment_url = f"{GITHUB_API}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{number}/comments"  
        requests.post(comment_url, headers=gh_headers(), json={"body": comment})  
      
    r = requests.patch(url, headers=gh_headers(), json=payload)  
    r.raise_for_status()  
    return r.json()


def safe_set_query_params(**kwargs):
    try:
        st.query_params.clear()
        st.query_params.update(kwargs)
    except Exception:
        st.experimental_set_query_params(**kwargs)


def do_rerun():
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()


# ---------- Prompts ----------
def make_scope_prompt(issue):
    return f"""
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
  "risks": [string]
}}
""".strip()


def make_complete_prompt(issue, action_plan_str):
    branch = f"devin/issue-{issue['number']}"
    return f"""
Take the following action plan and COMPLETE GitHub issue #{issue['number']} in {GITHUB_OWNER}/{GITHUB_REPO}.

Ticket:
Title: {issue['title']}
URL: {issue['html_url']}
Body: {issue['body'] or '(no description)'}

Action plan (authoritative; follow these steps explicitly):
{action_plan_str}

Execution requirements:
- Create branch: {branch}
- Commit changes referencing #{issue['number']}
- Open a PR to default branch with title: "Fix #{issue['number']}: {issue['title']}"
- Run tests and include results
Return JSON: {{"branch": "{branch}", "pr_url": "<link>", "notes": "..." }}
""".strip()


# ---------- UI ----------
st.set_page_config(page_title="Devin × GitHub Issues", layout="wide")

st.markdown(
    "<style>.muted{color:#666}.pill{display:inline-block;background:#eef;padding:4px 10px;border-radius:999px;font-size:12px;margin-right:6px}</style>",
    unsafe_allow_html=True,
)

if needs_config():
    st.stop()

params = st.query_params.to_dict() if hasattr(st, "query_params") else st.experimental_get_query_params()
view = params.get("view", ["home"] if isinstance(params.get("view"), list) else "home")
if isinstance(view, list): 
    view = view[0]

# ---------------- Home (Issues list) ----------------
if view == "home":
    st.title(f"Issues — {GITHUB_OWNER}/{GITHUB_REPO}")
    st.caption("Click **Scope** to have Devin produce a plan + confidence score. Use **Complete with this plan** on the session page.")
    try:
        issues = list_issues()
    except Exception as e:
        st.error(f"Error loading issues:\n\n{e}")
        st.stop()

    if not issues:
        st.info("No open issues found.")

    for i in issues:
        with st.container(border=True):
            left, right = st.columns([8, 1])
            with left:
                st.markdown(f"**#{i['number']} — {i['title']}**")
                st.markdown(f"[{i['html_url']}]({i['html_url']})")
                if i["labels"]:
                    st.write("Labels:", " ".join([f"`{l}`" for l in i["labels"]]))
            with right:
                if st.button("Scope", key=f"scope-{i['number']}"):
                    issue = get_issue(i["number"])
                    prompt = make_scope_prompt(issue)
                    try:
                        session = devin_create_session(prompt=prompt)
                    except Exception as e:
                        st.error(str(e))
                        st.stop()
                    sid = session["id"]
                    safe_set_query_params(
                        view="session",
                        id=sid,
                        issue=str(i["number"]),
                        type="scope"
                    )
                    do_rerun()

# ---------------- Session (Status page) ----------------
else:
    sid = params.get("id")
    issue_num = params.get("issue")
    s_type = params.get("type", "scope")
    if isinstance(sid, list): sid = sid[0]
    if isinstance(issue_num, list): issue_num = issue_num[0]
    if isinstance(s_type, list): s_type = s_type[0]

    st.markdown("[← Back to issues](/)", help="Return to issues list")

    pills = st.columns([4, 4, 4, 2])
    pills[0].markdown(f"<span class='pill'>Session: {sid}</span>", unsafe_allow_html=True)
    pills[1].markdown(f"<span class='pill'>Issue: #{issue_num}</span>", unsafe_allow_html=True)
    pills[2].markdown(f"<span class='pill'>Type: {s_type}</span>", unsafe_allow_html=True)
    do_refresh = pills[3].button("Refresh")

    # Poll Devin status
    raw = None
    parsed = {}

    def fetch_status():
        try:
            data = devin_get_session(sid)
        except Exception as e:
            return {"error": str(e), "raw": None, "parsed": {}}

        try:
            tmp = {}
            if data.get("structured_output"):
                tmp.update(data["structured_output"])
            else:
                out = data.get("output")
                if isinstance(out, str):
                    tmp.update(json.loads(out))
                elif isinstance(out, dict) and isinstance(out.get("text"), str):
                    tmp.update(json.loads(out["text"]))
        except Exception as e:
            pass

        # cache
        SESSION_CACHE[sid] = {"raw": data, "parsed": tmp}
        return {"raw": data, "parsed": tmp}

    # Use cache unless refresh clicked
    cache_hit = SESSION_CACHE.get(sid)
    if do_refresh or not cache_hit:
        status_data = fetch_status()
    else:
        status_data = cache_hit

    if status_data and "error" in status_data:
        st.error(status_data["error"])
    else:
        raw = status_data.get("raw")
        parsed = status_data.get("parsed", {})

    left, right = st.columns(2)

    with left:
        raw_status = (raw or {}).get("status", "")
        parsed_has_result = isinstance(parsed, dict) and any(
            k in parsed for k in ("pr_url", "branch", "notes")
        )
        status_looks_done = raw_status in {"completed", "success", "succeeded", "done", "finished"}

        completed = (s_type == "complete") and (parsed_has_result or status_looks_done)

        # Header
        if completed:
            try:
                _issue = get_issue(int(issue_num))
                _title = _issue["title"]
                st.success(f"Ticket Completed — #{issue_num} · {_title}")
            except Exception:
                st.success("Ticket Completed")
        else:
            st.subheader("Action Plan and Confidence Score")

        # Summary (only helpful before completion)
        if not completed:
            if parsed:
                if "confidence_score" in parsed:
                    st.write(f"**Confidence Score:** {parsed['confidence_score']}")
                if isinstance(parsed.get("plan"), list) and parsed["plan"]:
                    for step in parsed["plan"]:
                        st.markdown(f"- {step}")
            else:
                st.caption("No structured JSON parsed yet — check Raw.")

        # Complete with this plan (hide once completed)
        if (not completed) and isinstance(parsed.get("plan"), list) and parsed["plan"]:
            with st.form(key="complete_with_plan"):
                st.caption("Click to trigger **Complete** using the parsed plan.")
                submitted = st.form_submit_button("Complete with this plan")
                if submitted:
                    try:
                        issue = get_issue(int(issue_num))
                        action_plan_str = json.dumps(parsed["plan"], indent=2)
                        prompt = make_complete_prompt(issue, action_plan_str)
                        session = devin_create_session(prompt=prompt)
                        new_sid = session["id"]
                        safe_set_query_params(view="session", id=new_sid, issue=str(issue["number"]), type="complete")
                        do_rerun()
                    except Exception as e:
                        st.error(str(e))

        # Parsed JSON block 
        st.subheader("Parsed JSON")
        if parsed and len(parsed.keys()) > 0:
            st.code(json.dumps(parsed, indent=2), language="json")
        else:
            st.caption("No parsed result yet")

        # Close issue button (still only when we have a PR and we're on 'complete')
        if parsed.get("pr_url") and s_type == "complete":
            if st.button(f"Close Issue #{issue_num}", key="close_issue"):
                try:
                    close_issue(int(issue_num), f"Completed via PR: {parsed['pr_url']}")
                    st.success(f"Issue #{issue_num} has been closed!")
                except Exception as e:
                    st.error(f"Failed to close issue: {e}")

    with right:
        st.subheader("Raw")
        if raw is None:
            st.caption("Polling…")
        else:
            st.code(json.dumps(raw, indent=2), language="json")


    # Auto-refresh button
    if raw and isinstance(raw, dict):
        status = raw.get("status", "")
        if status and status not in ["completed", "failed", "errored"]:
            count = st.session_state.get("auto_count", 0)
            if count < 60:
                st.session_state["auto_count"] = count + 1
                time.sleep(3)
                do_rerun()
