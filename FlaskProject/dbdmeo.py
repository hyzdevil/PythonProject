import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/flask_db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "Demo.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

models = SQLAlchemy(app)

class Student(models.Model):
    __tablename__ = "students"
    id = models.Column(models.Integer, primary_key=True)
    name = models.Column(models.String(32), unique=True)

models.create_all()