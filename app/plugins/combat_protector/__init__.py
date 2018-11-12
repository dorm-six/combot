from __future__ import unicode_literals, absolute_import, print_function

import random
from app.api import API
from app.settings import BODIES, OBWAGA6_CHAT_ID


class Combat_Protector:

    malicious_words = [
            u'комбат', u'кмбат', u'камбат', u'комбта', u'комбот',
            u'combat', u'cmbat', u'cambat', u'combta', u'combot',
    ]

    @staticmethod
    def pin(msg):
        chat_id = msg['chat']['id']
        msg = API.sendMsgAndPin(chat_id, 'КОМБАТЫ')
        if msg:
            for to_chat_id in BODIES:
                API.forwardMsg(chat_id, to_chat_id, msg['message_id'])

        if chat_id == OBWAGA6_CHAT_ID:
            API.sendMsg(RUSIK_CHAT_ID, 'КОМБАТЫ')

    @staticmethod
    def unpin(msg):
        chat_id = msg['chat']['id']
        if API.unpinMsg(chat_id):
            API.sendMsg(chat_id, 'ОТКРЕПЛЕНО')

        if chat_id == OBWAGA6_CHAT_ID:
            API.sendMsg(RUSIK_CHAT_ID, 'ОТКРЕПЛЕНО')

    @staticmethod
    def scanForCombat(msg):
        if '@CombatDetectorBot' in msg['text']:
            return False

        msg = msg['text'].lower()

        for word in Combat_Protector.malicious_words:
            if word in msg:
                return True

        return False

    @staticmethod
    def notificationForwarding(msg):
        for chat_id in BODIES:
            API.forwardMsg(msg['chat']['id'], chat_id, msg['message_id'])
