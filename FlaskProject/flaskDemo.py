from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world"

@app.route("/student/", methods=["GET","POST"])
def student():
    students_list = [
        {"name":"张三","gender":"男","age":"15"},
        {"name":"李四","gender":"男","age":"18"},
        {"name":"王五","gender":"男","age":"24"},
        {"name":"如花","gender":"女","age":"29"},
    ]
    return render_template("student.html", **locals())

if __name__ == '__main__':
    app.run()