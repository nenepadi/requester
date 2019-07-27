#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import click
from bottle import static_file, Bottle, run, TEMPLATE_PATH, request
from beaker.middleware import SessionMiddleware

from requester import settings
from requester.routes import Routes
from requester.utils import validate_input, hash_password
import sqlite3


TEMPLATE_PATH.insert(0, settings.TEMPLATE_PATH)
session_opts = {
    'session.type': 'cookie',
    'session.cookie_expires': True,
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.validate_key': True,
    'session.auto': True,
}

app = SessionMiddleware(Bottle(), session_opts)


# Bottle Routes
app.wrap_app.merge(Routes)


@app.wrap_app.route('/assets/<path:path>', name='assets')
def assets(path):
    yield static_file(path, root=settings.STATIC_PATH)


@click.group()
def cmds():
    pass


@cmds.command()
@click.option('--port', default=os.environ.get('PORT', 8080), type=int,
              help=u'Set application server port!')
@click.option('--ip', default='0.0.0.0', type=str,
              help=u'Set application server ip!')
@click.option('--debug', default=False,
              help=u'Set application server debug!')
def runserver(port, ip, debug):
    click.echo('Start server at: {}:{}'.format(ip, port))
    run(app=app, host=ip, port=port, debug=debug, reloader=debug)


@cmds.command()
def test():
    import unittest
    loader = unittest.TestLoader()
    tests = loader.discover('tests')
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)


@cmds.command()
def createadmin():
    fname = input("Firstname: ")
    lname = input("Surname: ")
    email = input("Email: ")
    phonenumber = input("Phone number: ")
    password = input("Password: ")

    if validate_input(email, r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)") == False:
        print("Please enter a valid email address!")
        sys.exit(0)

    if validate_input(phonenumber, r"^0\d{9}$") == False:
        print("Please enter a valid phone number!")
        sys.exit(0)

    hashed_password = hash_password(password)

    data = (fname, lname, email, phonenumber, hashed_password, "admin")
    connection = sqlite3.connect(settings.DB_FILE)
    cursorObj = connection.cursor()

    try:
        cursorObj.execute(
            '''INSERT INTO users(fname, lname, email, phonenumber, password, role) VALUES(?, ?, ?, ?, ?, ?)''', data)
        connection.commit()
        print("Admin user has been successfully created!")
    except sqlite3.Error as error:
        print("An error occured: ", error.args[0])
        sys.exit()

    connection.close()


if __name__ == "__main__":
    cmds()
