class UserNameNotExisting(Exception):
    """Indicates that a user with the entered user name does not exist.
    Is raised when a user tries to login with a username that is not stored in the database, i.e., unused.

    Attributes:
        username ('str'): the entered username that does not exist
        message ('str'): the error message that can be displayed
    """

    def __init__(self, username):
        self.username = username
        self.message = "A user with this username does not exist."
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
