# Quit Smoking App


## Initialize


To set up the project, create a virtual environment and install the required dependencies:

```powershell
# Create a new virtual environment (if .venv does not exist)
python -m venv .venv

# Activate the virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```


**Troubleshooting (Windows PowerShell):**
If you see an error about script execution being disabled when activating the virtual environment, run the following command in a PowerShell window (as your user, not as admin):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This allows you to run local scripts like `Activate.ps1`.

If you ever delete the `.venv` folder, simply repeat these steps to recreate it and reinstall dependencies.


## Running the App

To start the application, run the following command from the project directory:

```sh
python main.py
```

This will launch the console interface for the Quit Smoking App.

## Dependencies

- **pytest**: For running unit tests
- **matplotlib**: For analytics and plotting

## VS Code Extensions

The following VS Code extensions are recommended for this project (see `.vscode/extensions.json`):

- **Python** (`ms-python.python`): Core support for Python development in VS Code.
- **Black Formatter** (`ms-python.black-formatter`): Code formatting using Black.
- **Flake8** (`ms-python.flake8`): Linting and code quality checks.
- **SQLite** (`alexcvzz.vscode-sqlite`): View and manage SQLite database files.
- **Pytest** (`ms-pytest.pytest`): Integration for running and managing pytest unit tests.



## Todo
- Unit tests
- Improve Readme file
- DB
- Your project is uploaded to GitHub (code not zipped) and polished.
- Your project has a good Readme.
- You follow basic Python naming conventions and don't commit files the users don't need (e.g. pycache, use a .gitignore if needed).
- Your project is modular and consists of several, logically split files that make it easy for users to understand how your app works.
- You have some basic code comments.
- Your analytics module is complete, as defined in the portfolio guidelines.
- Your streak calculation respects the habit's periodicity.
- You have 4 weeks worth of predefined habit data (time-series data) that you can use in unit tests to verify your streak calculations.
- You have a good suite of unit tests covering a) habit creation, editing and deletion and b) tests for each functionality in the analytics module.