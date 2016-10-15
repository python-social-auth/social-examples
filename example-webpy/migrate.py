from social_webpy.models import SocialBase

from app import engine
from models import Base


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    SocialBase.metadata.create_all(engine)
