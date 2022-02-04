import db
from db import get_db, add_user, add_completion, add_habit
from habit import HabitDB
from user import UserDB
import analyze as an
import questionary as qu
from validators import HabitNameValidator, UserNameValidator
from exceptions import UserNameNotExisting, UserHasNoHabits
import test_data
import datetime
import time
import os


# Auslagern der Input-Befehle in eigene Funktionen zum einfachen Testen des Inputs
# TODO: vielleicht macht es Sinn, die main.db als Default-Datenbank zu verwenden? Dann muss man sie nicht mehr übergeben
def input_username(database, action):
    text = "Please choose a username: " if action == "create" else "Please enter your username: "
    username = qu.text(text, validate=UserNameValidator(database, action)).ask()
    return username


def input_new_habit(user):
    habit_name = qu.text("Which habit do you want to create?", validate=HabitNameValidator(user)).ask()
    periodicity = input_periodicity(habit_name.strip())  # strip, um leading und ending spaces zu deleten
    return habit_name.strip(), periodicity


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
        if count == 3:  # wenn man drei Mal den Nutzernamen falsch eingegeben hat, wird das Programm unterbrochen
            print("Login failed three times.")
            return False
        try:
            username = input_username(database, "login")
            user = UserDB(username, database)
            if not an.check_for_user(user):
                raise UserNameNotExisting(user.username)
        except UserNameNotExisting:
            print("This user does not exist. Please enter a username that does.")
            count += 1
        else:
            print(f"Logged in as {username}")
            username_existing = True
            return user


def start(database):
    start_action = qu.select(
        "What do you want to do?",
        choices=["Create new user", "Login", "Exit"]
    ).ask()
    if start_action == "Create new user":
        current_user = create_new_user(database)
    elif start_action == "Login":
        current_user = login(database)
    else:
        print("See you later, Bye!")
        quit()
    if current_user:  # ist nur None, wenn man nicht "Exit" gewählt hat und drei mal einen falschen Nutzernamen
        # eingegeben hat, dann wird nochmal die einleitende Frage gestellt
        # wenn man den Nutzernamen vergessen hat, hat man Pech
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
    habit_periodicity = an.return_habit_periodicity(user, habit_name)
    habit = HabitDB(habit_name, habit_periodicity, user, user.database)
    return habit


def delete_habit(user):
    habit = identify_habit("delete", user)
    if habit.delete_habit():
        print(f"The habit \"{habit.name}\" with the periodicity \"{habit.periodicity}\" was successfully deleted.")


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


def return_past_days(no_days):
    return str(datetime.date.today() - datetime.timedelta(days=no_days))


def check_now():
    return qu.confirm("Did you complete your habit just now?", default=True).ask()


def input_past_check_date():
    # es werden nur die letzten Tage zur Auswahl angeboten
    return qu.select("When did you complete your habit?",
                     choices=[f"today", f"yesterday", return_past_days(2), return_past_days(3),
                              return_past_days(4), return_past_days(5)]).ask()


def check_off_habit(user):
    habit = identify_habit("check off", user)
    if check_now():
        habit.check_off_habit()
        print("Habit successfully completed (today).")
    else:
        check_day = input_past_check_date()
        if check_day == "today":
            manual_date = datetime.date.today()
        elif check_day == "yesterday":
            manual_date = return_past_days(1)
        else:
            manual_date = check_day
        check_date = (" ".join([str(manual_date), "12:00:00"]))  # es wird einfach die Mittagszeit genommen
        habit.check_off_habit(check_date)
        print(f"Habit successfully completed ({check_day}).")


def analyze_habits(user):
    # Funktion brauche ich meiner Meinung nach nicht zu testen
    type_of_analysis = qu.select("Do you want to analyse all habits or just one?",
                                 choices=["All habits", "Just one"]).ask()
    if type_of_analysis == "All habits":
        print(user.analyze_habits())
    else:  # type_of_analysis == "Just one"
        habit = identify_habit("analyze", user)
        print(habit.analyze_habit())


def test_data_existing(database):
    """
    checks if the test data has already been entered or not
    :return:
    """
    return db.user_data_existing(database)


def manage_habits(user):
    manage_action = qu.select("What do you want to do with your habits?",
                              choices=["Create habit", "Delete habit", "Modify habit"]).ask()
    if manage_action == "Create habit":
        create_habit(user)
    elif manage_action == "Delete habit":
        delete_habit(user)
    else:  # manage_action == "Modify habit"
        modify_habit(user)


def inspect_habits(user):
    user_periodicities = an.return_ordered_periodicites(user)
    periodicity = qu.select("Which habits do you want to look at?",
                            choices=["All habits"] + [(x + " habits only") for x in user_periodicities]).ask()
    if periodicity == "All habits":
        print(user.return_habit_information())
    else:
        print(user.return_habits_of_type(periodicity.replace(" habits only", "")))


def determine_possible_actions(user):  # tested
    actions = {
        "no habits": ["Create habit", "Exit"],
        "habit without data": ["Manage habits", "Look at habits", "Check off habit", "Exit"],
        "habit with data": ["Manage habits", "Look at habits", "Check off habit", "Analyze habits", "Exit"]
    }  # um Fehler zu vermeiden, stehen User nur die Handlungen zur Verfügung, die sie ausführen können
    habits = an.return_habits_only(user)
    habit_data_existing = an.check_for_habit_data(user)
    if len(habits) == 0:
        category = "no habits"
    elif not habit_data_existing:
        category = "habit without data"
    else:
        category = "habit with data"
    return actions[category]


def cli():
    main_database = get_db()  # TODO: hier Verbindung zur Datenbank checken, sonst einen Fehler ausgeben
    if not db.user_data_existing(main_database):  # creates test data only if no other data is existing
        test_data.DataCli("main.db")
    # TODO: wäre es vielleicht nicht doch besser, auf eine separate Testdatenbank zurückzugreifen, wo bei jedem
    #  Neustart die ursprünglichen Daten wieder enthalten sind?
    # TODO: Generelle Information: Wie bekomme ich Hilfe? Wie beende ich das Programm?
    # TODO: Handle Python KeyboardInterrupt

    # Program Flow
    current_user = start(main_database)
    counter = 0
    while True:
        counter += 1  # zur Verbesserung der Usability
        possible_actions = determine_possible_actions(current_user)
        if counter > 1:
            qu.text("Press \"enter\" to proceed to the main menu.").ask()
        next_action = qu.select("What do you want to do next?", choices=possible_actions).ask()
        if next_action == "Create habit":
            create_habit(current_user)
        elif next_action == "Manage habits":
            manage_habits(current_user)
        elif next_action == "Look at habits":
            inspect_habits(current_user)
        elif next_action == "Check off habit":
            check_off_habit(current_user)
        elif next_action == "Analyze habits":
            analyze_habits(current_user)
        else:  # next_action == "Exit"
            print("See you later, Bye!")
            break

    #  TODO: Help-Funktion implementieren und damit Streak, Break und sowas erklären?
    #   (geht möglicherweise bei der Enter Frage, indem man help eingibt)


if __name__ == "__main__":
    cli()
