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

def extract_json_sent(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  
  try:
    json_obj = json.loads(json_msg)
    server_response = json_obj['response']['type']
    message = json_obj['response']['message']
    
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(server_response, message, token)

def extract_json_receive(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  
  try:
    json_obj = json.loads(json_msg)
    server_response = json_obj['response']['type']
    message = json_obj['response']['messages']
    
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(server_response, message, token)
