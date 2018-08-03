# Most of the code will be excuted for each test already,
# so if sth fails the other tests will notice.
# The only behavior that can change is passing test config.
# If config is not passed, there should be some default configuration,
# otherwise the configuration should be overridden.
from flaskr import create_app


def test_config():
    '''Test create_app without passing test config.'''
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
