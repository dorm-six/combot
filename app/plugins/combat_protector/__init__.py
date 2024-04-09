from __future__ import unicode_literals, absolute_import, print_function

import random
from app.api import API
from app.settings import OBWAGA6_CHAT_ID


class Combat_Protector:
    @staticmethod
    def pin(msg):
        chat_id = msg['chat']['id']
        API.sendMsgAndPin(chat_id, 'КОМБАТЫ')

    @staticmethod
    def unpin(msg):
        chat_id = msg['chat']['id']
        if API.unpinMsg(chat_id):
            API.sendMsg(chat_id, 'ОТКРЕПЛЕНО')
