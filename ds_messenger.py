import socket
import ds_protocol
from typing import TextIO
import asyncio, time, json
from collections import namedtuple

port = 3021

class MessengerException(Exception):
    """Raised when message fails to send."""
    pass

class ConnectionException(Exception):
    """Raised when connection is not established etc."""
    pass

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
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def connection(self, server:str, port:int):
        """Establishes a connection to the server so messages can be sent."""
        
        try:
            ds_conn = DSConnection()
            ds_conn.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ds_conn.connection.connect((server,port))
            ds_conn.send = ds_conn.connection.makefile('w')
            ds_conn.recv = ds_conn.connection.makefile('r')
            return ds_conn
        except:
            return None

    def join(self, ds_conn:DSConnection, username:str, password:str) -> str:
      """
      Takes in the parameter and uses the ds_protocol to make the join message.
      Takes the join message and puts it into the write function to be written to the server.
      """
      
      j_msg = ds_protocol.joinmsg(username, password)
      
      resp = self.write(ds_conn, j_msg)
      
      return ds_protocol.extract_token(resp)

    def write(self, ds_conn:DSConnection, message:str):
        """Sends the message to the server."""
        
        ds_conn.send.write(message + '\r\n')
        ds_conn.send.flush()
        resp = ds_conn.recv.readline()

        return resp

    def send(self, message:str, recipient:str) -> bool:
        """
        Sends the direct message to the specified recipient.
        Returns true if message successfully sent, false if send failed.
        """
        
        connect = self.connection(self.dsuserver, port)

        try:
            if connect == None:
                raise ConnectionException()
                return False
            else:
                self.token = self.join(connect, self.username, self.password)
                msg = ds_protocol.send_directmessage(self.token, message, recipient)
                resp = self.write(connect, msg)
                resps = ds_protocol.extract_response_typ(resp)
                return resps
            if resps == 'ok':
                print('Direct Message Sent')
                return True
            else:
                raise MessengerException()
                
                return False
        
        except ConnectionException:
            print("Cannot Connect. Please Check Connection")
        except MessengerException:
            print('Direct Message Unable to be Sent')
            


    def retrieve_new(self) -> list:
        """Returns a list of DirectMessage objects containing all messages."""
        
        connect = self.connection(self.dsuserver, port)
        
        try:
            if connect == None:
                raise ConnectionException()
                return None
            else:
                try:
                    self.token = self.join(connect, self.username, self.password)
                    
                    new_msg = ds_protocol.request_messages(self.token,'new')
                    
                    resp = self.write(connect, new_msg)
                    resps = ds_protocol.extract_response_typ(resp)
                    messages = ds_protocol.extract_json(resp)
                    return messages
                except:
                    print('ERROR')
                    return None
        except ConnectionException:
            print("Connection Error")


    def retrieve_all(self) -> list:
        """Returns a list of DirectMessage objects containing all messages"""
        connect = self.connection(self.dsuserver, port)
        
        try:
            if connect == None:
                raise ConnectionException()
                return None
            else:
                try:
                    self.token = self.join(connect, self.username, self.password)
                    
                    new_msg = ds_protocol.request_messages(self.token,'all')
                    
                    resp = self.write(connect, new_msg)
                    resps = ds_protocol.extract_response_typ(resp)
                    messages = ds_protocol.extract_json(resp)
                    return messages
                except:
                    print("ERROR")
                    return None
                
        except ConnectionException:
            print("Connection Error")
