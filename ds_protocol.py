#For JSON SCRIPT
import json, time
from collections import namedtuple
DataTuple = namedtuple('DataTuple', ['type','message','token'])
MessageTuple = namedtuple('MessageTuple', ['type', 'message'])

def send_directmessage(user_token, msg, recipient):
  
  json_directmessage = json.dumps({"token":user_token, "directmessage": {"entry": msg,"recipient": recipient, "timestamp": str(time.time())}})
  return json_directmessage

def request_messages(user_token, msg):
  json_request = json.dumps({"token": user_token, "directmessage": msg})
  return json_request
