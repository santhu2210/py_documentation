from flask import request, jsonify, session, _request_ctx_stack,json
from functools import wraps
from werkzeug.security import safe_str_cmp


class User(object):
    """Class to Create login users.

    Attributes:
        id: user id.
        username: username.
        password: password.
    """
    def __init__(self, id, username, password):
        """Inits User management class."""
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        """return default name."""
        return self.username

users = [
    User(1, 'admin', 'admin@123'),
    User(2, 'devuser', 'user@123'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)



# # Decorator method to check if user logged in
# def is_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             # return redirect(url_for('login'))
#             raise AuthError("Not logged in, please login",401)
#     return wrap