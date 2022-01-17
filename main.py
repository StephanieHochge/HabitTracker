from db import get_db, add_user, add_period, add_habit
from habit import HabitDB
from user import UserDB
import analyze as an
import questionary as qu
from questionary import Validator, ValidationError, prompt
import re
from Exceptions import UserNameNotExisting


# Questionary validators - TODO: besseren Ort für Validator-Klassen suchen
class UserNameValidator(Validator):  # Code from Questionary documentation
    def __init__(self, database, action_type="login"):
        self.database = database
        self.action_type = action_type

    def validate(self, document):
        user = UserDB(document.text)
        user_existing = an.check_for_user(self.database, user)
        if len(document.text) == 0:  # mindestens ein Zeichen muss eingegeben werden
            raise ValidationError(
                message="Please enter at least one character",  # error message that is displayed
                cursor_position=len(document.text),  # TODO: die zwei Zeilen in Funktion packen?
            )
        elif re.search("[ &@!]", document.text) is not None:  # darf keine Sonder- oder Leerzeichen enthalten
            raise ValidationError(
                message="User name must not contain spaces or '&', '@', or '!'",
                cursor_position=len(document.text),
            )

        elif user_existing and self.action_type == "create":  # User Name schon in der Datenbank vorhanden?
            # ist aber nur relevant, wenn man einen neuen User anlegt
            raise ValidationError(
                message="User name already existing. Please try another one.",
                cursor_position=len(document.text),
            )


class HabitNameValidator(Validator):

    def __init__(self, database, user):
        self.database = database
        self.user = user

    def validate(self, document):
        habits_of_user = an.return_habits(self.database, self.user)
        if len(document.text) == 0:  # TODO: Vererbung!
            raise ValidationError(
                message="Please enter at least one character",  # error message that is displayed
                cursor_position=len(document.text),
            )
        elif document.text in habits_of_user:  # Habit wird schon von dem Nutzer genutzt?
            raise ValidationError(
                message="Habit already existing. Please choose another name.",
                cursor_position=len(document.text),
            )


def input_username(database):
    username = qu.text("Please choose a user name: ",
                       validate=UserNameValidator(database, "create")).ask()
    return username


def create_new_user(database):
    username = input_username(database)
    app_user = UserDB(username)
    app_user.store_user()
    print(f"A user with the username {username} has successfully been created. Logged in as {username}.")
    return app_user


def login(database):
    username_existing = False
    count = 0
    while not username_existing:
        try:
            username = qu.text("Please enter your user name.",
                               validate=UserNameValidator(database, "login")).ask()
            user = UserDB(username)
            if not an.check_for_user(database, user):
                raise UserNameNotExisting(user.username)
            print(f"Logged in as {username}")
            username_existing = True
            return user
        except UserNameNotExisting:
            print("This user does not exist. Please try again")
            count += 1
            # TODO: nach zwei Fehlversuchen, sich einzuloggen, fragen, ob man neuen User anlegen oder gehen möchte
            # TODO: Was tun, wenn man den eigenen Nutzernamen vergessen hat? Liste an Nutzernamen anzeigen? Pech?


def create_habit(user, database):
    habit_name = qu.text("Which habit do you want to add?",
                         validate=HabitNameValidator(database, user)).ask()
    periodicity = qu.select(f"Which periodicity shall {habit_name} have?",
                            choices=["daily", "weekly", "monthly", "yearly"]).ask()
    habit = HabitDB(habit_name, periodicity, user)
    habit.store_habit(database)
    print(f"The habit \"{habit_name}\" with the periodicity \"{periodicity}\" was created.")
    return habit


def identify_habit(habit_action, database, user):
    tracked_habits = an.return_habits(database, user)
    habit_name = qu.select(f"Which habit do you want to {habit_action}?",
                           choices=tracked_habits).ask()
    habit_periodicity = an.return_periodicity(database, user, habit_name)
    # user.username und habit_name könnte auch nur mit dem Argument "habit" übergeben werden
    habit = HabitDB(habit_name, habit_periodicity, user)
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
    add_period(teeth_rb)
    add_period(teeth_sh, "2021-12-01")
    add_period(teeth_sh, "2021-12-01")
    add_period(teeth_sh, "2021-12-02")
    add_period(teeth_sh, "2021-12-04")
    add_period(teeth_sh, "2021-12-05")
    add_period(teeth_sh, "2021-12-07")
    add_period(teeth_sh, "2021-12-08")
    add_period(teeth_sh, "2021-12-09")
    add_period(teeth_sh, "2021-12-10")
    add_period(teeth_sh, "2021-12-11")
    add_period(teeth_sh, "2021-12-12")
    add_period(teeth_sh, "2021-12-13")
    add_period(teeth_sh, "2021-12-14")
    add_period(teeth_sh, "2021-12-15")
    add_period(teeth_sh, "2021-12-16")
    add_period(teeth_sh, "2021-12-17")
    add_period(teeth_sh, "2021-12-18")
    add_period(teeth_sh, "2021-12-19")
    add_period(teeth_sh, "2021-12-20")
    add_period(teeth_sh, "2021-12-21")
    add_period(teeth_sh, "2021-12-22")
    add_period(teeth_sh, "2021-12-23")
    add_period(teeth_sh, "2021-12-24")
    add_period(teeth_sh, "2021-12-25")
    add_period(teeth_sh, "2021-12-26")
    add_period(teeth_sh, "2021-12-27")
    add_period(teeth_sh, "2021-12-29")
    add_period(teeth_sh, "2021-12-30")
    add_period(teeth_sh, "2021-12-31")
    add_period(dance_sh, "2021-11-06")
    add_period(dance_sh, "2021-11-07")
    add_period(dance_sh, "2021-11-11")
    add_period(dance_sh, "2021-11-13")
    add_period(dance_sh, "2021-11-14")
    add_period(dance_sh, "2021-11-21")
    add_period(dance_sh, "2021-11-25")
    add_period(dance_sh, "2021-11-27")
    add_period(dance_sh, "2021-11-28")
    add_period(dance_sh, "2021-12-02")
    add_period(dance_sh, "2021-12-04")
    add_period(dance_sh, "2021-12-05")
    add_period(dance_sh, "2021-12-16")
    add_period(dance_sh, "2021-12-18")
    add_period(dance_sh, "2021-12-19")
    add_period(dance_sh, "2021-12-30")
    add_period(bathroom_sh, "2021-11-06")
    add_period(bathroom_sh, "2021-11-13")
    add_period(bathroom_sh, "2021-11-20")
    add_period(bathroom_sh, "2021-12-04")
    add_period(bathroom_sh, "2021-12-11")
    add_period(bathroom_sh, "2021-12-18")
    add_period(bathroom_sh, "2022-01-01")
    add_period(windows_sh, "2022-11-17")
    add_period(windows_sh, "2022-12-30")
    add_period(dentist_sh, "2022-12-17")
    add_period(dentist_sh, "2021-12-05")
    add_period(teeth_sh, "2021-12-03")
    add_period(dance_sh, "2021-12-21")

    # TODO: Generelle Information: Wie bekomme ich Hilfe? Wie beende ich das Programm?
    # TODO: Handle Python KeyboardInterrupt

    # Program Flow
    start_action = qu.select(
        "What do you want to do?",
        choices=["Create new user", "Login", "Exit"]
    ).ask()
    if start_action == "Create new user":
        current_user = create_new_user(main_database)
    elif start_action == "Login":
        current_user = login(main_database)
    else:
        print("Bye")
        quit()  # ist das hier gute Praxis?

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


if __name__ == "__main__":
    cli()
