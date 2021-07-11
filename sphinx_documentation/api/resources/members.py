import os
import json
from flask_restful import Resource, reqparse, marshal, fields
from common.errors import AuthError, ProfileNotFoundError, GeneralError
from flask_jwt import jwt_required

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

json_data_path = os.path.join(BASE_DIR,'data','members.json')


# Opening JSON file
with open(json_data_path) as json_file:
    members_data = json.load(json_file)


member_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String,
    "age": fields.Integer,
    "is_active": fields.Boolean,
}

def member_request_parser():
    """member details request parser.
    Returns:
        Parsed member details.
    """ 
    input_parser = reqparse.RequestParser()
    input_parser.add_argument("id", type=int, required=True, location="json")
    input_parser.add_argument("name", type=str, required=True, location="json")
    input_parser.add_argument("location", type=str, required=False, location="json")
    input_parser.add_argument("age", type=int, required=False, location="json")
    input_parser.add_argument("is_active", type=bool, required=False, location="json",  default=True)
    return input_parser


def member_args_parser(args):
    """member details Args parser.
    Returns:
        A dict of members details arguments parsed.
    """
    member_updates = {
        "id":args["id"],
        "name": args["name"],
        "location": args["location"],
        "age":args["age"],
        "is_active": args["is_active"]
    }
    return member_updates


# Class to manage members detail with get and post method
class MembersList(Resource):
    """Class to manage members detail with GET and POST  methods.

    Attributes:
        reqparse: member details request parser.
    """
    def __init__(self):
        """Inits memberList class."""
        self.reqparse = member_request_parser()
        super(MembersList, self).__init__()
    
    @jwt_required()
    def get(self):
        """Performs GET method to get all active member details.
        Authentication Required
        Returns:
            A dict with all active member details.
        Raises:
            ProfileNotFoundError: An error occured if profile Id is not found in 
            datastore or profile is not active.
        """

        profiles = members_data['members']
        
        if (profiles is None):
            raise ProfileNotFoundError()
        all_profiles = [marshal(profile, member_fields) for profile in profiles]
        # datastore query not supported '!=' operator, so added not-equal condition in code
        active_profiles  = [profile_dict for profile_dict in all_profiles if profile_dict['is_active'] != False]
        return {"members": active_profiles}

    @jwt_required()
    def post(self):
        """Performs POST method to create member details.
        Authentication Required
        Returns:
            A dict with response code, message , status and member details added.
        Raises:
            GeneralError: An error occured if profile values are not in accepted format.
        """

        args = self.reqparse.parse_args()
        memberInsert = member_args_parser(args)

        profiles = members_data['members']
        profile =  list(filter(lambda member_record: member_record['id'] == memberInsert['id'], profiles))

        if memberInsert and len(profile) == 0:
            members_data['members'].append(memberInsert)

            with open(json_data_path, 'w') as fp:
                json.dump(members_data, fp)
            
            return {"status": "success","message":"Member details has been created successfully",
                "member":marshal(memberInsert, member_fields),"code":201}
        
        else:
            raise GeneralError('Some thing went wrong, Please check input data')



# Class to manage members details with get method
class MembersItem(Resource):
    """Class to manage members detail with GET and PUT  methods.
    Authentication Required
    Attributes:
        reqparse: member details request parser.
    """
    def __init__(self):
        """Inits membersItem class."""
        self.reqparse = member_request_parser()
        super(MembersItem, self).__init__()

    @jwt_required()
    def get(self, id):
        """Performs GET method to get members details.
        Args:
            id: Id of profile of which member details has to be get.
        Returns:
            A dict with person details.
        Raises:
            ProfileNotFoundError: An error occured if member Id is not found in 
            json data or profile is not active.
        """
        profiles = members_data['members']

        profile =  list(filter(lambda member_record: member_record['id'] == id, profiles))
        
        if len(profile) == 0:
            raise ProfileNotFoundError()
        return {"member": marshal(profile, member_fields)}