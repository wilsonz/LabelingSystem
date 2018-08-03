#
# __init__.py
# serves double duty:
# it will contain the application factory(应用工厂),
# and it tells Python that the flaskr dir should be treated as a package

import os
from flask import Flask


###########################################
# this is the application factory function.
# Any configuration, registration, and other setup the application needs
# will happen inside the func, then the application will be returned.
def create_app(test_config=None):
    '''Create and configure an instance of the Flask application.'''
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
        # a default secret that should be overridden by instance config
        # 发布时应当使用一个随机值来重载
        SECRET_KEY='dev',
        # store the database in the instance folder
        # 实例文件夹用于存放本地数据（如配置密匙和数据库），不应当提交到版本控制系统
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # it overrides the default config with values taken from
        # config.py
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

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


    # register the database commands
    from flaskr import db
    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth
    app.register_blueprint(auth.bp)

    from flaskr import blog
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index.
    app.add_url_rule('/', endpoint='index')

    return app
