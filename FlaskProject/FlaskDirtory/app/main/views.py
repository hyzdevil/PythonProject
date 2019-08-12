import hashlib
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import render_template
from datetime import datetime

from .import main
from app import csrf
from app import cache
from app.models import *
from .forms import TeachersForm,StudentsForm

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

@main.route("/user_vaild/", methods=["GET", "POST"])
def userVail():
    result = {"code":"","msg":""}
    if request.method == "GET":
        username = request.args.get("username")
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                result["code"] = "400"
                result["msg"] = "用户名已存在"
            else:
                result["code"] = "200"
                result["msg"] = ""
        else:
            result["code"] = "400"
            result["msg"] = "用户名不能为空"
    else:
        password = request.form.get("password")
        apassword = request.form.get("apassword")
        if password == apassword:
            result["code"] = "200"
            result["msg"] = ""
        else:
            result["code"] = "400"
            result["msg"] = "两次密码输入不一致"
    return jsonify(result)

def loginVaild(fun):
    def inner(*args, **kwargs):
        c_name = request.cookies.get("username")
        s_name = session.get("username")
        if c_name and s_name:
            if c_name == s_name:
                return fun(*args, **kwargs)
        return redirect("/login/")
    return inner

# @main.route("/", methods=["GET","POST"])
# @main.route("/index/", methods=["GET","POST"])
# @loginVaild
# def index():
#     return render_template("index.html")

@main.route("/add_teacher/", methods=["POST"])
def add_teacher():
    name = request.form.get("name")
    gender = request.form.get("gender")
    birthday = request.form.get("birthday")
    course_id = request.form.get("course_id")
    user_id = request.cookies.get("user_id")
    # print(birthday)
    # print(datetime.strptime(birthday, "%Y-%m-%d").date())
    teacher = Teachers()
    teacher.name = name
    teacher.gender = gender
    teacher.birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
    teacher.course_id = course_id
    teacher.save()
    user = User.query.get(user_id)
    user.identify_id = teacher.id
    user.save()
    return redirect("/user_person/?identify={}".format(user.identify))

@main.route("/", methods=["GET","POST"])
@main.route("/user_person/", methods=["GET","POST"])
@loginVaild
def user_person():
    identify = int(request.args.get("identify"))
    user_id = request.cookies.get("user_id")
    user = User.query.get(user_id)
    if identify == 1:
        result = {"flag":False}
        course = Course.query.all()
        teacher_form = TeachersForm()
        teacher = Teachers.query.get(user.id)
        if teacher:
            result["flag"] = True
        return render_template("teacher_person.html", **locals())
    else:
        result = {"flag": False}
        student_form = StudentsForm()
        student = Students.query.get(user.id)
        if student:
            result["flag"] = True
        return render_template("student_person.html", **locals())

@csrf.exempt
@main.route("/register/", methods=["GET","POST"])
def register():
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identify = form_data.get("identify")
        user = User()
        user.username = username
        user.password = setPassword(password)
        user.identify = int(identify)
        user.save()
        return redirect("/login/")
    return render_template("register.html")

@csrf.exempt
@main.route("/login/", methods=["GET","POST"])
@cache.cached(timeout=50)
def login():
    result = {"error":""}
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identify = int(form_data.get("identify"))
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == setPassword(password):
                    response = redirect("/user_person/?identify={}".format(identify))
                    response.set_cookie("username", username)
                    response.set_cookie("user_id", str(user.id))
                    session["username"] = username
                    return response
                else:
                    result["error"] = "用户名或密码错误"
            else:
                result["error"] = "该用户不存在"
        else:
            result["error"] = "登录信息不能为空"
    return render_template("login.html", **locals())

@main.route("/logout/", methods=["GET","POST"])
def logout():
    response = redirect("/login/")
    for key in request.cookies:
        response.delete_cookie(key)
    del session["username"]
    return response

@main.route("/student/", methods=["GET","POST"])
def student():
    students_list = Students.query.all()
    return render_template("student.html", **locals())

@csrf.exempt
@main.route("/teacher_form/", methods=["GET", "POST"])
def teacher_form():
    teacher_form = TeachersForm()
    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        course = request.form.get("course")
        teacher = Teachers()
        teacher.name = name
        teacher.gender = gender
        teacher.course_id = int(course)
        teacher.save()
        return redirect("/index/")
    return render_template("teacher_form.html", **locals())

@csrf.error_handler
@main.route("/csrf_403/")
def csrf_403(reason):
    return render_template("/csrf_403.html")