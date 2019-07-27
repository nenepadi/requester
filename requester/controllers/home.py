# -*- coding: utf-8 -*-
from bottle import Bottle, jinja2_view, request, redirect
from requester.models.User import User

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
        return {'user': user, 'loggedin': loggedin}


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
