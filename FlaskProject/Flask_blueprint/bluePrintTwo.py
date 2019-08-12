from flask import Blueprint

simple_blueprint2 = Blueprint("simple_page2", __name__)

@simple_blueprint2.route("/index2/")
def index():
    return "这是index2主页"