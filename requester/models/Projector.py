import sqlite3
from requester.utils import dict_factory
from requester import settings
import datetime


class Projector:
    @staticmethod
    def make_request(userid, start_time, end_time, purpose):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO projector_request(userid, start_datetime, end_datetime, purpose) VALUES(?, ?, ?, ?)''',
                            (userid, start_time, end_time, purpose))
                con.commit()
                res = True
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res

    @staticmethod
    def get_users_requests(userid):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                rows = cur.execute(
                    '''SELECT * FROM projector_request WHERE userid = ? AND deleted = 0''', (userid,)).fetchall()

                for row in rows:
                    row['start_readable'] = datetime.datetime.fromtimestamp(
                        row['start_datetime']).strftime("%Y-%m-%d %H:%M:%S")

                    row['end_readable'] = datetime.datetime.fromtimestamp(
                        row['end_datetime']).strftime("%Y-%m-%d %H:%M:%S")
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            rows = False
        finally:
            con.close()
            return rows

    @staticmethod
    def all_requests():
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                rows = cur.execute(
                    '''SELECT t1.*, t2.fname || t2.lname `requester` FROM projector_request t1 JOIN users t2 ON t1.userid=t2.userid WHERE t1.deleted = 0''').fetchall()

                for row in rows:
                    row['start_readable'] = datetime.datetime.fromtimestamp(
                        row['start_datetime']).strftime("%Y-%m-%d %H:%M:%S")

                    row['end_readable'] = datetime.datetime.fromtimestamp(
                        row['end_datetime']).strftime("%Y-%m-%d %H:%M:%S")
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            rows = False
        finally:
            con.close()
            return rows

    @staticmethod
    def delete_request(id):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                res = cur.execute(
                    '''UPDATE projector_request SET deleted = ? WHERE request_id = ?''', (1, id,))
                con.commit()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res

    @staticmethod
    def approve_request(id):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                res = cur.execute(
                    '''UPDATE projector_request SET status = 1 WHERE request_id = ? AND deleted = 0''', (id,))
                con.commit()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res
