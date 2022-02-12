"""This module contains the habit tracker's functionalities necessary to control the user flow and to
expose the user to the command line interface.

Examples of the most important functionalities include functions to
    - create a new user
    - login
    - manage habits (create, delete or modify)
    - inspect habits
    - complete habits
    - analyze habits
"""

import db
from habit import HabitDB
from user import UserDB
import analyze as ana
import questionary as qu
from validators import HabitNameValidator, UserNameValidator
from exceptions import UserNameNotExisting
import test_data
import datetime


# Some input commands are outsourced to facilitate testing of the cli
def input_start_action():
    """ask the user what s/he wants to do after starting the app"""
    return qu.select("What do you want to do?", choices=["Login", "Create new user", "Exit"]).ask()


def input_username(database, action):
    """ask the user to input either a new (creating a new user) or an already existing username.

    :param database: the database, in which user data shall be/is already stored (type: sqlite3 connection)
    :param action: the action, the user wants to undergo (either "create new user" or "loing") (type: str)
    :return: the new/already existing username
    """
    text = "Please choose a username: " if action == "create" else "Please enter your username: "
    username = qu.text(text, validate=UserNameValidator(database, action)).ask()
    return username


def input_new_habit(user):
    """ask the user to specify a new habit (name and periodicity).

    :param user: the user who wants to create a new habit (type: user.Userdb object)
    :return: a tuple containg the name and the periodicity of the new habit (type: tuple)
    """
    habit_name = qu.text("Which habit do you want to create?", validate=HabitNameValidator(user)).ask()
    periodicity = input_periodicity(habit_name.strip())  # strip: to delete leading und ending spaces
    return habit_name.strip(), periodicity


def input_periodicity(habit_name):
    """ask the user to specify the periodicity of a habit.

    :param habit_name: the name of the habit (type: str)
    :return: the selected periodicity (type: str)
    """
    periodicity = qu.select(f"Which periodicity shall \"{habit_name}\" have?",
                            choices=["daily", "weekly", "monthly", "yearly"]).ask()
    return periodicity


def input_new_habit_name(user):
    """ask the user to input a new name.

    :param user: the user who wants to modify the habit name (type: user.UserDB object)
    :return: the new name (type: str)
    """
    new_name = qu.text("Please enter a new name: ", validate=HabitNameValidator(user)).ask()
    return new_name


def input_habit_modify_target():
    """ask the user to input what part of the habit he wants to modify.

    :return: the modification target (type: str)
    """
    target = qu.select("What part of the habit do you want to modify?", choices=["name", "periodicity", "both"]).ask()
    return target


def input_chosen_habit(habit_action, tracked_habits):
    """ask the user to select a habit from the list of tracked habits.

    :param habit_action: the action the user wants to perform with the habit, e.g. delete or check off,  (type: str)
    :param tracked_habits: a list of the users tracked habits (type: str)
    :return: the habit name the user chose (type: str)
    """
    habit_name = qu.select(f"Which habit do you want to {habit_action}?", choices=tracked_habits).ask()
    return habit_name


def confirm_delete(habit_name):
    """ask the user for confirmation to perform the deletion of a habit and all its data.

    :param habit_name: the name of the habit to be deleted (type: str)
    :return: True if the user confirms the deletion, False if not (type: bool)
    """
    return qu.confirm(f"Are you sure that you want to delete \"{habit_name}\" and all corresponding data?",
                      default=False).ask()


def return_past_days(no_days):
    """return the date of the day that is no_days away from the current date.

    :param no_days: the number of days to be substracted from the current date (type: int)
    :return: the date of the day that is no_days
    """
    return str(datetime.date.today() - datetime.timedelta(days=no_days))


def input_check_day():
    """ask the user to specify the checkoff date and time by selecting one of the options presented.

    :return: the selected checkoff date (type: str)
    """
    return qu.select("When did you complete your habit?",
                     choices=[f"just now", f"earlier today", f"yesterday", return_past_days(2), return_past_days(3),
                              return_past_days(4), return_past_days(5)]).ask()


# Functions to perform the main functionalities of the habit tracker
def create_new_user(database):
    """create a new user based on user input data and store the user in the specified sqlite3 database connection.

    :param database: the database in which the user is to be stored (type: sqlite3 connection)
    :return: the newly created and stored user (type: user.UserDB object)
    """
    username = input_username(database, "create")
    new_user = UserDB(username, database)
    new_user.store_user()
    print(f"A user with the username {username} has successfully been created. Logged in as {username}.")
    return new_user


def login(database):
    """ask for a username and check whether the username exists in the database. If it does, return the corresponding
    user. It the login fails three times, return to the start menu.

    :param database: The database, in which the user is stored (type: sqlite3 connection)
    :return: The user (type: user.UserDB object) if the username exists in the database, else False.
    """
    count = 0
    while True:
        if count == 3:  # after entering an incorrect username thrice, return to the start menu
            print("\x1b[0;0;41m" +
                  "Login failed three times. Do you perhaps want to perform another action?"
                  + "\x1b[0m")  # add red highlight to the text
            return False
        try:
            username = input_username(database, "login")
            user = UserDB(username, database)
            if not ana.check_for_username(user):  # check if a user with the entered name exists in the database
                raise UserNameNotExisting(user.username)
        except UserNameNotExisting as e:
            print("\x1b[0;0;41m" + str(e) + "\x1b[0m")
            count += 1
            if count < 3:
                print("\x1b[0;0;41m" + "Please try again." + "\x1b[0m")
        else:
            print(f"Logged in as {username}")
            return user


def start(database):
    """Ask the user what he wants to do. Depending on his choice, either let the user log in to the app, create a new
    user, or quit the application.

    :param database: The database, in which the users are to be stored (type: sqlite3 connection)
    :return: the current user (type: user.UserDB instance), if the user logged in successfully or successfully
    created a new user
    """
    start_action = input_start_action()
    if start_action == "Exit":
        print("See you later, Bye!")
        quit()
    else:
        current_user = login(database) if start_action == "Login" else create_new_user(database)
        return current_user if current_user else start(database)  # if the login was unsuccessful, the introductory
        # question is asked again and the user has the ability to choose a different action
    # TODO: @Chris: diese Funktion hab ich jetzt nicht getestet (ich wüsste nicht wie), ist das in Ordnung?


def create_habit(user):
    """create a new habit by asking the user for a (valid) habit name and a periodicity.

    :param user: the user who wants to create a new habit (type: user.UserDB)
    :return: the newly created habit (type: habit.HabitDB instance)
    """
    habit_name, periodicity = input_new_habit(user)
    habit = HabitDB(habit_name, periodicity, user)
    habit.store_habit()
    print(f"The habit \"{habit_name}\" with the periodicity \"{periodicity}\" was created.")
    return habit


def identify_habit(habit_action, user):
    """present a list of all habits the user defined and let the user choose one of these habits.

    :param habit_action: the action which is to be done with the habit (e.g., "delete", †ype: str)
    :param user: the user whose habits are displayed (type: user.UserDB)
    :return: the habit which the user chose (type: habit.HabitDB)
    """
    habit_name = input_chosen_habit(habit_action, user.defined_habits)
    return [habit for habit in user.defined_habits if habit.name == habit_name][0]


def delete_habit(user):
    """ask which habit the user wants to delete, ask for confirmation and then delete the habit and its corresponding
     data if the user confirms that the habit should be deleted.

    :param user: the user who wants to delete a habit and its corresponding data (type: user.UserDB)
    """
    habit = identify_habit("delete", user)
    if confirm_delete(habit.name):
        habit.delete_habit()
        print(f"The habit \"{habit.name}\" with the periodicity \"{habit.periodicity}\" was successfully deleted.")


def modify_habit(user):
    """ask which habit the user wants to modify and for the modification target (name, periodicity, or both), then
    let the user modify the target and save the modification in the database.

    :param user: the user who wants to modify a habit (type: user.UserDB)
    """
    habit = identify_habit("modify", user)
    target = input_habit_modify_target()
    if target in ("name", "both"):
        print(f"The habit's old name is {habit.name}.")
        new_name = input_new_habit_name(user)
        habit.modify_habit(name=new_name)
        print(f"The habit's name was successfully changed to {habit.name}.")
    if target in ("periodicity", "both"):
        print(f"The habit's old periodicity is {habit.periodicity}.")
        new_periodicity = input_periodicity(habit.name)
        habit.modify_habit(periodicity=new_periodicity)
        print(f"The habit's periodicity was successfully changed to {habit.periodicity}.")
        # TODO: @Chris: sehr schlimm, dass die beiden if-Teile so gleich sind?


def check_off_habit(user):
    """ask which habit the user wants to check off, then ask for the check date and store a completion for the
    selected habit and the selected check date.

    :param user: the user who wants to check off the habit (type: user.UserDB)
    """
    habit = identify_habit("check off", user)
    check_day = input_check_day()
    if check_day == "just now":
        check_date = None
    elif check_day == "earlier today":
        now = datetime.datetime.now()
        check_time = str(f"{now.hour - 2}:00:00") if now.hour > 2 else str(f"01:00:00")  # two hours are subtracted
        # unless the habit was completed before 3 am
        check_date = (" ".join([str(now.date()), check_time]))
    else:
        manual_date = return_past_days(1) if check_day == "yesterday" else check_day
        check_date = (" ".join([str(manual_date), "12:00:00"]))  # 12 pm is chosen as time
    habit.check_off_habit(check_date)
    print(f"Habit successfully completed ({check_day}).")


def analyze_habits(user):
    """ask the user which habit s/he wants to analyse or if s/he wants to analyze all habits and then display
    the requested analysis.

    :param user: the user who wants to analyze habit(s) (type: user.UserDB)
    """
    habit_names = [habit.name for habit in user.completed_habits]  # only completed habits can be analyzed
    habit_to_analyze = qu.select("Which habit(s) do you want to analyze?", choices=["All habits"] + habit_names).ask()
    if habit_to_analyze == "All habits":
        habit_comparison, analysis = user.analyze_habits()
        print(f"""Summary statistics:
        {analysis.to_string(index=False)}
        A detailed comparison of all habits:
        {habit_comparison}""")
    else:
        habit = [habit for habit in user.completed_habits if habit.name == habit_to_analyze][0]
        data = habit.analyze_habit()
        print(ana.present_habit_analysis(data, habit.name))


def manage_habits(user):
    """ask the user what kind of habit management they want to perform, and then start the desired process.

    :param user: the user who wants to manage a habit (type: user.UserDB)
    """
    manage_action = qu.select("What do you want to do with your habits?",
                              choices=["Create habit", "Delete habit", "Modify habit"]).ask()
    if manage_action == "Create habit":
        create_habit(user)
    elif manage_action == "Delete habit":
        delete_habit(user)
    else:  # manage_action == "Modify habit"
        modify_habit(user)


def inspect_habits(user):
    """ask the user which habit(s) they want to inspect and then display information about the requested habits.

    :param user: the user who wants to inspect the habits (type: user.UserDB)
    """
    user_periodicities = ana.return_ordered_periodicities(user)
    view_habits = qu.select("Which habits do you want to look at?",
                            choices=["all habits"] + [(x + " habits only") for x in user_periodicities]).ask()
    periodicity = None if view_habits == "all habits" else view_habits.replace(" habits only", "")
    habit_information = user.return_habit_information(periodicity)
    print(habit_information.to_string(index=False))


def determine_possible_actions(user):
    """determine the actions which a user can perform, depending on whether s/he has already created habits or not
    and whether the habits have already been completed.

    :param user: the user for which the possible actions are to be determined (type: user.UserDB)
    :return: the possible actions of the user (type: list)
    """
    actions = {
        "no habits": ["Create habit", "Exit"],
        "no completed habits": ["Manage habits", "Look at habits", "Check off habit", "Exit"],
        "completed habits": ["Manage habits", "Look at habits", "Check off habit", "Analyze habits", "Exit"]
    }  # to avoid exceptions at runtime, only the actions that users can perform are available to them
    if len(user.defined_habits) == 0:
        category = "no habits"
    elif not user.completed_habits:
        category = "no completed habits"
    else:
        category = "completed habits"
    return actions[category]


def cli():
    """expose the user to the CLI"""
    main_database = db.get_db("main.db")
    if not db.check_for_user_data(main_database):  # create test data only if no other data is existing
        test_data.DataForTestingCLI("main.db")

    current_user = start(main_database)
    counter = 0
    while True:
        counter += 1  # to improve usability
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


if __name__ == "__main__":
    cli()


### für jede Funktion, die ich testen wollte, existiert mind. 1 Test hier
# alle Funktionen werden verwendet
