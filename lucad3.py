import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeerInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse, UsernameUniquenessResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage,IncomingGroupChatMessage,IncomingStatusResponse, IncomingGroupStatus, OutgoingChatMessage
from kik_unofficial.datatypes.xmpp.login import ConnectionFailedResponse
import logging
import time
import threading
from typing import List, Union
from kik_unofficial.datatypes.xmpp.base_elements import XMPPElement
import datetime
import random
import json

username = '{username}'
password = '{password}'

with open("quotes.json","r",encoding="utf8") as f:
  quotes_list = json.load(f)


current_time = datetime.datetime.now()



class EchoBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    
    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage ):
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))
        print("[+] Replaying.")

        if ("hello" == chat_message.body.lower()):
        	self.client.send_chat_message(chat_message.from_jid,f"Aye cutie")

        elif ("time"== chat_message.body.lower()):
        	self.client.send_chat_message(chat_message.from_jid,f"{current_time}")

        elif("Decode" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.from_jid,f"Available commands: \nhello\ntime\nlucad\nDescribe")

        elif ("lucad" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.from_jid,"Yes b*tch thats me")

        elif ("describe" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.from_jid,"Lucad \nSeries:HAL 90000\n")

        elif ("purpose" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.from_jid,"(　-_･) ︻デ═一  ▸ ")

        elif ("snipe" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.from_jid,"▄︻̷̿┻̿═━一")

        elif ("babe" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.from_jid,"quotes_list['quotes'][random.randint(1,102)]['quote']")


# 
    def on_group_message_received(self, chat_message:chatting.IncomingGroupChatMessage):
         print("[+] '{}' from group ID {} says: {}".format(chat_message.from_jid, chat_message.group_jid,
                                                          chat_message.body))
         if ("hello" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,f"Aye cutie")

         elif ("lucad" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,"Yes b*tch thats me")

         elif ("time"== chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,f"{currentTime()}")

         elif("Decode" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,f"Available commands: \nhello\ntime\nusage\nDescribe")

         elif("lurkers" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,f"Lurkers are: null")

         elif ("purpose" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,"(　-_･) ︻デ═一  ▸ ")

         elif ("snipe" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,"▄︻̷̿┻̿═━一")


         elif ("wisdom" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,f"{quotes_list['quotes'][random.randint(1,102)]['quote']}")

        


    def on_message_read(self, response: chatting.IncomingMessageReadEvent):
        print("[+] Human has read the message with ID {}.".format(response.message_id))


def currentTime():
    return(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

class RemoveFromGroupRequest(XMPPElement):
    def __init__(self, group_jid, peer_jid,message_id):
        super().__init__()
        self.group_jid = group_jid
        self.peer_jid = peer_jid
        self.message_id = message_id

    def serialize(self) -> bytes:
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '<m r="1">{}</m>'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid, self.peer_jid)
        return data.encode()


def main():
    bot = EchoBot()


if __name__ == '__main__':
    main()
