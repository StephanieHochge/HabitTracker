from questionary import Validator, ValidationError
from user import UserDB
import re
import analyze as an


# Questionary validators
class UserNameValidator(Validator):
    """This class is used to validate if an entered username meets the requirements either for creating
    a new user or for logging in. It inherits methods and attributes from the questionary's Validator class.

    Attributes:
        database (sqlite3.connection): the database in which the username is (to be) stored
        action_type ('str'): the action that is to be done with the entered username, either "login" (looging into
                            the application) or "create" (creating a new user)
    """
    def __init__(self, database, action_type: str = "login"):
        self.database = database
        self.action_type = action_type

    def validate(self, document):
        """validate if the entered username meets the requirements:
                - usernames must contain at least one character
                - usernames must not contain spaces or '&', '@', or '!'
                - usernames must be unique (the same username cannot be used by different users)

        :param document: the user's input ('Document')

        raise:
            a validation error in case the currently entered username does not meet all requirements.
            The user can then make a new entry/modify his entry.
        """
        user = UserDB(document.text, self.database)
        user_existing = an.check_for_username(user)
        if len(document.text) == 0:  # at least one character has to be entered
            raise ValidationError(
                message="Please enter at least one character.",
                cursor_position=len(document.text),
            )
        elif re.search("[ &@!]", document.text) is not None:  # must not contain spaces or '&', '@', or '!'
            raise ValidationError(
                message="Username must not contain spaces or '&', '@', or '!'",
                cursor_position=len(document.text),
            )
        elif user_existing and self.action_type == "create":  # when creating a new user, the username must
            # not be in use yet
            raise ValidationError(
                message="Username already existing. Please choose another one.",
                cursor_position=len(document.text),
            )


class HabitNameValidator(Validator):
    """This class is used to validate if an entered habit name meets the requirements for habit names when
    creating new habits.

        Attributes:
            database (sqlite3.connection): the database in which the username is (to be) stored
            user ('user.UserDB'): the user who wants to create a new habit with the entered name
        """

    def __init__(self, user):
        self.database = user.database
        self.user = user

    def validate(self, document):
        """validate if the entered username meets the requirements:
                - habit names must contain at least one character that is not a space
                - a user's habit names must be unique (i.e, a user cannot create two habits with
                  the same name, but two different users can)

        :param document: the user's input ('Document')

        raise:
            a validation error in case the currently entered habit name does not meet all requirements.
            The user can then make a new entry/modify his entry.
            """
        if len(document.text.strip()) == 0:  # Habit must contain at least one character that is not a space
            raise ValidationError(
                message="Please enter at least one character that is not a space.",
                cursor_position=len(document.text),
            )
        elif document.text in self.user.habit_names:  # The user must not already have a habit with the same name
            raise ValidationError(
                message="Habit already existing. Please choose another name.",
                cursor_position=len(document.text),
            )


