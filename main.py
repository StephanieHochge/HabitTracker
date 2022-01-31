import db
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


def input_new_habit(user):
    habit_name = qu.text("Which habit do you want to add?",
                         validate=HabitNameValidator(user)).ask()
    periodicity = input_periodicity(habit_name)
    return habit_name, periodicity


def input_periodicity(habit_name):
    periodicity = qu.select(f"Which periodicity shall {habit_name} have?",
                            choices=["daily", "weekly", "monthly", "yearly"]).ask()
    return periodicity


def input_new_habit_name(user):
    new_name = qu.text("Please enter a new name: ", validate=HabitNameValidator(user)).ask()
    return new_name


def input_habit_modify_target():
    target = qu.select("What part of the habit do you want to modify?", choices=["name", "periodicity", "both"]).ask()
    return target


def input_chosen_habit(habit_action, tracked_habits):
    habit_name = qu.select(f"Which habit do you want to {habit_action}?", choices=tracked_habits).ask()
    return habit_name


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


def create_habit(user):
    habit_name, periodicity = input_new_habit(user)
    habit = HabitDB(habit_name, periodicity, user, user.database)
    habit.store_habit()
    print(f"The habit \"{habit_name}\" with the periodicity \"{periodicity}\" was created.")
    return habit


def identify_habit(habit_action, user):
    tracked_habits = an.return_habits_only(user)
    habit_name = input_chosen_habit(habit_action, tracked_habits)
    habit_periodicity = an.return_periodicity(user, habit_name)
    habit = HabitDB(habit_name, habit_periodicity, user, user.database)
    return habit


def delete_habit(user):
    habit = identify_habit("delete", user)
    if habit.delete_habit():
        print(f"The habit \"{habit.name}\" with the periodicity \"{habit.periodicity}\" successfully deleted.")
        # TODO: muss ich jetzt auch nochmal testen, ob das geklappt hat?


def modify_habit(user):
    habit = identify_habit("modify", user)
    target = input_habit_modify_target()
    if target in ("name", "both"):
        print(f"The habit's old name is {habit.name}.")
        new_name = input_new_habit_name(user)
        if habit.modify_habit(name=new_name):
            print(f"The habit's name was successfully changed to {new_name}.")
    if target in ("periodicity", "both"):
        print(f"The habit's old periodicity is {habit.periodicity}.")
        new_periodicity = input_periodicity(habit.name)
        if habit.modify_habit(periodicity=new_periodicity):
            print(f"The habit's periodicity was successfully changed to {new_periodicity}.")


def check_off_habit():
    pass


def analyze_habits(user):
    type_of_analysis = qu.select("Do you want to analyse all habits or just one?",
                                 choices=["All habits", "Just one"]).ask()
    if type_of_analysis == "All habits":
        pass
    else:  # type_of_analysis == "Just one"
        habit = identify_habit("analyze", user)
        print(f"You want to analyse {habit.name}")


def test_data_existing(database):
    """
    checks if the test data has already been entered or not
    :return:
    """
    return db.user_data_existing(database)


def cli():
    main_database = get_db()
    if not db.user_data_existing(main_database):  # creates test data only if no other data is existing
        test_data.DataCli("main.db")
    # TODO: wäre es vielleicht nicht doch besser, auf eine separate Testdatenbank zurückzugreifen, wo bei jedem
    #  Neustart die ursprünglichen Daten wieder enthalten sind?
    # TODO: Generelle Information: Wie bekomme ich Hilfe? Wie beende ich das Programm?
    # TODO: Handle Python KeyboardInterrupt

    # Program Flow
    current_user = start(main_database)
    next_action = qu.select(
        "What do you want to do next?",
        choices=["Add habit", "Delete habit", "Modify habit", "Check off habit", "Analyze habits"]
    ).ask()
    if next_action == "Add habit":
        create_habit(current_user)
    elif next_action == "Delete habit":
        delete_habit(current_user)
    elif next_action == "Modify habit":
        modify_habit(current_user)
    elif next_action == "Check off habit":
        check_off_habit()
    else:  # check_action == "Analyze habits"
        analyze_habits(current_user)

    # TODO: Daten in der Zukunft dürfen nicht eingegeben werden!


if __name__ == "__main__":
    cli()
