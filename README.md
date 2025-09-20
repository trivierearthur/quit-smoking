# Quit Smoking App  

A console-based habit tracker to help you quit smoking, build healthier routines, and gain insights through analytics.  

---

## Project Setup  

### 1. Create & Activate Virtual Environment  

```powershell
# Create a new virtual environment (if not already created)
python -m venv .venv

# Activate the virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies  

```powershell
pip install -r requirements.txt
```

** Troubleshooting (Windows PowerShell):**  
If you see an error about script execution being disabled when activating the virtual environment, run:  

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This allows you to run local scripts like `Activate.ps1`.  
If you ever delete `.venv`, simply repeat the steps above.  

---

##  Running the App  

Launch the app with:  

```sh
python main.py
```

This starts the console interface for the Quit Smoking App.  

---

## Running Tests  


You can run all unit tests using **pytest**. This ensures your code is working as expected.

### 1. Command Line

Open a terminal in your project root and run:

```powershell
python -m pytest
```

This will automatically discover and run all tests in files named `test_*.py` inside the `tests/` folder. You should see output showing which tests passed or failed.

If you want to see more detailed output, use:

```powershell
python -m pytest -v
```

### 2. VS Code Testing Panel

- Open the **Testing** panel (beaker icon in the Activity Bar, or `Ctrl+Shift+\`)
- Make sure **pytest** is selected as the test framework (configure if prompted)
- Click the play/run icons next to your tests to run them individually or all at once

If you do not see any tests, ensure your test files are named like `test_*.py` and are in the `tests/` folder.

**Troubleshooting:**
- If you get import errors, make sure your `src/` and `tests/` folders have an `__init__.py` file (can be empty).
- If pytest is not found, install it with `pip install pytest`.

---


## Dependencies

- **pytest** → Unit testing
- **matplotlib** → Analytics & plotting
- **black** → Code formatting
- **flake8** → Linting

---

## Linting & Formatting

- **Black**: To auto-format your code, run:
  ```powershell
  black .
  ```
- **Flake8**: To check code style and lint for errors, run:
  ```powershell
  flake8 .
  ```

---

## Recommended VS Code Extensions  

Listed in `.vscode/extensions.json`:  

- **Python** (`ms-python.python`) – Core Python support  
- **Black Formatter** (`ms-python.black-formatter`) – Auto formatting  
- **Flake8** (`ms-python.flake8`) – Linting & code quality  
- **SQLite** (`qwtel.sqlite-viewer`) – Manage SQLite database files  
- **Pytest** (`ms-pytest.pytest`) – Integrated test runner  

---

## Project Requirements & Checklist  

- [ ] Unit tests implemented  

- [x] Your project is uploaded to GitHub (code not zipped) and polished.

- [x] Your project has a good Readme.

- [x] You follow basic Python naming conventions and don't commit files the users don't need (e.g. pycache, use a .gitignore if needed).

- [x] Your project is modular and consists of several, logically split files that make it easy for users to understand how your app works.

- [ ] You have some basic code comments.

- [x] **Your analytics module is complete, as defined in the portfolio guidelines.**

- [ ] Your streak calculation respects the habit's periodicity.

- [x] You have 4 weeks worth of predefined habit data (time-series data) that you can use in unit tests to verify your streak calculations.

- [ ] You have a good suite of unit tests covering a) habit creation, editing and deletion and b) tests for each functionality in the analytics module.

- [ ]Your solution has an analytics module that allows users to analyse their habits. The functionality of this
analytics module must be implemented using the functional programming paradigm. You are free to consider implementing other functionality as well, but these are the minimal requirements. Provide functionality to
- return a list of all currently tracked habits,
- return a list of all habits with the same periodicity,
- return the longest run streak of all defined habits,
- and return the longest run streak for a given habit