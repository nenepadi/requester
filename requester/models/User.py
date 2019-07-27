import sqlite3
from requester.utils import check_password, dict_factory
from requester import settings


class User:
    @staticmethod
    def create(data):
        pass

    @staticmethod
    def authenticate(email, password):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                row = cur.execute(
                    '''SELECT * FROM users WHERE email = :email''', {'email': email}).fetchone()

                if row:
                    check = check_password(row['password'], password)
                    if check:
                        user = {
                            'userid': row['userid'],
                            'fname': row['fname'],
                            'lname': row['lname'],
                            'email': row['email'],
                            'phonenumber': row['phonenumber'],
                            'role': row['role']
                        }
                    else:
                        return False
                else:
                    return False
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            return False
        finally:
            con.close()
            return user

    @staticmethod
    def all_users():
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                rows = cur.execute("SELECT * FROM users").fetchall()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            return False
        finally:
            con.close()
            return rows
