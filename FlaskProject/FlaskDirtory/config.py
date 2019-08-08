import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/flask_db"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "hyz123"

class DebugConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "student.sqlite")

class OnlineConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "student.sqlite")