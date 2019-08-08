from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.DebugConfig")

models = SQLAlchemy(app)