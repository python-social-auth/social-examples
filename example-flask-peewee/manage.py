#!/usr/bin/env python
from example import app, database
from flask_script import Manager, Server, Shell

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=lambda: {"app": app}))


@manager.command
def syncdb():
    from example.models.user import User
    from social_flask_peewee.models import FlaskStorage

    models = [
        User,
        FlaskStorage.user,
        FlaskStorage.nonce,
        FlaskStorage.association,
        FlaskStorage.code,
        FlaskStorage.partial,
    ]
    for model in models:
        model.create_table(True)


if __name__ == "__main__":
    manager.run()
