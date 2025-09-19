# GitHub Issues + Devin Integration

This project provides a Streamlit dashboard that connects your GitHub repository issues with Devin AI sessions.

## Features

You can:
- View open issues from a GitHub repository
- Trigger a Scope session to generate a confidence score and structured action plan
- Trigger a Complete session to automatically execute the plan and (optionally) close out the issue. When executing the plan, the Devin bot will create a PR based on the action plan and the link to the PR will be provided on the dashboard.

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/cy5266/cognition-task.git
cd cognition-task
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate   # on Mac/Linux
# or on Windows:
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root with the following environment variables:
```
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=your_github_username
GITHUB_REPO=your_repository_name
DEVIN_API_KEY=your_devin_api_key
```

### Running the Application

To launch the Streamlit dashboard:
```bash
streamlit run app.py
```

This will start a local development server at http://localhost:8501

### Running Tests

To run the test suite:
```bash
pytest
```

For verbose output:
```bash
pytest -v
```

To run tests with coverage:
```bash
pytest --cov
```

## Project Structure

```
cognition-task/
├── README.md          # This file
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (create this)
└── tests/           # Test directory
    ├── test_app.py  # Application tests
    └── test_math.py # Math utility tests
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## Troubleshooting

If you encounter issues:

1. **Missing environment variables**: Make sure you've created a `.env` file with all required variables
2. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Port conflicts**: If port 8501 is in use, Streamlit will automatically try the next available port
4. **API authentication**: Verify your GitHub token and Devin API key have the necessary permissions

For additional help, please open an issue on GitHub.
