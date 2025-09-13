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
pytest
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

---

## 🛠️ Recommended VS Code Extensions  

Listed in `.vscode/extensions.json`:  

- **Python** (`ms-python.python`) – Core Python support  
- **Black Formatter** (`ms-python.black-formatter`) – Auto formatting  
- **Flake8** (`ms-python.flake8`) – Linting & code quality  
- **SQLite** (`alexcvzz.vscode-sqlite`) – Manage SQLite database files  
- **Pytest** (`ms-pytest.pytest`) – Integrated test runner  

---

## ✅ Project Requirements & Checklist  

- [ ] Unit tests implemented  
- [ ] Improved README (this file!)  
- [ ] Database integration completed  
- [ ] Uploaded to GitHub (not zipped, with `.gitignore`)  
- [ ] Modular code (logical file structure, comments)  
- [ ] Complete analytics module (per portfolio guidelines)  
- [ ] Streak calculation respects habit periodicity  
- [ ] 4 weeks of predefined time-series habit data for testing streaks  
- [ ] Unit tests cover:  
  - Habit creation, editing & deletion  
  - Analytics functionality  
