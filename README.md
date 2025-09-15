# Cognition Task

A Python application for cognitive task management and processing.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/cy5266/cognition-task.git
   cd cognition-task
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Application

To start the application, run:

```bash
python app.py
```

The application will start and display relevant output or instructions in the terminal.

## How to Run Tests

This project uses pytest for testing. To run the test suite:

1. **Install test dependencies** (if not already installed)
   ```bash
   pip install pytest
   ```

2. **Run all tests**
   ```bash
   pytest
   ```

3. **Run tests with verbose output**
   ```bash
   pytest -v
   ```

4. **Run specific test file**
   ```bash
   pytest tests/test_filename.py
   ```

## Troubleshooting

### Common Issues

**ImportError or ModuleNotFoundError**
- Ensure you have activated your virtual environment
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using the correct Python version (3.8+)

**Permission Errors**
- On macOS/Linux, you may need to use `python3` instead of `python`
- Ensure you have write permissions in the project directory

**Virtual Environment Issues**
- If virtual environment creation fails, try: `python -m pip install --upgrade pip`
- On some systems, use `python3 -m venv venv` instead of `python -m venv venv`

### Getting Help

If you encounter issues not covered here:
1. Check that all prerequisites are met
2. Ensure you're in the correct directory
3. Verify your Python version with `python --version`
4. Try recreating your virtual environment

## Contributing

This project welcomes contributions! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Follow the installation steps above
4. Make your changes
5. Run tests to ensure everything works: `pytest`
6. Commit your changes: `git commit -m "Description of changes"`
7. Push to your fork: `git push origin feature-name`
8. Create a Pull Request

### Development Setup

For development, you may want to install additional tools:

```bash
pip install pytest pytest-cov flake8 black
```

- `pytest-cov`: For test coverage reports
- `flake8`: For code linting
- `black`: For code formatting

## Project Structure

```
cognition-task/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── tests/             # Test files
│   └── test_*.py      # Test modules
├── README.md          # This file
└── ...                # Additional project files
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
