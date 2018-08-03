import pytest
from flask import g, session
from flaskr.db import get_db

def test_register(client, app):
    # test that viewing the page renders without template errors.
    # /client.get()/    makes a GET request and returns the
    # Response object returned by Flask.
    # To test that the page renders successfully, a simple request is made
    # and checked for a 200 OK /status_code/.
    # If rendering failed, Flask would return code /500 Internal Server Error/
    assert client.get('/auth/register').status_code == 200
    # /client.post()/    makes a POST request, converting the data dict
    # into form data.

    # test that successful registration redirects to the login page.
    response = client.post(
                    '/auth/register',
                    data={'username': 'a', 'password': 'a'}
    )
    # /headers/    will have a /Location/ header with the login URL when
    # the register view redirects to the login view.
    assert 'http://localhost/auth/login' == response.headers['Location']

    # test that the user was inserted into the database
    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None

# /pytest.mark.parametrize()/   tells Pytest to run the same test func
# with different arguments.
@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required.'),
        ('a', '', b'Password is required.'),
        ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # test that viewing the page renders without template errors
    assert client.get('/auth/login').status_code == 200

    # test that successful login redirects to the index page
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


# Testing /client/ in a /with/ block allows accesing context variables such
# as /session/ after the reponse is returned.
# Normally, accessing /session/ outside of a request would raise an error.

# Testing /logout/ is the opposite of /login/.
# /session/ should not contain /user_id/ after logging out.
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
