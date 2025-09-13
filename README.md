# 🚭 Quit Smoking App  

A console-based habit tracker to help you quit smoking, build healthier routines, and gain insights through analytics.  

---

## 📦 Project Setup  

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

**⚠️ Troubleshooting (Windows PowerShell):**  
If you see an error about script execution being disabled when activating the virtual environment, run:  

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This allows you to run local scripts like `Activate.ps1`.  
If you ever delete `.venv`, simply repeat the steps above.  

---

## ▶️ Running the App  

Launch the app with:  

```sh
python main.py
```

This starts the console interface for the Quit Smoking App.  

---

## 🧪 Running Tests  

You can run unit tests using **pytest** in two ways:  

### 1. Command Line  

```powershell
python -m pytest
```

This will discover and run all tests in files named `test_*.py`.  

### 2. VS Code Testing Panel  

- Open the **Testing panel** (beaker icon or `Ctrl+Shift+`)  
- Ensure **pytest** is selected as the test framework (configure if prompted)  
- Click the play/run icons next to your tests  

---


## 📊 Dependencies

- **pytest** → Unit testing
- **matplotlib** → Analytics & plotting
- **black** → Code formatting
- **flake8** → Linting

---

## 🧹 Linting & Formatting

- **Black**: To auto-format your code, run:
  ```powershell
  black .
  ```
- **Flake8**: To check code style and lint for errors, run:
  ```powershell
  flake8 .
  ```

---

## 🛠️ Recommended VS Code Extensions  

Listed in `.vscode/extensions.json`:  

- **Python** (`ms-python.python`) – Core Python support  
- **Black Formatter** (`ms-python.black-formatter`) – Auto formatting  
- **Flake8** (`ms-python.flake8`) – Linting & code quality  
- **SQLite** (`qwtel.sqlite-viewer`) – Manage SQLite database files  
- **Pytest** (`ms-pytest.pytest`) – Integrated test runner  

---

## ✅ Project Requirements & Checklist  

- [ ] Unit tests implemented  

- [ ] Your project is uploaded to GitHub (code not zipped) and polished.

- [x] Your project has a good Readme.

- [x] You follow basic Python naming conventions and don't commit files the users don't need (e.g. pycache, use a .gitignore if needed).

- [x] Your project is modular and consists of several, logically split files that make it easy for users to understand how your app works.

- [ ] You have some basic code comments.

- [ ] **Your analytics module is complete, as defined in the portfolio guidelines.**

- [ ] Your streak calculation respects the habit's periodicity.

- [x] You have 4 weeks worth of predefined habit data (time-series data) that you can use in unit tests to verify your streak calculations.

- [ ] You have a good suite of unit tests covering a) habit creation, editing and deletion and b) tests for each functionality in the analytics module.
