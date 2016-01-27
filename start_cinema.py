from init_db import DBinit
from cli import CLI

def main():
    db = DBinit()
    db.create_tables()
    print(db.show_movies())
    print(db.show_movie_projections())
    print(db.show_movie_projections_and_seats(2))
    db.gen_seats_matrix()
    db.get_reserved_seats(3)
    print(db.available_seats())

if __name__ == '__main__':
    main()
