# A Blueprint is a way to organize a group of related views and other code.
# Rather than registering views and other code directly with an app,
# they are registered with a blueprint.
# Then the blueprint is registered with the app when it is available in
# the factory function.

# Flaskr will have two blueprints
# one for authentication func, and another one for the blog posts func.
#

import functools
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flaskr.db import get_db

# create a Blueprint named 'auth'
# Like the app obj, the blueprint needs to know where it's defined,
# so __name__ is passed as the 2nd arg.
# the url_prefix will be prepended to all the URLs associated with bp.
bp = Blueprint('auth', __name__, url_prefix='/auth')

# the 1st view: register
#
@bp.route('/register'. methods=('GET', 'POST'))
