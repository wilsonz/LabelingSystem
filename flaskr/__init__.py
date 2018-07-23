#
# __init__.py
# serves double duty:
# it will contain the application factory,
# and it tells Python that the flaskr dir should be treated as a package

import os
from flask import Flask

# this is the application factory function.
def create_app(test_config=None):
    # create & configure the app
    # __name__  the name of current py module. it is a convenient
    #           way to tell app where it's located to set up path
    # instance_relative_config=True
    #           it tells app that configuration files are relative
    #           to the instance folder.
    app = Flask(__name__, instance_relative_config=True)

    # this func sets some default config that app will use:
    # SECRET_KEY:   used by Flask and extensions to keep data safe
    # DATABASE:     the path where the SQLite database file saved
    #               it's under app.instance_path, which is the
    #               path that Flask has chosen for instance folder
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # it overrides the default config with values taken from
        # config.py
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        # this func ensures that app.instance_path exists.
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says Hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    # new added
    from . import db
    db.init_app(app)



    return app
