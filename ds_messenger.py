import socket
import ds_protocol

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
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
				client.connect(server, port)

				send = client.makefile('w')
				recv = client.makefile('r')

				send.write(message + '\r\n')
				send.flush()

				msg = recv.readline()
				ds_connection = True
		except:
			print('Unable to Connect')
			ds_connection = False
			

	def send(self, message:str, recipient:str) -> bool:
		# returns true if message successfully sent, false if send failed.
		connet = connection(self.dsuserver, port)


	pass

	def retrieve_new(self) -> list:
	# returns a list of DirectMessage objects containing all new messages

		pass

	def retrieve_all(self) -> list:
	# returns a list of DirectMessage objects containing all messages
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
		

