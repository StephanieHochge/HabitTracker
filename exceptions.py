class UserNameNotExisting(Exception):
    """Raised when user tries to create a user name that is already existing"""

    def __init__(self, username,
                 message="A user with this username does not exist."):
        self.username = username
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class UserHasNoHabits(Exception):
    """Raised when user tries to do something with habits, but does not have any habits yet"""
    def __init__(self, username,
                 message="You do not have any habits yet. To perform this action, you first need to create habits."):
        self.username = username
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
