import sqlite3


class DBinit:
    def __init__(self):
        self.con = sqlite3.connect('/media/kromm/DATA/code/Cinema/cinema.db')
        self.cur = self.con.cursor()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXIST MOVIES (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME VARCHAR(255) NOT NULL,
RATING DOUBLE NOT NULL)
''')
        self.cur.execute('''CREATE TABLE IF NOT EXIST PROJECTIONS (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
MOVIE_ID INT NOT NULL,
TYPE VARCHAR(5) NOT NULL,
DATE VARCHAR(10) NOT NULL,
TIME VARCHAR(8) NOT NULL,
FOREIGN KEY (MOVIE_ID) REFERENCES MOVIES (ID))
''')
        self.cur.execute('''CREATE TABLE IF NOT EXIST RESERVATIONS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME VARCHAR(255) NOT NULL,
            PROJECTION_ID INT NOT NULL,
            ROW INT NOT NULL,
            COL INT NOT NULL,
            FOREIGN KEY (PROJECTION_ID) REFERENCES PROJECTIONS (ID))
            ''')
        self.con.commit()

    def import_data_to_tables(self):
        pass
