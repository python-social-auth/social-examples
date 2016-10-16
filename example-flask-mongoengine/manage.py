#!/usr/bin/env python
from flask_script import Server, Manager, Shell
from example import app, db


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db
}))


if __name__ == '__main__':
    manager.run()
