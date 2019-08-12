from flask import Blueprint

simple_blueprint1 = Blueprint("simple_page1", __name__)

@simple_blueprint1.route("/index1/")
def index():
    return "这是index1主页"