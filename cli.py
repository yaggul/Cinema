'''
class to cli order
DBinit instance,
'''

from init_db import DBinit
from prettytable import PrettyTable as pt


class CLI(DBinit):
    def __init__(self, *args):
        self.commands = []
