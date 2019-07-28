# -*- coding: utf-8 -*-
from bottle import Bottle, jinja2_view, request, redirect
from requester.models.User import User
from requester.models.Complain import Complain
import calendar
import time

home_app = Bottle()


@home_app.get('/')
@jinja2_view('index.html')
def index():
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin:
        user = session.get('user')
        return {'user': user, 'loggedin': loggedin}
    else:
        return {'loggedin': loggedin}


#### Authentication ####
@home_app.get('/login')
@jinja2_view('auth/login.html')
def login():
    session = request.environ.get('beaker.session')
    return {'error': session.get('error', '')}


@home_app.post('/login')
def authenticate():
    # pylint: disable=E1101
    session = request.environ.get('beaker.session')
    email = request.forms.get('email')
    password = request.forms.get('password')
    user = User.authenticate(email, password)

    if user == False:
        session['error'] = "Username/Password mismatch"
        redirect('/login')

    session['user'] = user
    session['loggedin'] = True
    redirect('/')


@home_app.get('/logout')
def logout():
    session = request.environ.get('beaker.session')
    session.delete()
    redirect('/login')


#### Complain ####
@home_app.get('/complain')
@jinja2_view('complain.html')
def complain():
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        user = session.get('user')
        complains = Complain.get_users_complains(user['userid'])

        error = session.get('error', "")
        session['error'] = ""

        success = session.get('msg', "")
        session['msg'] = ""

        return {
            'user': user,
            'loggedin': loggedin,
            'error': error,
            'success': success,
            'complains': complains
        }


@home_app.post('/make_complain')
def make_complain():
    # pylint: disable=E1101
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        userid = request.forms.get('userid')
        problem_type = request.forms.get('problem')
        description = request.forms.get('description')
        timestamp = calendar.timegm(time.gmtime())

        res = Complain.make_complain(
            userid, problem_type, description, timestamp)

        if res:
            session['msg'] = "Complain successfully submitted!"
        else:
            session['error'] = "Complain couldn't be submitted!"

        redirect('/complain')


@home_app.get('/delete_complain/<complain_id:int>')
def delete_user(complain_id):
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        res = Complain.delete_complain(complain_id)
        if res:
            session['msg'] = "Complain successfully deleted!"
        else:
            session['error'] = "Unable to delete complain!"

        redirect('/complain')


@home_app.get('/mark_solved/<complain_id:int>')
def mark_as_solved(complain_id):
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        res = Complain.mark_as_solved(complain_id)
        if res:
            session['msg'] = "Status changed successfully!"
        else:
            session['error'] = "Error occured!"

        redirect('/complain')


#### Projector Request ####
@home_app.get('/projector')
@jinja2_view('projector.html')
def projector():
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        user = session.get('user')
        return {'user': user, 'loggedin': loggedin}
