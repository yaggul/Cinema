from cinema_exceptions import *

'''
class to cli order
DBinit instance,
'''

# from init_db import DBinit
# from prettytable import PrettyTable as pt


class CLI():
    def __init__(self, *args):
        self.db = args[0]
        self.commands = {
            'show_movies': self.db.show_movies,
            'show_movie_projections': self.db.show_movie_projections,
            'make_reservations': self.db.make_reservations,
            'exit': self.db.exit,
            'help': self.db.help
}

    def start(self):
        self.db.welcome()
        while True:
            try:
                console_input = input("Enter command > ")
            except KeyboardInterrupt:
                self.db.exit()
            try:
                text = console_input.split(' ')
                command = text[0]
                parameter = text[1:]
                if parameter == []:
                    self.commands[command]()
                else:
                    # print(command, parameter)
                    self.commands[command](parameter)
            except KeyError:
                print('Wrong command. Type "help" for list of supported commands')


