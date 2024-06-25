from cherrypy.process import plugins
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class SAEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus, connection_string=None):
        self.sa_engine = None
        self.connection_string = connection_string
        self.session = Session(autoflush=True, autocommit=False)
        super().__init__(bus)

    def start(self):
        self.sa_engine = create_engine(self.connection_string, echo=False)
        self.bus.subscribe("bind-session", self.bind)
        self.bus.subscribe("commit-session", self.commit)

    def stop(self):
        self.bus.unsubscribe("bind-session", self.bind)
        self.bus.unsubscribe("commit-session", self.commit)
        if self.sa_engine:
            self.sa_engine.dispose()
            self.sa_engine = None

    def bind(self):
        self.session.bind = self.sa_engine
        return self.session

    def commit(self):
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()
