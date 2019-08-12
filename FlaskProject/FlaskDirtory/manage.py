from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
# 猴子模块，将不契合协程的代码变为契合协程代码
from gevent import monkey
monkey.patch_all()

from app import create_app, models

app = create_app()

manage = Manager(app)
migrate = Migrate(app, models)

manage.add_command("db", MigrateCommand)

# 使用pywsgi运行项目，添加runserver_gevent命令
@manage.command
def runserver_gevent():
    from gevent import pywsgi
    server = pywsgi.WSGIServer(("127.0.0.1", 5000), app)
    server.serve_forever()

if __name__ == '__main__':
    manage.run()