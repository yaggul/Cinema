import sqlite3
from prettytable import PrettyTable as pt


class OutOfRange(Exception):
    pass


class DBinit:
    def __init__(self):
        self.con = sqlite3.connect('/media/kromm/DATA/code/Cinema/cinema.db')
        # self.con.cursor = cur
        self.movies_data = []
        self.projections_data = []
        self.reservations_data = []
        self.seats_matrix = []
        self.seats_string = ''
        self.reservation_user_name = ''
        self.reservation_movie_id = ''
        self.reservation_projection_id = ''
        self.reservation_tickets_count = 0
        self.reservation_tickets = []

    def create_tables(self):
        cur = self.con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS MOVIES (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME VARCHAR(255) NOT NULL,
RATING DOUBLE NOT NULL)
''')
        cur.execute('''CREATE TABLE IF NOT EXISTS PROJECTIONS (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
MOVIE_ID INT NOT NULL,
TYPE VARCHAR(5) NOT NULL,
DATE VARCHAR(10) NOT NULL,
TIME VARCHAR(8) NOT NULL,
FOREIGN KEY (MOVIE_ID) REFERENCES MOVIES (ID))
''')
        cur.execute('''CREATE TABLE IF NOT EXISTS RESERVATIONS (
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

    def show_movies(self):
        '''
        print all movies ORDERED BY rating desc
        '''
        movies_header = ['ID', 'Name', 'Rating']
        tbl = pt(movies_header)
        tbl.align['Name'] = 'l'
        tbl.align['Rating'] = 'l'
        cur = self.con.cursor()
        cur.execute("select * from movies order by rating desc")
        for i in cur.fetchall():
            tbl.add_row(i)
        return "Current movies:\n" + str(tbl)

    def show_movie_projections(self, **kwargs):
        '''
        show_movie_projections <movie_id> [<date>]
- print all projections of a given movie for the given date (date is optional).
        '''
        tbl_headers = ['Projection_ifno']
        tbl = pt(tbl_headers)
        tbl.align['Projection_ifno'] = 'l'
        cur = self.con.cursor()
        movie_id_sql = '''SELECT m.name, "["||p.id||"] - "||p.date||" "||
            p.time||" ("||p.type||")" as p_info from movies m left join
            projections p on (m.id = p.movie_id) where m.id=?'''
        movie_and_date_sql = '''SELECT m.name, p.date, "["||p.id||"] - "||
            p.time||" ("||p.type||")" as p_info from movies m left join
            projections p on (m.id = p.movie_id) where m.id=? and p.date =?'''
        try:
            if kwargs['date'] is None:
                cur.execute(movie_id_sql, (kwargs['movie_id'],))
                result = cur.fetchall()
                for i in result:
                    tbl.add_row([i[1], ])
                return "Projections for movie '{}':\n".format(result[0][0]) + str(tbl)
            else:
                cur.execute(movie_and_date_sql, (kwargs['movie_id'], kwargs['date']))
                result = cur.fetchall()
                for i in result:
                    tbl.add_row([i[2], ])
                return "Projections for movie '{}' on date {}:\n".format(
                    result[0][0], result[0][1]) + str(tbl)
        except (IndexError, KeyError):
            return 'Wrong command. Type help for list of supported commands \
and parameters'

    def make_reservations(self):
        pass

    def choose_user(self):
        self.reservation_user_name = ''
        while self.reservation_user_name == '':
            self.reservation_user_name = input('Step 1 (User): Choose name> ')

    def choose_ticket_count(self):
        self.reservation_tickets = 0
        while self.reservation_tickets == 0:
            try:
                self.reservation_tickets = int(input(
                    'Step 1 (User): Choose number of tickets > '))
                if self.reservation_tickets not in range(0, 101):
                    raise OutOfRange
            except (ValueError, OutOfRange):
                print('You have entered invalid number. Range (1-100)')

        def choose_movie_id(self):
            self.reservation_movie_id = 0
            while self.reservation_movie_id == 0:
                try:
                    self.reservation_movie_id == int(input(
                        'Step 2 (Movie): Choose a movie> '))
                    if self.reservation_movie_id not in self.show_movie_ids():
                        raise OutOfRange
                except (ValueError, OutOfRange):
                    print('We need a number between 1 and {}'.format(
                        self.show_movie_ids()[-1]))

        def choose_projection_id(self):
            self.reservation_projection_id = ''
            print(self.show_movies())
            while self.reservation_projection_id == 0:
                try:
                    self.reservation_projection_id == int(input(
                        'Step 3 (Projection): Choose a projection> '))
                    if self.reservation_projection_id not in self.show_projection_ids():
                        raise OutOfRange
                except (ValueError, OutOfRange):
                    print('Allowed choice {}'.format(
                        self.show_projection_ids()))

    def show_movie_projections_and_seats(self, movie_id):
        tbl_headers = ['Projection info']
        tbl = pt(tbl_headers)
        tbl.align['Projection info'] = 'l'
        cur = self.con.cursor()
        sql = '''SELECT m.name, "["||p.id||"] - "||p.date||" "||
            p.time||" ("||p.type||")"||" - "||(100 - COUNT(R.PROJECTION_ID))||
            ' available seats' as p_info
            from movies m
            left join projections p
            on (m.id = p.movie_id)
            left join reservations r
            on (p.id = r.projection_id)
            group by m.name, p.id, p.date, p.time, r.projection_id
            having m.id = ?'''
        cur.execute(sql, (movie_id, ))
        result = cur.fetchall()
        for i in result:
            tbl.add_row([i[1]])
        return "Projections for movie '{}':\n".format(
            result[0][0]) + str(tbl)

    def available_seats(self):
        tbl_headers = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        tbl = pt(tbl_headers)
        row_num = [1]
        for i in self.seats_matrix:
            tbl.add_row(row_num + i)
            row_num[0] += 1
        return str(tbl)

    def gen_seats_matrix(self):
        for i in range(10):
            self.seats_matrix.append(['.' for i in range(10)])

    def return_reserved_seats(self, proj_id):
        cur = self.con.cursor()
        sql = '''SELECT r.row, r.col as r_seats
        from reservations r
        where projection_id=?
        '''
        cur.execute(sql, (proj_id, ))
        r_seats = cur.fetchall()
        for seat in r_seats:
            self.seats_matrix[seat[0]][seat[1]] = 'X'

    def show_projection_ids(self, movie_id):
        cur = self.con.cursor()
        cur.execute('select projection_id from projections where movie_id=?', (movie_id, ))
        p_ids = [i[0] for i in cur.fetchall()]
        return p_ids

    def show_movie_ids(self):
        cur = self.con.cursor()
        cur.execute('select id fom movies')
        m_ids = [i[0] for i in cur.fetchall()]
        return m_ids

    def choose_seats(self, proj_id):
        cur = self.con.cursor()
        sql = '''SELECT r.row, r.col as r_seats
        from reservations r
        where projection_id=?
        '''
        cur.execute(sql, (proj_id, ))
        r_seats = cur.fetchall()
        self.reservation_tickets_count = 0
        self.reservation_tickets = []
        while self.reservation_tickets_count == 0:
            try:
                self.reservation_tickets_count = int(input("Step 4 (Seats): Choose ticket count> "))
                tc = 100 - len(r_seats)
                if self.reservation_tickets_count > tc:
                    raise OutOfRange
            except (ValueError, OutOfRange):
                print('''There are only {0} free tickets. Please enter a
                    number between 1 and {0}'''.format(tc))
        t_count = self.reservation_tickets_count
        while t_count > 0:
            try:
                for i in range(1, t_count+1):
                    ticket = input('Step 4 (Seats): Choose seat {}> '.format(i))
                    if ticket[0] not in range(1, 11) or ticket[1] not in range(1, 11):
                        raise OutOfRange
                    else:
                        self.reservation_tickets.append(ticket)
            except (ValueError, OutOfRange):
                print('Please insert ticket as rown and column in range 1-10')


    def cancel_reservation(self):
        pass

    def exit(self):
        pass

    def help(self):
        pass
