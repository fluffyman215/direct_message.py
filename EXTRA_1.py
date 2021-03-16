
def retrieve_all(self) -> list:
        connect = self.connection(self.dsuserver, port)
        print(connect)
        # returns a list of DirectMessage objects containing all messages
        new_msg = ds_protocol.request_messages(self.token,'all')
        print(new_msg)
        print(80)
        resp = self.write(connect, new_msg)
        print(resp)
        resps = ds_protocol.extract_response_typ(resp)
        print(resps)
        print(9)
        messages = ds_protocol.extract_json_all(resp)
        print(messages)
        return messages
