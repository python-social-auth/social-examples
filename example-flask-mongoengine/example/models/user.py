from mongoengine import StringField, EmailField, BooleanField, ListField, ReferenceField

from flask_login import UserMixin

from social_flask_mongoengine.models import FlaskStorage

from example import db


class User(db.Document, UserMixin):
    username = StringField(max_length=200)
    password = StringField(max_length=200, default='')
    name = StringField(max_length=100)
    email = EmailField()
    active = BooleanField(default=True)

    @property
    def social_auth(self):
        return FlaskStorage.user.objects(user=self)

    def is_active(self):
        return self.active
