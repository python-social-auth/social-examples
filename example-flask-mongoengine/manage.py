#!/usr/bin/env python
from example import app, db
import click
from flask.cli import FlaskGroup


@click.group(cls=FlaskGroup, create_app=lambda: app)
def cli():
    """Management script for the Example Flask Social Login application."""

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


if __name__ == '__main__':
    cli()
