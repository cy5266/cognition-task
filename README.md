# Cognition Task

A Flask web application that integrates Devin AI with GitHub Issues, providing an automated workflow for scoping and completing GitHub issues.

## Overview

This application creates a web dashboard that allows you to:
- View open GitHub issues from a specified repository
- Use Devin AI to scope issues and generate implementation plans
- Automatically complete issues with Devin AI integration

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- GitHub Personal Access Token
- Devin API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cy5266/cognition-task.git
cd cognition-task
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following environment variables:
```bash
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_OWNER=your_github_username_or_org
GITHUB_REPO=your_repository_name
DEVIN_API_KEY=your_devin_api_key
DEVIN_BASE_URL=https://api.devin.ai/v1
```

## Running the Application

To start the Flask web server:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

Alternatively, you can use Flask's built-in command:
```bash
FLASK_APP=app.py flask run
```

## Running Tests

To run the test suite:
```bash
pytest
```

Or with verbose output:
```bash
pytest -v
```

You can also run tests using Python's unittest module:
```bash
python -m pytest
```

## Project Structure

```
cognition-task/
├── README.md          # This file
├── app.py            # Main Flask application
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (create this file)
└── tests/           # Test directory
    └── test_app.py  # Application tests
```

## Environment Variables

The application requires the following environment variables:

- `GITHUB_TOKEN`: Personal access token for GitHub API access
- `GITHUB_OWNER`: GitHub username or organization name
- `GITHUB_REPO`: Repository name to manage issues for
- `DEVIN_API_KEY`: API key for Devin AI integration
- `DEVIN_BASE_URL`: Base URL for Devin API (defaults to https://api.devin.ai/v1)

## Usage

1. Start the application with `python app.py`
2. Open your browser to `http://localhost:5000`
3. View the list of open GitHub issues
4. Click "Scope" to have Devin analyze an issue and create an implementation plan
5. Click "Complete" to have Devin implement the solution and create a pull request

## Dependencies

- `requests`: HTTP library for API calls
- `python-dotenv`: Environment variable management
- `rich`: Enhanced terminal output
- `flask`: Web framework

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## Troubleshooting

If you encounter issues:

1. **Missing environment variables**: Ensure your `.env` file contains all required variables
2. **Import errors**: Run `pip install -r requirements.txt` to install dependencies
3. **API errors**: Verify your GitHub token and Devin API key are valid
4. **Port conflicts**: The app runs on port 5000 by default; ensure it's available

For additional help, please open an issue on GitHub.
