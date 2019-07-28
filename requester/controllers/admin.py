# -*- coding: utf-8 -*-
from bottle import Bottle, jinja2_view, request, redirect
from requester.utils import validate_input
from requester.models.User import User

admin_app = Bottle()


@admin_app.get('/admin/add_user')
@jinja2_view('admin/users.html')
def users():
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        user = session.get('user')
        users = User.all_users()
        departments = User.all_departments()

        error = session.get('error', "")
        session['error'] = ""

        success = session.get('msg', "")
        session['msg'] = ""

        return {
            'loggedin': loggedin,
            'users': users,
            'departments': departments,
            'user': user,
            'error': error,
            'success': success
        }


@admin_app.post('/admin/add_user')
def add_user():
    # pylint: disable=E1101
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        fname = request.forms.get('fname')
        lname = request.forms.get('lname')
        email = request.forms.get('email')
        phonenumber = request.forms.get('phonenumber')
        password = request.forms.get('password')
        cpassword = request.forms.get('cpassword')
        department = request.forms.get('dept')

        if password != cpassword:
            session['error'] = "Passwords do not match!"
            redirect('/admin/add_user')

        if validate_input(email, r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)") == False:
            session['error'] = "Please enter a valid email address!"
            redirect('/admin/add_user')

        if validate_input(phonenumber, r"^0\d{9}$") == False:
            session['error'] = "Please enter a valid phone number!"
            redirect('/admin/add_user')

        res = User.create_user(fname, lname, email,
                               phonenumber, password, department)

        if res:
            session['msg'] = "User successfully created!"
        else:
            session['error'] = "User not created!"

        redirect('/admin/add_user')


@admin_app.get('/admin/delete_user/<userid:int>')
def delete_user(userid):
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        res = User.delete_user(userid)
        if res:
            session['msg'] = "User successfully deleted!"
        else:
            session['error'] = "Unable to delete user!"

        redirect('/admin/add_user')
