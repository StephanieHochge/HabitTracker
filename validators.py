from questionary import Validator, ValidationError, prompt
from user import UserDB
import re
import analyze as an


# Questionary validators
class UserNameValidator(Validator):  # Code from Questionary documentation
    def __init__(self, database, action_type="login"):
        self.database = database
        self.action_type = action_type

    def validate(self, document):
        user = UserDB(document.text, self.database)
        user_existing = an.check_for_user(user)
        if len(document.text) == 0:  # mindestens ein Zeichen muss eingegeben werden
            raise ValidationError(
                message="Please enter at least one character.",  # error message that is displayed
                cursor_position=len(document.text),  # TODO: die zwei Zeilen in Funktion packen?
            )
        elif re.search("[ &@!]", document.text) is not None:  # darf keine Sonder- oder Leerzeichen enthalten
            raise ValidationError(
                message="Username must not contain spaces or '&', '@', or '!'",
                cursor_position=len(document.text),
            )
        elif user_existing and self.action_type == "create":  # User Name schon in der Datenbank vorhanden?
            # ist aber nur relevant, wenn man einen neuen User anlegt
            raise ValidationError(
                message="Username already existing. Please choose another one.",
                cursor_position=len(document.text),
            )


class HabitNameValidator(Validator):

    def __init__(self, user):
        self.database = user.database
        self.user = user

    def validate(self, document):
        habits_of_user = an.return_habit_names(self.user)
        if len(document.text.strip()) == 0:  # Habit enthält kein Zeichen oder nur Leerzeichen
            raise ValidationError(
                message="Please enter at least one character that is not a space.",  # error message that is displayed
                cursor_position=len(document.text),
            )
        elif document.text in habits_of_user:  # Habit wird schon von dem Nutzer genutzt?
            raise ValidationError(
                message="Habit already existing. Please choose another name.",
                cursor_position=len(document.text),
            )


