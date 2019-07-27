import re
import hashlib
import uuid


def validate_input(text, regex):
    output = re.search(regex, text)
    if output == None:
        return False
    else:
        return True


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.md5(salt.encode() + password.encode()).hexdigest() + ":" + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(":")
    return password == hashlib.md5(salt.encode() + user_password.encode()).hexdigest()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
