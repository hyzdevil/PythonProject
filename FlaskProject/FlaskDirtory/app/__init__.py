from flask import Flask
from flask_wtf import CSRFProtect
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

csrf = CSRFProtect()
models = SQLAlchemy()
cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.DebugConfig")

    csrf.init_app(app)
    models.init_app(app)
    cache.init_app(app)

    from .main import main as main_blurprint
    from .apiresourse import api_main
    app.register_blueprint(main_blurprint)
    app.register_blueprint(api_main, url_prefix="/api")

    return app