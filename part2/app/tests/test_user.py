from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')


user_model = api.model('User', {
    'first_name': fields.String(required=True, description='The first name of the user'),
    'last_name': fields.String(required=True, description='The last name of the user'),
    'email': fields.String(required=True, description='The email address of the user'),
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created.')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user
        """
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        else:
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201

    @api.response(200, 'User list retrieved successfully')
    @api.response(404, 'No user found')
    def get(self):
        """
        Get user list
        """
        user_list = facade.get_user_list()
        users = []
        if len(user_list) == 0:
            return {'error': 'No user found'}, 404
        for user in user_list:
            users.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
        return users, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.expect(user_model, validate=True)
    def put(self, user_id):
        """
        Update an existing user
        """
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'Invalid input data'}, 400
        return {'message': 'User details updated successfully'}, 200
