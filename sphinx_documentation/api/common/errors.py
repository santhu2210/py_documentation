from werkzeug.exceptions import HTTPException


class AuthError(HTTPException):
    """ Raises error if User is not Authenticated """
    """Class to handle error if un Authenticated user
    Attributes:
        status_code: Error status code.
        message: Error message.
        response: Contains status, message and status code.
    """
    def __init__(self, auth_err):
        """Inits authentication error class."""
        self.message = auth_err
        self.status_code = 401
        self.response = ({'status': self.status,'message': self.message},self.status_code)


class ProfileNotFoundError(HTTPException):
    """ Raises error if Profile Id not found """
    """Class to handle error if Profile Id not found 
    Attributes:
        status_code: Error status code.
        message: Error message.
        response: Contains status, message and status code.
    """
    def __init__(self):
        """Inits ProfileNotFoundError class."""
        self.status_code = 400
        self.message = "Please check the profile ID"
        self.status = "error"
        self.response = ({'status': self.status,'message': self.message},self.status_code)


class GeneralError(HTTPException):
    """ Class to handle general error by  passing error message
    Attributes:
        status_code: Error status code.
        message: Error message.
        response: Contains status, message and status code.   
     """
    def __init__(self,err_msg):
        """Inits GeneralError class."""
        self.status_code = 400
        self.message = err_msg
        self.status = "error"
        self.response = ({'status': self.status,'message': self.message},self.status_code)