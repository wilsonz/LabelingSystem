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
# @bp.route:    associates the URL/register with the register view func.
#               when Flask receives a request to /auth/register, it will
#               call the register view & use the return value as the response
#
@bp.route('/register'. methods=('GET', 'POST'))
def register():
    # request.method:   start validating the input if the uesr submitted form.
    if request.method == 'POST':
        # request.form:    a special type of dict mapping keys & values.
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # db.execute():    takes a SQL query with ? placeholders for user input
        # fetchone:    returns one row from the query. return None if no result
        # later, fetchall() is used to return a list of all results.
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # generate_password_hash():    securely hash the pw and then stored.
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            # db.commit():     to save the change.
            db.commit()
            # url_for():   generates the URL for the login view based on name.
            # redirect():   generates a redirect response to the generated URL.
            return redirect(url_for('auth.login'))

        # flash():  stores msg that can be retrieved when rendering the template
        flash(error)

    # render_template():    render a template containing the HTML.
    return render_template('auth/register.html')


# same pattern as the register() view above
#
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        # check_password_hash():    hashes the submitted password in the same
        #                           way as the stored hash and securely
        #                           compares them.
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is a dict that stores data across requests.
            # When validation succeeds, the user's id is stored in
            # a new session.
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


    # Now that the uesr's id is stored in the session
    # bp.before_app_request():    registers a func that runs before the view
    #                             func, no matter what URL is requested.
    @bp.before_app_request
    # load_logged_in_user():    checks if a user is stored in the session and
    #                           gets that user's data from the database,
    #                           storing it on g.user, which lasts for the
    #                           length of the request.
    def load_logged_in_user():
        user_id = session.get('user_id')

    # if there's no user id, or if the id doesn't exist, g.user will be None
        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECTE * FROM user WHERE id = ?', (user_id,)
            ).fetchone()


# To log out, u need to remove the uesr id from the session.
# Then load_logged_in_user won't load a user on subsequent requests.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Creating, editing, and deleting blog posts will require a user to be logged
# in. A decorator can be used to check this for each view it's applied to.
def login_required(view):
    
