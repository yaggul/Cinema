from init_db import DBinit
from cli import CLI


def main():
    db = DBinit()
    console = CLI(db)
    console.start()

if __name__ == '__main__':
    main()
