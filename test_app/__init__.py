# if this was not present, the package would not be considered to be a python package, but only in earlier versions
# is automatically run when a module from this package is imported

# from ."module" import * --> now we can just say from package import function
# logging could be initialized here

from .test_analyze import *
from .test_db import *
from .test_habit_user_classes import *
from .test_cli import *
