from init_db import DBinit
from cli import CLI

def main():
    db = DBinit()
    db.create_tables()
    db.make_reservations()
    print(db.assemble_reservation_data())
    db.insert_reservation_data()


if __name__ == '__main__':
    main()
