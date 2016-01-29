import sqlite3
from prettytable import PrettyTable as pt

from cinema_exceptions import *


class DBinit:
    def __init__(self):
        self.con = sqlite3.connect('/media/kromm/DATA/code/Cinema/cinema.db')
        self.movies_data = []
        self.projections_data = []
        self.reservations_data = []
        self.seats_matrix = []
        self.reservation_user_name = ''
        self.reservation_movie_id = 0
        self.reservation_projection_id = 0
        self.reservation_tickets_count = 0
        self.reservation_tickets = []
        self.reservation = True

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
        tbl_header = ['ID', 'Name', 'Rating']
        tbl = pt(tbl_header)
        tbl.align['Name'] = 'l'
        tbl.align['Rating'] = 'l'
        cur = self.con.cursor()
        cur.execute("select * from movies order by rating desc")
        for i in cur.fetchall():
            tbl.add_row(i)
        print("\nCurrent movies:\n" + str(tbl))

    def show_movie_projections(self, *args):
        '''
        show_movie_projections <movie_id> [<date>]
- print all projections of a given movie for the given date (date is optional).
        '''
        # print(args)
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
            if len(args[0]) == 1:
                cur.execute(movie_id_sql, (int(args[0][0]), ))
                result = cur.fetchall()
                for i in result:
                    tbl.add_row([i[1], ])
                print("\nProjections for movie '{}':\n".format(result[0][0]) + str(tbl))
            else:
                cur.execute(movie_and_date_sql, (int(args[0][0]), args[0][1]))
                result = cur.fetchall()
                for i in result:
                    tbl.add_row([i[2], ])
                print("\nProjections for movie '{}' on date {}:\n".format(
                    result[0][0], result[0][1]) + str(tbl))
        except (IndexError, KeyError, ValueError):
            print('\nWrong command. Type help for list of supported commands \
and parameters')

    def make_reservations(self):
        self.reservation = True
        while self.reservation:
            self.choose_user()
            if not self.reservation:
                break
            self.choose_ticket_count()
            if not self.reservation:
                break
            self.show_movies()
            self.choose_movie_id()
            if not self.reservation:
                break
            print(self.show_movie_projections_and_seats(self.reservation_movie_id))
            self.choose_projection_id()
            if not self.reservation:
                break
            print(self.available_seats())
            self.choose_seats(self.reservation_projection_id)
            if not self.reservation:
                break
            print(self.return_reservation_recap())
            self.finalize_reservation()

    def choose_user(self):
        self.reservation_user_name = ''
        while self.reservation_user_name == '':
            try:
                self.reservation_user_name = input('Step 1 (User): Choose name> ')
                if self.reservation_user_name == 'cancel':
                    raise Cancel
            except Cancel:
                self.clear_reservation_data()
                print("\nReservation canceled. Have a nice day")
                self.reservation = False
                break
            except KeyboardInterrupt:
                self.clear_reservation_data()
                self.con.close()
                print('\n\nBuy, Buy')
                quit()

    def choose_ticket_count(self):
        self.reservation_tickets_count = 0
        while self.reservation_tickets_count == 0:
            try:
                user_input = input(
                    '\nStep 1 (User): Choose number of tickets > ')
                if user_input == 'cancel':
                    raise Cancel
                else:
                    self.reservation_tickets_count = int(user_input)
                    if self.reservation_tickets_count not in range(1, 100):
                        raise OutOfRange
            except Cancel:
                self.clear_reservation_data()
                print("\nReservation canceled. Have a nice day")
                self.reservation = False
                break
            except (ValueError, OutOfRange):
                print('''\nThere are only {0} free tickets. Please enter a
                    number between 1 and 100''')
            except KeyboardInterrupt:
                self.clear_reservation_data()
                self.con.close()
                print('\n\nBuy, Buy')
                quit()

    def choose_movie_id(self):
        self.reservation_movie_id = 0
        m_ids = self.show_movie_ids()
        while self.reservation_movie_id not in m_ids:
            try:
                user_input = input(
                    '\nStep 2 (Movie): Choose a movie> ')
                if user_input == 'cancel':
                    raise Cancel
                else:
                    self.reservation_movie_id = int(user_input)
                    if self.reservation_movie_id not in m_ids:
                        raise OutOfRange
                    else:
                        pass
            except Cancel:
                self.clear_reservation_data()
                print("\nReservation canceled. Have a nice day")
                self.reservation = False
                break
            except (ValueError, OutOfRange):
                print('\nWe need a number between 1 and {}'.format(
                    self.show_movie_ids()[-1] + 1))
            except KeyboardInterrupt:
                self.clear_reservation_data()
                self.con.close()
                print('\n\nBuy, Buy')
                quit()

    def choose_projection_id(self):
        self.reservation_projection_id = 0
        p_ids = self.show_projection_ids(self.reservation_movie_id)
        while self.reservation_projection_id not in p_ids:
            try:
                user_input = input(
                    '\nStep 3 (Projection): Choose a projection> ')
                if user_input == 'cancel':
                    raise Cancel
                else:
                    self.reservation_projection_id = int(user_input)
                    if self.reservation_projection_id not in p_ids:
                        raise OutOfRange
            except Cancel:
                self.clear_reservation_data()
                print("\nReservation canceled. Have a nice day")
                self.reservation = False
                break
            except (ValueError, OutOfRange):
                print('\nAllowed choices {}'.format(p_ids))
            except KeyboardInterrupt:
                self.clear_reservation_data()
                self.con.slose()
                print('\n\nBuy, Buy')
                quit()

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
        return "\nProjections for movie '{}':\n".format(
            result[0][0]) + str(tbl)

    def available_seats(self):
        self.gen_seats_matrix()
        tbl_headers = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        tbl = pt(tbl_headers)
        tbl.align[''] = 'r'
        r_seats = self.return_reserved_seats(self.reservation_projection_id)
        for seat in r_seats:
            self.seats_matrix[seat[0]-1][seat[1]-1] = 'X'
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
        result = cur.fetchall()
        return result

    def show_projection_ids(self, movie_id):
        cur = self.con.cursor()
        cur.execute('select id from projections where movie_id=?', (movie_id, ))
        p_ids = [i[0] for i in cur.fetchall()]
        return p_ids

    def show_movie_ids(self):
        cur = self.con.cursor()
        cur.execute('select id from movies')
        m_ids = [i[0] for i in cur.fetchall()]
        return m_ids

    def choose_seats(self, proj_id):
        r_seats = self.return_reserved_seats(proj_id)
        self.reservation_tickets = []
        t_count = self.reservation_tickets_count
        while t_count > 0:
            try:
                for i in range(1, t_count+1):
                    ticket = input('Step 4 (Seats): Choose seat {}> '.format(i))
                    if ticket == 'cancel':
                        raise Cancel
                    else:
                        ticket = (int(ticket[1:-1].split(',')[0].strip(
                            ' ')), int(ticket[1:-1].split(',')[1].strip(' ')))
                        if ticket[0] not in range(1, 11) or ticket[1] not in range(1, 11):
                            raise OutOfRange
                        elif ticket in self.reservation_tickets:
                            raise EqualTicket
                        else:
                            if ticket in r_seats:
                                raise SeatTaken
                            else:
                                self.reservation_tickets.append(ticket)
                                t_count -= 1
            except Cancel:
                self.clear_reservation_data()
                print("\nReservation canceled. Have a nice day")
                self.reservation = False
                break
            except (ValueError, OutOfRange):
                print('\nPlease insert ticket as rown and column in range 1-10')
            except SeatTaken:
                print('\nThis seat is already taken')
            except EqualTicket:
                self.reservation_tickets = []
                t_count = self.reservation_tickets_count
                print('\nYou have duplicated a previous ticket of yours!!! \n\
Please try again.\n')
            except KeyboardInterrupt:
                self.clear_reservation_data()
                self.con.close()
                print('\n\nBuy, Buy')
                quit()

    def finalize_reservation(self):
        user_actions = ('cancel', 'finalize')
        user_input = ''
        while user_input not in user_actions:
            try:
                user_input = input("\nStep 5 (Confirm - type 'finalize') > ").lower()
                if user_input not in user_actions:
                    raise Finalize
                elif user_input == 'cancel':
                    raise Cancel
                else:
                    self.insert_reservation_data()
                    self.clear_reservation_data()
                    print('Thanks')
                    break
            except Finalize:
                print("\nType 'finalyze' to confirm your reservation or 'cancel' \
                    delete")
            except Cancel:
                self.clear_reservation_data()
                print("\nReservation canceled. Have a nice day")
                self.reservation = False
                break
            except KeyboardInterrupt:
                self.clear_reservation_data()
                self.con.close()
                print('\n\nBuy, Buy')
                quit()

    def return_movie_by_id(self, movie_id):
        cur = self.con.cursor()
        sql = '''SELECT m.name||" "||m.rating FROM movies m WHERE id=?'''
        cur.execute(sql, (movie_id, ))
        result = cur.fetchall()
        return result

    def return_projection_by_id(self, projection_id):
        cur = self.con.cursor()
        sql = '''SELECT p.date||" "||p.time||" "||p.type
        FROM  projections p WHERE id=?'''
        cur.execute(sql, (projection_id, ))
        result = cur.fetchall()
        return result

    def insert_reservation_data(self):
        cur = self.con.cursor()
        sql = '''INSERT INTO reservations (USERNAME, PROJECTION_ID, ROW, COL)
        VALUES (?, ?, ?, ?)'''
        r_data = self.assemble_reservation_data()
        cur.executemany(sql, r_data)
        self.con.commit()

    def assemble_reservation_data(self):
        result = []
        for i in self.reservation_tickets:
            result.append((self.reservation_user_name, self.reservation_projection_id, i[0], i[1]))
        return result

    def clear_reservation_data(self):
        self.reservation_user_name = ''
        self.reservation_movie_id = 0
        self.reservation_tickets_count = 0
        self.reservation_projection_id = 0
        self.reservation_projection_id = 0
        self.reservation_tickets = []
        self.seats_matrix = []

    def return_reservation_recap(self):
        movie = self.return_movie_by_id(self.reservation_movie_id)[0][0]
        projection = self.return_projection_by_id(
            self.reservation_projection_id)[0][0]
        seats = self.reservation_tickets
        return '\nThis is your reservation:\nMovie: {}\nDate and Time: {}\n\
Seats: {}'.format(movie, projection, ','.join([str(seat) for seat in seats]))

    def exit(self):
        self.clear_reservation_data()
        self.con.close()
        print('\n\nBuy, Buy')
        quit()

    def help(self):
        pass
