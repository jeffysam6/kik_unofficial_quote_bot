import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeerInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse, UsernameUniquenessResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage, IncomingGroupChatMessage, IncomingStatusResponse, IncomingGroupStatus
from kik_unofficial.datatypes.xmpp.login import ConnectionFailedResponse
import logging
import time
import threading
from typing import List, Union
from kik_unofficial.datatypes.xmpp.base_elements import XMPPElement


username = '{username}'
password = '{password}'


def main():
    bot = EchoBot()


class EchoBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))
        print("[+] Replaying.")
        self.client.send_chat_message(chat_message.from_jid, "You said \"" + chat_message.body + "\"!")

    def on_message_delivered(self, response: chatting.IncomingMessageDeliveredEvent):
        print("[+] Chat message with ID {} is delivered.".format(response.message_id))

    def on_message_read(self, response: chatting.IncomingMessageReadEvent):
        print("[+] Human has read the message with ID {}.".format(response.message_id))

    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        print("[+] '{}' from group ID {} says: {}".format(chat_message.from_jid, chat_message.group_jid,
                                                          chat_message.body))

    def on_is_typing_event_received(self, response: chatting.IncomingIsTypingEvent):
        print("[+] {} is now {}typing.".format(response.from_jid, "not " if not response.is_typing else ""))

    def on_group_is_typing_event_received(self, response: chatting.IncomingGroupIsTypingEvent):
        print("[+] {} is now {}typing in group {}".format(response.from_jid, "not " if not response.is_typing else "",
                                                          response.group_jid))

    def on_roster_received(self, response: FetchRosterResponse):
        print("[+] Roster:\n" + '\n'.join([str(m) for m in response.members]))

    def on_friend_attribution(self, response: chatting.IncomingFriendAttribution):
        print("[+] Friend attribution request from " + response.referrer_jid)

    def on_image_received(self, image_message: chatting.IncomingImageMessage):
        print("[+] Image message was received from {}".format(image_message.from_jid))
    
    def on_peer_info_received(self, response: PeerInfoResponse):
        print("[+] Peer info: " + str(response.users))

    def on_group_status_received(self, response: chatting.IncomingGroupStatus):
        print("[+] Status message in {}: {}".format(response.group_jid, response.status))

    def on_group_receipts_received(self, response: chatting.IncomingGroupReceiptsEvent):
        print("[+] Received receipts in group {}: {}".format(response.group_jid, ",".join(response.receipt_ids)))

    def on_status_message_received(self, response: chatting.IncomingStatusResponse):
        print("[+] Status message from {}: {}".format(response.from_jid, response.status))

    def on_username_uniqueness_received(self, response: UsernameUniquenessResponse):
        print("Is {} a unique username? {}".format(response.username, response.unique))

    def on_sign_up_ended(self, response: RegisterResponse):
        print("[+] Registered as " + response.kik_node)

    # Error handling

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("[-] Connection failed: " + response.message)

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print("[-] Register error: {}".format(response.message))
        
class AddToGroupRequest(XMPPElement):
    def __init__(self, group_jid, peer_jid):
        super().__init__()
        self.group_jid = group_jid
        self.peer_jid = peer_jid

    def serialize(self) -> bytes:
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '<m>{}</m>'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid, self.peer_jid)
        return data.encode()


class RemoveFromGroupRequest(XMPPElement):
    def __init__(self, group_jid, peer_jid):
        super().__init__()
        self.group_jid = group_jid
        self.peer_jid = peer_jid

    def serialize(self) -> bytes:
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '<m r="1">{}</m>'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid, self.peer_jid)
        return data.encode()


class UnbanRequest(XMPPElement):
    def __init__(self, group_jid, peer_jid):
        super().__init__()
        self.group_jid = group_jid
        self.peer_jid = peer_jid

    def serialize(self) -> bytes:
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '<b r="1">{}</b>'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid, self.peer_jid)
        return data.encode()


class BanMemberRequest(XMPPElement):
    def __init__(self, group_jid, peer_jid):
        super().__init__()
        self.group_jid = group_jid
        self.peer_jid = peer_jid

    def serialize(self) -> bytes:
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '<b>{}</b>'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid, self.peer_jid)
        return data.encode()


class LeaveGroupRequest(XMPPElement):
    def __init__(self, group_jid):
        super().__init__()
        self.group_jid = group_jid

    def serialize(self) -> bytes:
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '<l />'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid)
        return data.encode()


class PromoteToAdminRequest(XMPPElement):
    def __init__(self, group_jid, peer_jid):
        super().__init__()
        self.group_jid = group_jid
        self.peer_jid = peer_jid

    def serialize(self) -> bytes:
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '<m a="1">{}</m>'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid, self.peer_jid)
        return data.encode()


class DemoteAdminRequest(XMPPElement):
    def __init__(self, group_jid, peer_jid):
        super().__init__()
        self.group_jid = group_jid
        self.peer_jid = peer_jid

    def serialize(self) -> bytes:
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '<m a="0">{}</m>'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid, self.peer_jid)
        return data.encode()


class AddMembersRequest(XMPPElement):
    def __init__(self, group_jid, peer_jids: Union[str, List[str]]):
        super().__init__()
        self.group_jid = group_jid
        if isinstance(peer_jids, List):
            self.peer_jids = peer_jids
        else:
            self.peer_jids = [peer_jids]

    def serialize(self) -> bytes:
        items = ''.join(['<m>{}</m>'.format(jid) for jid in self.peer_jids])
        data = ('<iq type="set" id="{}">'
                '<query xmlns="kik:groups:admin">'
                '<g jid="{}">'
                '{}'
                '</g>'
                '</query>'
                '</iq>').format(self.message_id, self.group_jid, items)
        return data.encode()

if __name__ == '__main__':
    main()
