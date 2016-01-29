from init_db import DBinit
from cli import CLI


def main():
    dbase = DBinit()
    console = CLI(dbase)
    console.start()

if __name__ == '__main__':
    main()
