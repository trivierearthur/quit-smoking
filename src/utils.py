import random
from datetime import timedelta, date


def get_random_previous_day(day: date, max_days: int):
    return (day - timedelta(days=random.randint(1, max_days))).isoformat()


def input_select(label: str, options: list[str]):
    print(label)
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt.capitalize()}")
    while True:
        try:
            choice = int(input("\nEnter option number: ").strip())
            return options[choice - 1]
        except ValueError:
            pass
        except (KeyboardInterrupt, SystemExit):
            print("\nExiting. Goodbye!")
        print("Invalid option, try again.")
