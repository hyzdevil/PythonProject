from flask import Flask
from flask_script import Manager

# from Flask_blueprint.bluePrintOne import simple_blueprint1
# from Flask_blueprint.bluePrintTwo import simple_blueprint2
from bluePrintOne import simple_blueprint1
from bluePrintTwo import simple_blueprint2

app = Flask(__name__)
app.register_blueprint(simple_blueprint1)
app.register_blueprint(simple_blueprint2)
manage = Manager(app)

@manage.command
def hello(name = "createsuperuser"):
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    sure_password = input("Please enter your password again: ")
    email = input("Please enter your email: ")
    return "欢迎注册"

if __name__ == '__main__':
    manage.run()