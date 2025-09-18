import sys
import os
import main

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


def test_main_menu_exit(monkeypatch, capsys):
    # Simulate user entering '8' to exit immediately
    inputs = iter(["8"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    # Patch out functions that would interact with DB or require more input
    monkeypatch.setattr(main, "init_db", lambda: None)

    class FakeTracker:
        def __init__(self):
            self.habits = []

        def add_habit(self, habit):
            self.habits.append(habit)

    monkeypatch.setattr(main, "load_tracker", lambda: FakeTracker())
    monkeypatch.setattr(
        main,
        "setup_initial_consumption",
        lambda tracker: {"Cigarettes Smoked": 1, "Nicotine Gum Used": 1},
    )
    monkeypatch.setattr(main, "generate_reduction_plan", lambda c, g: {})
    monkeypatch.setattr(main, "save_habit", lambda h: None)
    monkeypatch.setattr(main, "show_dashboard", lambda t: print("Dashboard"))
    monkeypatch.setattr(main, "log_habit_values", lambda t: None)
    monkeypatch.setattr(main, "show_reduction_plans", lambda t: None)
    monkeypatch.setattr(main, "show_analytics", lambda t: None)
    monkeypatch.setattr(main, "add_habit", lambda t: None)
    monkeypatch.setattr(main, "remove_habit", lambda t: None)
    monkeypatch.setattr(main, "modify_habit", lambda t: None)

    main.main()
    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out
