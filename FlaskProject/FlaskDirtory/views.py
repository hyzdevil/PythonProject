import hashlib
from flask import request
from flask import render_template,redirect

from FlaskDirtory.main import app,session
from FlaskDirtory.models import *

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

def loginVaild(fun):
    def inner(*args, **kwargs):
        c_name = request.cookies.get("username")
        user_id = request.cookies.get("user_id")
        s_name = session.get("username")
        if c_name and user_id and s_name:
            if c_name == s_name:
                return fun(*args, **kwargs)
        return redirect("/login/")
    return inner

@app.route("/", methods=["GET","POST"])
@app.route("/index/", methods=["GET","POST"])
@loginVaild
def index():
    return render_template("index.html")

@app.route("/register/", methods=["GET","POST"])
def register():
    result = {"error":""}
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identify = form_data.get("identify")
        if username and password and identify:
            user = User()
            user.username = username
            user.password = setPassword(password)
            user.identify = int(identify)
            user.save()
            return redirect("/login/")
        else:
            result["error"] = "注册信息不能为空"
    return render_template("register.html", **locals())

@app.route("/login/", methods=["GET","POST"])
def login():
    result = {"error": ""}
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == setPassword(password):
                    response = redirect("/index/")
                    response.set_cookie("username", username)
                    response.set_cookie("user_id", str(user.id))
                    session["username"] = username
                    return response
                else:
                    result["error"] = "用户名或密码错误"
            else:
                result["error"] = "用户名不存在"
        else:
            result["error"] = "登录信息不能为空"
    return render_template("login.html", **locals())

@app.route("/logout/", methods=["GET","POST"])
def logout():
    response = redirect("/login/")
    for key in request.cookies:
        response.delete_cookie(key)
    del session["username"]
    return response

@app.route("/student/", methods=["GET","POST"])
def student():
    students_list = Students.query.all()
    return render_template("student.html", **locals())