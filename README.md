# Cognition Task

A simple Python application for demonstrating basic setup and development workflow.

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

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

To run the main application:
```bash
python app.py
```

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
├── app.py            # Main application entry point
├── requirements.txt  # Python dependencies
└── tests/           # Test directory
    └── test_app.py  # Application tests
```

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
3. You're running commands from the project root directory

For additional help, please open an issue on GitHub.
