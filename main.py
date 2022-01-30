from db import get_db, add_user, add_completion, add_habit
from habit import HabitDB
from user import UserDB
import analyze as an
import questionary as qu
from validators import HabitNameValidator, UserNameValidator
from exceptions import UserNameNotExisting
import test_data
import os


# Auslagern der Input-Befehle in eigene Funktionen zum einfachen Testen des Inputs
# TODO: vielleicht macht es Sinn, die main.db als Default-Datenbank zu verwenden? Dann muss man sie nicht mehr übergeben
def input_username(database, action):
    text = "Please choose a username: " if action == "create" else "Please enter your username: "
    username = qu.text(text, validate=UserNameValidator(database, action)).ask()
    return username


def input_new_habit(user, database):
    habit_name = qu.text("Which habit do you want to add?",
                         validate=HabitNameValidator(database, user)).ask()
    periodicity = qu.select(f"Which periodicity shall {habit_name} have?",
                            choices=["daily", "weekly", "monthly", "yearly"]).ask()
    return habit_name, periodicity


# Programmlogik
def create_new_user(database):
    username = input_username(database, "create")
    app_user = UserDB(username, database)
    app_user.store_user()
    print(f"A user with the username {username} has successfully been created. Logged in as {username}.")
    return app_user


def login(database):
    username_existing = False
    count = 0
    while not username_existing:
        try:
            username = input_username(database, "login")
            user = UserDB(username, database)
            if not an.check_for_user(user):
                raise UserNameNotExisting(user.username)
            print(f"Logged in as {username}")
            username_existing = True
            return user
        except UserNameNotExisting:
            print("This user does not exist. Please enter a username that does.")
            if count == 2:  # wenn man drei Mal den Nutzernamen falsch eingegeben hat, wird das Programm unterbrochen
                print("Login failed three times.")
                return False
            count += 1
            # TODO: nach zwei Fehlversuchen, sich einzuloggen, fragen, ob man neuen User anlegen oder gehen möchte
            # TODO: Was tun, wenn man den eigenen Nutzernamen vergessen hat? Liste an Nutzernamen anzeigen? Pech?


def start(database):
    start_action = qu.select(
        "What do you want to do?",
        choices=["Create new user", "Login"]
    ).ask()
    if start_action == "Create new user":
        current_user = create_new_user(database)
    else:
        current_user = login(database)
    if current_user:
        return current_user
    else:
        start(database)


def create_habit(user, database):
    habit_name, periodicity = input_new_habit(user, database)
    habit = HabitDB(habit_name, periodicity, user, database)
    habit.store_habit()
    print(f"The habit \"{habit_name}\" with the periodicity \"{periodicity}\" was created.")
    return habit


def identify_habit(habit_action, database, user):
    tracked_habits = an.return_habits_only(user)
    habit_name = qu.select(f"Which habit do you want to {habit_action}?",
                           choices=tracked_habits).ask()
    habit_periodicity = an.return_periodicity(user, habit_name)
    habit = HabitDB(habit_name, habit_periodicity, user, database)
    return habit


def delete_habit():
    pass


def modify_habit():
    pass


def check_off_habit():
    pass


def analyze_habits(database, user):
    type_of_analysis = qu.select("Do you want to analyse all habits or just one?",
                                 choices=["All habits", "Just one"]).ask()
    if type_of_analysis == "All habits":
        pass
    else:  # type_of_analysis == "Just one"
        habit = identify_habit("analyze", database, user)
        print(f"You want to analyse {habit.name}")


def cli():
    main_database = get_db()
    habit_data = test_data.DataCli("main.db")
    # TODO: Generelle Information: Wie bekomme ich Hilfe? Wie beende ich das Programm?
    # TODO: Handle Python KeyboardInterrupt

    # Program Flow
    current_user = start(main_database)
    next_action = qu.select(
        "What do you want to do next?",
        choices=["Add habit", "Delete habit", "Modify habit", "Check off habit", "Analyze habits"]
    ).ask()
    if next_action == "Add habit":
        action = "add"
        current_habit = create_habit(current_user, main_database)
    elif next_action == "Delete habit":
        action = "delete"
        delete_habit()
    elif next_action == "Modify habit":
        action = "modify"
        modify_habit()
    elif next_action == "Check off habit":
        action = "check off"
        check_off_habit()
    else:  # check_action == "Analyze habits"
        analyze_habits(main_database, current_user)

    # TODO: Daten in der Zukunft dürfen nicht eingegeben werden!


if __name__ == "__main__":
    cli()
