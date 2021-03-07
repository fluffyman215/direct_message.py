import socket
import ds_protocol

class DSConnection:
	connection: socket = None
	send: TextIO = None
	recv: TextIO = None

class DirectMessage:
	def __init__(self):
	self.recipient = None
	self.message = None
	self.timestamp = None
	
class DirectMessenger:
	def __init__(self, dsuserver=None, username=None, password=None):
		self.token = None
		self.dsuserver = None
		self.username = None
		self.password = None
	
	def connection(self, server:str, port:int):
		try:
			ds_conn = DSConnection()
			ds_conn.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ds_conn.connection.connect((server,port))
			ds_conn.send = ds_conn.connection.makefile('w')
			ds_conn.recv = ds_conn.connection.makefile('r')
		 	return ds_conn
		 except:
		 	return None
			
	def write(self, ds_conn:DSConnection, message:str):
  		ds_conn.send.write(message + '\r\n')
  		ds_conn.send.flush()
 		resp = ds_conn.recv.readline()
  		return resp

	def send(self, message:str, recipient:str) -> bool:
		# returns true if message successfully sent, false if send failed.
		connet = connection(self.dsuserver, port)
		if connect == None:
			print('Unable to connect')
			return False
		else:
			msg = ds_protocol.send_directmessage(self.token, message, recipient)
			resp = write(msg)
			resps = extract_response_typ(resp)
			if resps == 'ok':
				print('Direct Message Sent')
				return True
			else:
				print('Direct Message Unable to be Sent')
				return False



	def retrieve_new(self) -> list:
	# returns a list of DirectMessage objects containing all new messages
		new_msg = ds_protocol.request(messages(self.token, "new"))
		messages = ds_protocol.extract_json_new(new_msg)
		return messages.message

	def retrieve_all(self) -> list:
	# returns a list of DirectMessage objects containing all messages
		new_msg = ds_protocol.request(messages(self.token, "new"))
		messages = ds_protocol.extract_json_all(new_msg)
		return messages.message
		pass
	
	def send_request(self, new_msg):
		'''
		Extra send function to connect retrieve_new and retrieve_all functions.
		
		new_msg will be the keywords associated to retrieve the desired information.
		'''
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
				client.connect(self.dsuserver, port)

				send = client.makefile('w')
				recv = client.makefile('r')

				send.write(new_msg + '\r\n')
				send.flush()

				msg = recv.readline()
		

