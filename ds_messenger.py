import socket
import ds_protocol
from typing import TextIO
import asyncio, time, json
from collections import namedtuple

port = 3021

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
      print(j_msg)
      resp = self.write(ds_conn, j_msg)
      print(resp)
      return ds_protocol.extract_token(resp)

    def write(self, ds_conn:DSConnection, message:str):
        ds_conn.send.write(message + '\r\n')
        ds_conn.send.flush()
        resp = ds_conn.recv.readline()

        return resp

    def send(self, message:str, recipient:str) -> bool:
        # returns true if message successfully sent, false if send failed.
        connect = self.connection(self.dsuserver, port)
        if connect == None:
            print('Unable to connect')
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
            print('Direct Message Unable to be Sent')
            return False



    def retrieve_new(self) -> list:
        connect = self.connection(self.dsuserver, port)
        # returns a list of DirectMessage objects containing all messages
        if connect == None:
            print('Unable to connect')
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

    def retrieve_all(self) -> list:
        connect = self.connection(self.dsuserver, port)
        # returns a list of DirectMessage objects containing all messages
        if connect == None:
            print('Unable to connect')
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
                print('ERROR')
                return None
