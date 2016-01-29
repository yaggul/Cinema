from cinema_exceptions import *

'''
class to cli order
DBinit instance,
'''

# from init_db import DBinit
# from prettytable import PrettyTable as pt


class CLI():
    def __init__(self, *args):
        self.commands = {
            'show_movies': args[0].show_movies,
            'show_movie_projections': args[0].show_movie_projections,
            'make_reservations': args[0].make_reservations,
            'exit': args[0].exit,
            'help': args[0].help
}

    def start(self):
        while True:
            console_input = input("Enter command > ")
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
            except KeyboardInterrupt:
                print('\n\nBuy, Buy')
                quit()


