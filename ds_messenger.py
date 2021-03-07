class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
	self.token = None
	self.dsuserver = None
	self.username =
	
		
  def send(self, message:str, recipient:str) -> bool:
    # returns true if message successfully sent, false if send failed.
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
			client.connect(server, port)
			
			send = client.makefile('w')
            		recv = client.makefile('r')
			
			send.write(profile + '\r\n')
		    	send.flush()
			
		    	msg = recv.readline()
    pass
		
  def retrieve_new(self) -> list:
    # returns a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # returns a list of DirectMessage objects containing all messages
    pass
