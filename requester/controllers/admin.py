# -*- coding: utf-8 -*-
from bottle import Bottle, jinja2_view, request, redirect
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
        print(User.all_users())
