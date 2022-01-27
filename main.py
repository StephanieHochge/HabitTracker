from db import get_db, add_user, add_completion, add_habit
from habit import HabitDB
from user import UserDB
import analyze as an
import questionary as qu
from validators import HabitNameValidator, UserNameValidator
from exceptions import UserNameNotExisting
import os


# Auslagern der Input-Befehle in eigene Funktionen zum einfachen Testen des Inputs
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
    tracked_habits = an.return_habits(database, user)
    habit_name = qu.select(f"Which habit do you want to {habit_action}?",
                           choices=tracked_habits).ask()
    habit_periodicity = an.return_periodicity(database, user, habit_name)
    # user.username und habit_name könnte auch nur mit dem Argument "habit" übergeben werden
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
    #  just for testing purposes, test data is inserted
    user_sh = UserDB("StephanieHochge", main_database)
    user_rb = UserDB("RajaBe", main_database)
    user_le = UserDB("LibertyEvans", main_database)
    add_user(user_sh)
    add_user(user_rb)
    add_user(user_le)
    teeth_rb = HabitDB("Brush teeth", "daily", user_rb, main_database)
    teeth_sh = HabitDB("Brush teeth", "daily", user_sh, main_database)
    dance_sh = HabitDB("Dance", "weekly", user_sh, main_database)
    windows_sh = HabitDB("Clean windows", "monthly", user_sh, main_database)
    bathroom_sh = HabitDB("Clean bathroom", "weekly", user_sh, main_database)
    dentist_sh = HabitDB("Go to dentist", "yearly", user_sh, main_database)
    add_habit(teeth_rb)
    add_habit(teeth_sh, "2021-11-30 07:54:24.999098")
    add_habit(dance_sh, "2021-10-31 07:54:24.999098")
    add_habit(windows_sh, "2021-10-31 07:54:24.999098")
    add_habit(bathroom_sh, "2022-10-31 07:56:24.999098")
    add_habit(dentist_sh, "2022-10-31 07:56:24.999098")
    add_completion(teeth_rb)
    add_completion(teeth_sh, "2021-12-01")
    add_completion(teeth_sh, "2021-12-01")
    add_completion(teeth_sh, "2021-12-02")
    add_completion(teeth_sh, "2021-12-04")
    add_completion(teeth_sh, "2021-12-05")
    add_completion(teeth_sh, "2021-12-07")
    add_completion(teeth_sh, "2021-12-08")
    add_completion(teeth_sh, "2021-12-09")
    add_completion(teeth_sh, "2021-12-10")
    add_completion(teeth_sh, "2021-12-11")
    add_completion(teeth_sh, "2021-12-12")
    add_completion(teeth_sh, "2021-12-13")
    add_completion(teeth_sh, "2021-12-14")
    add_completion(teeth_sh, "2021-12-15")
    add_completion(teeth_sh, "2021-12-16")
    add_completion(teeth_sh, "2021-12-17")
    add_completion(teeth_sh, "2021-12-18")
    add_completion(teeth_sh, "2021-12-19")
    add_completion(teeth_sh, "2021-12-20")
    add_completion(teeth_sh, "2021-12-21")
    add_completion(teeth_sh, "2021-12-22")
    add_completion(teeth_sh, "2021-12-23")
    add_completion(teeth_sh, "2021-12-24")
    add_completion(teeth_sh, "2021-12-25")
    add_completion(teeth_sh, "2021-12-26")
    add_completion(teeth_sh, "2021-12-27")
    add_completion(teeth_sh, "2021-12-29")
    add_completion(teeth_sh, "2021-12-30")
    add_completion(teeth_sh, "2021-12-31")
    add_completion(dance_sh, "2021-11-06")
    add_completion(dance_sh, "2021-11-07")
    add_completion(dance_sh, "2021-11-11")
    add_completion(dance_sh, "2021-11-13")
    add_completion(dance_sh, "2021-11-14")
    add_completion(dance_sh, "2021-11-21")
    add_completion(dance_sh, "2021-11-25")
    add_completion(dance_sh, "2021-11-27")
    add_completion(dance_sh, "2021-11-28")
    add_completion(dance_sh, "2021-12-02")
    add_completion(dance_sh, "2021-12-04")
    add_completion(dance_sh, "2021-12-05")
    add_completion(dance_sh, "2021-12-16")
    add_completion(dance_sh, "2021-12-18")
    add_completion(dance_sh, "2021-12-19")
    add_completion(dance_sh, "2021-12-30")
    add_completion(bathroom_sh, "2021-11-06")
    add_completion(bathroom_sh, "2021-11-13")
    add_completion(bathroom_sh, "2021-11-20")
    add_completion(bathroom_sh, "2021-12-04")
    add_completion(bathroom_sh, "2021-12-11")
    add_completion(bathroom_sh, "2021-12-18")
    add_completion(bathroom_sh, "2022-01-01")
    add_completion(windows_sh, "2022-11-17")
    add_completion(windows_sh, "2022-12-30")
    add_completion(dentist_sh, "2022-12-17")
    add_completion(dentist_sh, "2021-12-05")
    add_completion(teeth_sh, "2021-12-03")
    add_completion(dance_sh, "2021-12-21")

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
