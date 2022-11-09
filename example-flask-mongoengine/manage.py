#!/usr/bin/env python
from example import app, db
from flask_script import Manager, Server, Shell

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=lambda: {"app": app, "db": db}))


if __name__ == "__main__":
    manager.run()
