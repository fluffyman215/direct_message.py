import socket
import ds_protocol

class DirectMessage:
	def __init__(self):
	self.recipient = None
	self.message = None
	self.timestamp = None


class DirectMessenger(DirectMessage):
	def __init__(self, dsuserver=None, username=None, password=None):
		## dsu_server = 168.235.86.101
		## port = 3021
		self.token = None
		self.dsuserver = None
		self.username = None
		self.password = None
	
	def connection(self, server:str, port:int):
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
				client.connect(server, port)

				send = client.makefile('w')
				recv = client.makefile('r')

				send.write(message + '\r\n')
				send.flush()

				msg = recv.readline()
				ds_connection = True
		except socket.gaierror:
			print('Unable to Connect')
			ds_connection = False
			return ds_connection
		except socket.error as e:
			return False
			

	def send(self, message:str, recipient:str) -> bool:
		# returns true if message successfully sent, false if send failed.
		connet = connection(self.dsuserver, port)


	pass

	def retrieve_new(self) -> list:
	# returns a list of DirectMessage objects containing all new messages
		new_messages = self.send_request("new")
		list_messages = ds_protocol.json_extract_retrieve(new_messages)
		return list_messages.message

	def retrieve_all(self) -> list:
	# returns a list of DirectMessage objects containing all messages
		new_messages = self.send_request("all")
		list_messages = ds_protocol.json_extract_retrieve(new_messages)
		return list_messages.message
		
	
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
				
				msg_to_send = ds_protocol.request_messages(self.token, new_msg)
				send.write(msg_to_send + '\r\n')
				send.flush()

				msg = recv.readline()
				
				return msg
		

