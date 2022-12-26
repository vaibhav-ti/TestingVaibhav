import imp
from multiprocessing.spawn import import_main_path
from .base import *

if DEBUG == True:
    from .dev import *
else:
    from .prod import *