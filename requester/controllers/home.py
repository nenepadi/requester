# -*- coding: utf-8 -*-
from bottle import Bottle, jinja2_view, request, redirect
from requester.models.User import User
from requester.models.Complain import Complain
from requester.models.Projector import Projector
import calendar
import time
from datetime import datetime

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
def delete_complain(complain_id):
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
        requests = Projector.get_users_requests(user['userid'])

        error = session.get('error', "")
        session['error'] = ""

        success = session.get('msg', "")
        session['msg'] = ""

        return {
            'user': user,
            'loggedin': loggedin,
            'error': error,
            'success': success,
            'requests': requests
        }


@home_app.post('/make_request')
def make_request():
    # pylint: disable=E1101
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        start_date = request.forms.get('start_date')
        start_time = request.forms.get('start_time')
        end_date = request.forms.get('end_date')
        end_time = request.forms.get('end_time')
        purpose = request.forms.get('purpose')
        userid = request.forms.get('userid')

        start_datetime = int(time.mktime(datetime.strptime(
            start_date + " " + start_time, "%Y-%m-%d %H:%M").timetuple()))

        end_datetime = int(time.mktime(datetime.strptime(
            end_date + " " + end_time, "%Y-%m-%d %H:%M").timetuple()))

        res = Projector.make_request(
            userid, start_datetime, end_datetime, purpose)

        if res:
            session['msg'] = "Projector requested successfully!"
        else:
            session['error'] = "Error occured!"

        redirect('/projector')


@home_app.get('/delete_request/<request_id:int>')
def delete_request(request_id):
    session = request.environ.get('beaker.session')
    loggedin = 'loggedin' in session
    if loggedin == False:
        redirect('/login')
    else:
        res = Projector.delete_request(request_id)
        if res:
            session['msg'] = "Request successfully deleted!"
        else:
            session['error'] = "Unable to delete request!"

        redirect('/projector')
