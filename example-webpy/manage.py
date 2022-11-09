import sys

from app import app, engine
from models import Base
from social_webpy.models import SocialBase

if __name__ == "__main__":
    if sys.argv[1] == "syncdb":
        Base.metadata.create_all(engine)
        SocialBase.metadata.create_all(engine)
    else:
        app.run()
