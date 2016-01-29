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
        self.wrong_message = '''
Wrong command or bad parameter.
Type <help> for list of supported commands and parameters.
        '''
        self.commands = {
            'show_movies': self.db.show_movies,
            'show_movie_projections': self.db.show_movie_projections,
            'make_reservations': self.db.make_reservations,
            'exit': self.db.exit,
            'help': self.db.help
}

    def start(self):
        print(self.db.welcome())
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
                    print(self.commands[command]())
                else:
                    # print(command, parameter)
                    print(self.commands[command](parameter))
            except KeyError:
                print(self.wrong_message)


