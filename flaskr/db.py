#
# Define and Access the DATABASE
#
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    # g:    a special object that is unique for each request.
    #       it is used to store data that might be accessed by multiple funcs
    #       during the request.
    if 'db' not in g:
        # sqlite3.connect():    establishes a connection to the file pointed
        #                       at by the DATABASE configuration key.
        # This file doesn't have to exist yet, and won't until you initialize
        # the database later.
        g.db = sqlite3.connect(
            # current_app:   points to the Flask app handling the request.
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row:    tells the connection to return rows that behave like
        #                 dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db

# close_db():     checks if a connection was created by checking if g.db was set
#                 if the connection exists, it is closed.
def close_db(e=None):
    db = g.app('db', None)

    if db is not None:
        db.close()

# add func that will run these SQL commands
def init_db():
    # get_db():    returns a database connection, which is used to exe the
    #              commands read from the file.
    db = get_db()
    # open_resource():    opens file relative to the flaskr pkg, which is
    #                     useful since u won't necessarily know where that
    #                     location is when deploying the app latter.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# click.command():    defines a command line command called init-db that calls
#                     the init_db func & shows a success msg to the user.
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Cleaer the existing data and current new tables."""
    init_db()
    click.echo('Initialized the database.')



# the close_db() & init_db_command() need to be registered with the app instance
# otherwise they won't be used by the app.
# However, since u'r using a factory func, that instance isn't available when
# writing the func. Instead, write a func that takes an app and does the regist.

def init_app(app):
    # app.teardown_appcontext():    tells Flask to call that func when cleaning
    #                               up after returning the response.
    app.teardown_appcontext(close_db)
    # app.cli.add_command():    adds a new command that can be called with
    #                           the flask command.
    app.cli.add_command(init_db_command)
# import & call this func from the factory.
