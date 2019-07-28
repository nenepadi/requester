import sqlite3
from requester.utils import check_password, dict_factory, validate_input, hash_password
from requester import settings


class User:
    @staticmethod
    def create_user(fname, lname, email, phonenumber, password, department):
        hashed_password = hash_password(password)
        data = (fname, lname, email, phonenumber,
                hashed_password, "user", department)

        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    '''INSERT INTO users(fname, lname, email, phonenumber, password, role, department) VALUES(?, ?, ?, ?, ?, ?, ?)''', data)
                con.commit()
                res = True
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res

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
                        user = False
                else:
                    user = False
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            user = False
        finally:
            con.close()
            return user

    @staticmethod
    def all_users():
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                rows = cur.execute(
                    "SELECT t1.*, t2.name AS dept_name FROM users t1 LEFT JOIN departments t2 ON t1.department = t2.deptid").fetchall()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            rows = False
        finally:
            con.close()
            return rows

    @staticmethod
    def delete_user(id):
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                cur = con.cursor()
                res = cur.execute(
                    '''DELETE FROM users WHERE userid = ?''', (id,))
                con.commit()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            res = False
        finally:
            con.close()
            return res

    @staticmethod
    def all_departments():
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                rows = cur.execute("SELECT * FROM departments").fetchall()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            rows = False
        finally:
            con.close()
            return rows

    @staticmethod
    def get_department(id):
        print(id)
        try:
            with sqlite3.connect(settings.DB_FILE) as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                row = cur.execute(
                    '''SELECT * FROM departments WHERE deptid = ?''', (id, )).fetchone()
        except sqlite3.Error as error:
            print("SQL error occured: ", error.args[0])
            row = False
        finally:
            con.close()
            return row
