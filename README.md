GitHub Issues + Devin Integration

This project provides a Streamlit dashboard that connects your GitHub repository issues with Devin AI sessions.

You can:
- View open issues from a GitHub repository
- Trigger a Scope session to generate a confidence score and structured action plan
- Trigger a Complete session to automatically execute the plan and (optionally) close out the issue. When executing the plan, the Devin bot will create a PR based on the action plan and the link to the PR will be provided on the dashboard.

Notes:
- I personally think the hosted demo works better in light mode (some text is harder to read in dark mode).
- There is an optional feature to 'Close Issue' if the completed ticket looks good, which automatically closes out the ticket on GitHub.
- Scoping and completing an issue may take a few minutes to run. In light mode, you will be able to see a loading icon. Once that stops running, pressing the 'Refresh' button on the dashboard will display the results.
- Devin currently allows only 5 concurrent sessions. If multiple people are testing the demo, it may hit the limit- please let me know and I can terminate any extra sessions.

Installation

Clone the repository:
- git clone https://github.com/cy5266/cognition-task.git
- cd cognition-task

Create and activate a virtual environment:
- python3 -m venv .venv
- source .venv/bin/activate   # on Mac/Linux
- .venv\Scripts\activate

Install dependencies:

- pip install -r requirements.txt


Launching the app:
- streamlit run app.py

This will start a local dev server (default: http://localhost:8501)
