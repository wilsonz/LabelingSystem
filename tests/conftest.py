#
# The app fixture will call the factory and pass /test_config/ to configure
# the application and database for testing instead of using ur local
# development configuration.
import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    '''Create and configure a new app instance for each test.'''
    # create a temporary file to isolate the databse for each test.
    # tempfile.mkstemp():   creates and opens a temporary file, returning
    #                       the file object and the path to it.
    db_fd, db_path = tempfile.mkstemp()
    # /DATABASE/ path:     is overridden so it points to this temporary path
    #                      instead of the instance folder.
    # /TESTING/    tells Flask that the app is in test mode.

    # create the app with common test config
    app = create_app({'TESTING': True, 'DATABASE': db_path, })

    # create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary databse
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
# The /client/ fixture calls /app.test_client()/ with the app objext
# created by the app fixture
def client(app):
    '''A test client for the app.'''
    return app.test_client()

# The /runner/ fixture creates a runner that can call the Click commands
# registered with the application.
@pytest.fixture
def runner(app):
    '''A test runner for the app's Click commands.'''
    return app.test_cli_runner()


# For most of the views, a user needs to be logged in.
# The easiest way to do this in tests is to make a POST request
# to the login view with the client.
# Rather than writting that out every time, we can write a class with
# methods to do that, and use a fixture to pass it the client for each test.
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
                    '/auth/login',
                    data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
