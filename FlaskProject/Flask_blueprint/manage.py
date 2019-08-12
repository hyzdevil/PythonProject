from flask import Flask
from flask_script import Manager

from Flask_blueprint.bluePrintOne import simple_blueprint1
from Flask_blueprint.bluePrintTwo import simple_blueprint2

app = Flask(__name__)
app.register_blueprint(simple_blueprint1)
app.register_blueprint(simple_blueprint2)
# manage = Manager(app)
if __name__ == '__main__':
    app.run()