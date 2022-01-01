import db


class User:

    def __init__(self, user_name):
        self.__user_name = user_name

    def __set_user_name(self, user_name):
        self.__user_name = user_name

    def __get_user_name(self):
        return self.__user_name

    # Definition der Properties
    user_name = property(__get_user_name, __set_user_name)


class UserDB(User):

    def store_user(self, data_base):
        db.add_user(data_base, self.user_name)
