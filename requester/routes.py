# -*- coding: utf-8 -*-
from bottle import Bottle

from .controllers.home import home_app
from .controllers.admin import admin_app


Routes = Bottle()
# App to render / (home)
Routes.merge(home_app)
Routes.merge(admin_app)
