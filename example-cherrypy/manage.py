#!/usr/bin/env python
import sys

import cherrypy

from sqlalchemy import create_engine


cherrypy.config.update({
    'SOCIAL_AUTH_USER_MODEL': 'example.db.user.User',
})

from social_cherrypy.models import SocialBase
from example.db import Base
from example.db.user import User

from example.app import run_app, DATABASE_NAME

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'syncdb':
        engine = create_engine(DATABASE_NAME)
        Base.metadata.create_all(engine)
        SocialBase.metadata.create_all(engine)
    else:
        if len(sys.argv) > 1:
            run_app(sys.argv[1])
        else:
            run_app()
