from flask import Flask
from flask import jsonify, make_response
from werkzeug.exceptions import InternalServerError
from flask_restful import Resource, Api
from common.auth import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
from resources.members import MembersList, MembersItem


app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
app.config['SECRET_KEY'] = 'super-secret-development-key'


errors={
    'InternalServerError': {
    'status': 500,
    'message': 'Internal Server Error'
	},
	'AuthError': {
		'status': 401,
		'message': 'Authentication error'
	},
}

jwt = JWT(app, authenticate, identity)
api = Api(app, errors=errors)

api.add_resource(MembersList,"/members")
api.add_resource(MembersItem, '/members/<int:id>')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def health_check():
    """entry point/app health checker.

    Returns:
        str: 'ok'
    """
    return 'ok'


# Dashboard
@app.route('/dashboard')
@jwt_required()
def dashboard():
    """Welcome page.

    Authentication Required

    Returns:
        dict: success message along with username

    Raises:
        AuthError: An error occured when un authenticated user access.
    """
    return make_response(jsonify({'message': 'Welcome Mr. {} to REST API App.'.format(current_identity)}), 200)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)