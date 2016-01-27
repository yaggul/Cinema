from init_db import DBinit
from cli import CLI

def main():
    db = DBinit()
    db.create_tables()
    print(db.show_movies())
    print(db.show_movie_projections())
    # con = sqlite3.connect('/media/kromm/DATA/code/Cinema/cinema.db')
    # cur = con.cursor()
    # cur.execute('select name,rating from movies order by rating')
    # a = cur.fetchall()
    # print(a)
if __name__ == '__main__':
    main()
