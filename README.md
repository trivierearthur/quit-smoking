# Quit Smoking App  

A console-based habit tracker to help you quit smoking, build healthier routines, and gain insights through analytics.  

##  Features

- ** Dashboard**: View all your habits with current status and record counts
- ** Daily Logging**: Record your daily habit values and track progress
- ** Analytics**: Visualize progress with time series plots and streak calculations
- ** Reduction Plans**: Generate personalized tapering schedules for elimination habits
- ** Cost Tracking**: Calculate money saved from avoiding cigarettes
- ** Habit Management**: Add, update, and delete custom habits
- ** Interactive Charts**: Matplotlib visualizations for progress tracking

##  Quick Start

The app comes with 5 predefined habits to get you started:

**Elimination Habits** (reduce these):
- **Cigarettes Smoked** (daily) - Track daily cigarette consumption
- **Nicotine Gum Used** (daily) - Monitor nicotine replacement usage

**Establishment Habits** (build these):
- **Meditation Time** (daily) - Track daily meditation practice
- **Sport** (weekly) - Monitor physical activity engagement  
- **Specialist Appointment** (monthly) - Track healthcare appointments

The app automatically generates 4 weeks of sample data when first launched, so you can immediately explore all features and see how analytics work.

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

##  How to Use

Once launched, you'll see a menu with 8 options:

1. **Dashboard** - View all habits with today's values and total records
2. **Log Today Habits** - Enter values for your habits (e.g., cigarettes smoked)
3. **Show Reduction Plans** - Get personalized tapering schedules for elimination habits
4. **Show Analytics** - View streak statistics and interactive progress charts
5. **Add Habit** - Create custom habits (daily/weekly/monthly, elimination/establishment)
6. **Delete Habit** - Remove habits you no longer want to track
7. **Update Habit** - Modify existing habit properties
8. **Exit** - Close the application

###  Analytics Features

The analytics module provides comprehensive insights:

- **Streak Calculations**: Find your longest consecutive days across all habits
- **Time Series Charts**: 28-day trend visualization for each habit
- **Weekly Progress**: Cigarette avoidance and cost savings analysis
- **Visual Progress**: Interactive matplotlib charts and graphs

###  Data Storage

- All data is stored in a local SQLite database (`.db/habits.sqlite`)
- Data persists between sessions automatically
- No cloud storage - your data stays private on your machine

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


---

##  Project Structure

```
quit-smoking/
├── src/                    # Main application code
│   ├── analytics.py        # Functional programming analytics & visualization
│   ├── cli.py             # Command-line interface and menu system
│   ├── constants.py       # App constants and default habits
│   ├── db.py              # SQLite database operations
│   ├── habit_manager.py   # Core habit management logic
│   ├── models.py          # Data models and structures
│   └── utils.py           # Utility functions
├── tests/                  # Unit tests (pytest)
├── .db/                   # SQLite database storage
├── main.py                # Application entry point
└── requirements.txt       # Python dependencies
```

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

