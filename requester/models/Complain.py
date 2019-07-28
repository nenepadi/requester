import sqlite3
from requester.utils import dict_factory
from requester import settings
import datetime


class Complain:
    @staticmethod
    def make_complain(userid, complain_type, desc, timestamp):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO complains(userid, complain_type, complain_desc, timestamp) VALUES(?, ?, ?, ?)''',
                            (userid, complain_type, desc, timestamp))
                con.commit()
                res = True
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res

    @staticmethod
    def get_users_complains(userid):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                rows = cur.execute(
                    '''SELECT t1.*, t2.fname || t2.lname as `assignee` FROM complains t1 LEFT JOIN users t2 ON t1.assignee = t2.userid WHERE t1.userid = ? AND t1.deleted = 0 AND is_solved = 0''', (userid,)).fetchall()

                for row in rows:
                    row['time_readable'] = datetime.datetime.fromtimestamp(
                        row['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            rows = False
        finally:
            con.close()
            return rows

    @staticmethod
    def all_complains(status):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                rows = cur.execute(
                    '''SELECT t1.*, t2.fname || t2.lname `complainer`, t3.fname || t3.lname `assignee` FROM complains t1 JOIN users t2 ON t1.userid=t2.userid LEFT JOIN users t3 ON t1.assignee=t3.userid WHERE t1.deleted = 0 AND t1.is_solved = ? ORDER BY t1.timestamp''', (status,)).fetchall()

                for row in rows:
                    row['time_readable'] = datetime.datetime.fromtimestamp(
                        row['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            rows = False
        finally:
            con.close()
            return rows

    @staticmethod
    def delete_complain(id):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                res = cur.execute(
                    '''UPDATE complains SET deleted = ? WHERE complain_id = ?''', (1, id,))
                con.commit()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res

    @staticmethod
    def set_assignee(id, assignee):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                res = cur.execute(
                    '''UPDATE complains SET assignee = ? WHERE complain_id = ? AND deleted = 0''', (assignee, id,))
                con.commit()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res

    @staticmethod
    def mark_as_solved(id):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                res = cur.execute(
                    '''UPDATE complains SET is_solved = 1 WHERE complain_id = ? AND deleted = 0''', (id,))
                con.commit()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res
