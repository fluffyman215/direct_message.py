#For JSON SCRIPT
import json, time
from collections import namedtuple
DataTuple = namedtuple('DataTuple', ['type','message'])

"""
Converts the send message into a json string.
"""
def send_directmessage(user_token, msg, recipient):

    json_directmessage = json.dumps({"token":user_token, "directmessage": {"entry": msg,"recipient": recipient, "timestamp": str(time.time())}})
    
    return json_directmessage

"""
Converts the request message into a json string.
"""
def request_messages(user_token, msg):
    
    json_request = json.dumps({"token": user_token, "directmessage": msg})
    
    return json_request

"""
Call the json.loads function on a json string and convert it to a DataTuple object
"""
def extract_json(json_msg:str) -> DataTuple:
    try:
        json_obj = json.loads(json_msg)
        server_response = json_obj['response']['type']
        message = json_obj['response']['messages']
        return message

    except json.JSONDecodeError:
        
        print("Json cannot be decoded.")

        return DataTuple(server_response, message)

"""
Call the json.loads function on a json string and convert it to a DataTuple object and returns response type.
"""
def extract_response_typ(json_str:str) -> str:
    typ = ''
    try:
        json_obj = json.loads(json_str)
        typ = json_obj['response']['type']
        return typ
    except json.JSONDecodeError:
        print('JSON cannot be decoded')
        return typ

"""
This function will take in the parameters and create the join message.
"""
def joinmsg(username:str, password:str) -> str:
    msg = '{"join": {"username":"'+username+'", "password":"'+password+'", "token":"user_token"}}'
    return msg

"""
This function will take in the server's response, and return the server's public key for the ds_client to proceed.
"""
def extract_token(json_str:str) -> str:
    typ = ''
    msg = ''
    token = None
    try:
        json_obj = json.loads(json_str)
        typ = json_obj['response']['type']
        msg = json_obj['response']['message']
        if 'token' in json_obj['response']:
            token = json_obj['response']['token']
    except json.JSONDecodeError:
        print('JSON cannot be decoded')
    return token
