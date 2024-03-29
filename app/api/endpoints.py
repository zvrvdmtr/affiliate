from flask import Blueprint, request
from app.models import User, Link, Action
from app import db
from app.api.serializer import UserObject, LinkObject, ActionObject
from flask_restful import Api, Resource
from app.schema_validate.schema_validator import validate_data
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def validate_user_decorator(func):
    def wrapper(*args, **kwargs):
        if kwargs['user_id'] != get_jwt_identity()['id']:
            return 'Forbidden', 403
        return func(*args, **kwargs)
    return wrapper


def validate_admin_decorator(func):
    def wrapper(*args, **kwargs):
        if get_jwt_identity()['is_admin'] is not True:
            return 'Forbidden', 403
        return func(*args, **kwargs)
    return wrapper


class UserAuthentication(Resource):

    def post(self):
        user_obj = UserObject()
        credentials = request.get_json()
        result = validate_data(credentials, 'auth.json')
        if result:
            return result, 400
        user = User.query.filter_by(email=credentials['email']).first()
        if not user or not user.check_password(credentials['password']):
            return 'There is no such user', 400
        token = create_access_token(identity=user_obj.dump(user))
        return token


class UserRegistration(Resource):

    def post(self):
        data = request.get_json()
        result = validate_data(data, 'user.json')
        if result:
            return result, 400
        if User.query.filter_by(email=data['email']).first():
            return 'Email already used!', 400
        user_obj = UserObject()
        user = user_obj.make_instance(data)
        user.set_password(user.password_hash)
        db.session.add(user)
        db.session.commit()
        return user_obj.dump(user), 200


class UsersList(Resource):

    @jwt_required
    @validate_admin_decorator
    def get(self):
        user = User.query.all()
        user_obj = UserObject()
        return user_obj.dump(user, many=True), 200


class UserDetail(Resource):

    @jwt_required
    @validate_user_decorator
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        user_obj = UserObject()
        return user_obj.dump(user), 200

    @jwt_required
    @validate_user_decorator
    def put(self, user_id):
        data = request.get_json()
        user_obj = UserObject()
        user = user_obj.load(data=data, instance=User.query.get_or_404(user_id), partial=True)
        db.session.commit()
        return user_obj.dump(user), 201


class LinksList(Resource):

    @jwt_required
    @validate_user_decorator
    def get(self, user_id):
        links = Link.query.filter_by(user_id=user_id)
        link_obj = LinkObject()
        return link_obj.dump(links, many=True), 200

    @jwt_required
    @validate_user_decorator
    def post(self, user_id):
        data = request.get_json()
        if 'site' not in data or 'name' not in data:
            return 'Site and link name must be define', 400
        link_obj = LinkObject()
        link = link_obj.make_instance(data=data)
        link.generate_hash()
        link.user_id = user_id
        db.session.add(link)
        db.session.commit()
        return link_obj.dump(link), 200


class LinkDetail(Resource):

    @jwt_required
    def get(self, link_id):
        link = Link.query.get(link_id)
        if link.user_id != get_jwt_identity()['id']:
            return 'Forbidden', 403
        link_obj = LinkObject()
        return link_obj.dump(link)


class ActionsList(Resource):

    def get(self, link_id):
        actions = Action.query.filter_by(link_id=link_id).all()
        action_obj = ActionObject()
        return action_obj.dump(actions, many=True)


class PostBack(Resource):

    def post(self, link_hash):
        link = Link.query.filter_by(hash_str=link_hash).first()
        if not link:
            return 'Not found', 404
        data = request.args.to_dict()
        action_obj = ActionObject()
        action = Action(
            link_id=link.id,
            ip_address=data.get('subid1'),
            user_agent=data.get('subid2'),
            type_id=data.get('subid3'),
            purchase_amount=data.get('subid4'),
        )
        db.session.add(action)
        db.session.commit()
        return action_obj.dump(action)


api.add_resource(UserAuthentication, '/auth')
api.add_resource(UserRegistration, '/register')
api.add_resource(UsersList, '/users')
api.add_resource(UserDetail, '/users/<int:user_id>')
api.add_resource(LinksList, '/users/<int:user_id>/links')
api.add_resource(LinkDetail, '/links/<int:link_id>')
api.add_resource(ActionsList, '/links/<int:link_id>/actions')
api.add_resource(PostBack, '/postback/<string:link_hash>', methods=['post'])
