from flask_marshmallow import Marshmallow
from app.models import User, Link, Action

ma = Marshmallow()


class UserObject(ma.ModelSchema):

    class Meta:
        model = User
        additional = ('id', 'email', 'first_name', 'last_name',
                      'messenger_type', 'messenger', 'password_hash', 'is_admin')
        load_only = ('password_hash', )
        exclude = ('links',)


class LinkObject(ma.ModelSchema):

    class Meta:
        model = Link
        fields = ('id', 'name', 'site', 'hash_str', 'date_create', 'user_id')


class ActionObject(ma.ModelSchema):

    class Meta:
        model = Action
