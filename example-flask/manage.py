#!/usr/bin/env python
from flask_script import Server, Manager, Shell
from example import app, db_session, engine


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db_session': db_session
}))


@manager.command
def syncdb():
    from example.models import user
    from social_flask_sqlalchemy import models
    user.Base.metadata.create_all(engine)
    models.PSABase.metadata.create_all(engine)

if __name__ == '__main__':
    manager.run()
