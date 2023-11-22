import datetime


def get_status() -> str:
    statuses = {
        "1": "To Do",
        "2": "In progress",
        "3": "Done",
    }
    for num, status in statuses.items():
        print(f"{num}: {status}")
    status = statuses.get(input("Select status: "))
    if not status:
        print("Invalid input, please select a valid number.")
        return get_status()
    return status


def get_date() -> str:
    date_input = input("Due date (dd/mm/yy): ")
    try:
        date = datetime.datetime.strptime(date_input, "%d/%m/%y").strftime("%d/%m/%y")
    except:
        print("Error: make sure the data is in the format dd/mm/yy")
        return get_date()
    return date


def get_new_id(tasks) -> str:
    if not tasks.tasks:
        return "1"
    else:
        return str(int(tasks.tasks[-1].id) + 1)


def format_string(string, max_length):
    if len(string) > max_length:
        return string[: max_length - 3] + "..."
    else:
        return string
