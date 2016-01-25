from prettytable import PrettyTable as pt
from init_db import DBinit


def main():
    db = DBinit()
    db.create_tables()

if __name__ == '__main__':
    main()
