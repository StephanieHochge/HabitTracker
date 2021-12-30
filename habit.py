class Habit:
    def __init__(self, name, periodicity, user):
        self.__name = name
        self.__periodicity = periodicity
        self.__user = user

    # Setter # TODO: Entscheidung: braucht man Setter auch für User?
    def __setName(self, name):
        self.__name = name

    def __setPeriodicity(self, periodicity):
        self.__periodicity = periodicity

    # Getter
    def __getName(self):
        return self.__name

    def __getPeriodicity(self):
        return self.__periodicity

    def __getUser(self):
        return self.__user

    # Definition der Properties
    name = property(__getName, __setName)
    periodicity = property(__getPeriodicity, __setPeriodicity)
    user = property(__getUser)

    def checkOffHabit(self):
        # TODO: Methode "checkOffHabit" schreiben
        pass

# TODO: def __str__(self) Funktion noch in die Habit-Klasse einbauen
