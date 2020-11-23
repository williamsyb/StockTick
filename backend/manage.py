from app import create_app, db
from app.models import User
from flask_script import Manager, Shell
from flask_script.commands import Server, ShowUrls

app = create_app()
manager = Manager(app)

manager.add_command('url', ShowUrls())

manager.add_command('server', Server(
    host=app.config.get('HOST', 'localhost'),
    port=app.config.get('PORT', 7002)
))


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))


"""
python manager.py shell
user = User(username="admin")
user.set_password("123456")
db.session.add(user)
db.session.commit()
"""
if __name__ == '__main__':
    manager.run()
