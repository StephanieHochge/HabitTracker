class UserNameNotExisting(Exception):
    """Raised when user tries to create a user name that is already existing"""

    def __init__(self, username,
                 message="A user with this user name does not exist."):
        self.username = username
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.username} -> {self.message}'
