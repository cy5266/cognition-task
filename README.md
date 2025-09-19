GitHub Issues + Devin Integration

This project provides a Streamlit dashboard that connects your GitHub repository issues with Devin AI sessions.

You can:
- View open issues from a GitHub repository
- Trigger a Scope session to generate a confidence score and structured action plan
- Trigger a Complete session to automatically execute the plan and (optionally) close out the issue

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
