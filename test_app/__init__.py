"""This package contains test classes to test the habit tracker's main functionalities using pytest.

The test classes include classes to test the application's main functionalities provided by
    - the analysis module (test_analyze.py)
    - the command line interface (test_cli.py)
    - the database module (test_db.py)
    - the HabitDB (habit.py) and UserDB (user.py) classes (user.py, habit.py)
"""

from .test_analyze import *
from .test_db import *
from .test_habit_user_classes import *
from .test_cli import *
