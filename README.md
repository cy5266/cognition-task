# Cognition Task

A Flask web application that integrates Devin AI with GitHub Issues for automated issue scoping and completion.

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- GitHub personal access token
- Devin API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/cy5266/cognition-task.git
cd cognition-task
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:
```bash
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_OWNER=your_github_username
GITHUB_REPO=your_repository_name
DEVIN_API_KEY=your_devin_api_key
DEVIN_BASE_URL=https://api.devin.ai/v1
```

### Running the Application

To run the Flask web application:
```bash
python app.py
```

The application will start on `http://localhost:5000` and provide a web interface for:
- Viewing GitHub issues
- Scoping issues with Devin AI
- Completing issues automatically

### Running Tests

To run the test suite:
```bash
pytest
```

Or alternatively:
```bash
python -m pytest
```

To run tests with verbose output:
```bash
pytest -v
```

## Project Structure

```
cognition-task/
├── README.md          # This file
├── app.py            # Flask web application
├── requirements.txt  # Python dependencies
└── tests/           # Test directory
    └── test_app.py  # Application tests
```

## Features

- **Issue Dashboard**: View all open GitHub issues in a web interface
- **AI Scoping**: Use Devin AI to automatically scope issues with confidence scores and plans
- **Automated Completion**: Have Devin AI implement solutions and create pull requests
- **Real-time Status**: Monitor Devin session progress with live updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## Getting Help

If you encounter any issues with setup or running the application, please check:
1. You have Python 3.7+ installed
2. All dependencies are installed via `pip install -r requirements.txt`
3. Your `.env` file is properly configured with valid API keys
4. You're running commands from the project root directory

For additional help, please open an issue on GitHub.
