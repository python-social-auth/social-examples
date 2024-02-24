#!/usr/bin/env python
from example import app, database
import click
from flask.cli import FlaskGroup


@click.group(cls=FlaskGroup, create_app=lambda: app)
def cli():
    """Management script for the Example Flask Social Login application."""


@app.cli.command()
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


if __name__ == '__main__':
    cli()
