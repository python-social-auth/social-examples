import click
from flask.cli import FlaskGroup
from example import app, db_session, engine


@click.group(cls=FlaskGroup, create_app=lambda: app)
def cli():
    """Management script for the Example Flask Social Login application."""

    @app.shell_context_processor
    def make_shell_context():
        return dict(db_session=db_session)

@app.cli.command()
def syncdb():
    from example.models import user
    from social_flask_sqlalchemy import models

    user.Base.metadata.create_all(engine)
    models.PSABase.metadata.create_all(engine)


if __name__ == '__main__':
    cli()
