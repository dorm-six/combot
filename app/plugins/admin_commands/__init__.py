from __future__ import unicode_literals, absolute_import, print_function

import random
from app.api import API
from app.command import Command
from app.settings import CHAT_ID_DORM_CHAT, CHAT_ID_SUPERUSER


class AdminCommands:


    @staticmethod
    def is_ok(msg):
        cmd_obj = Command(msg['text'])
        chat_id = msg['chat']['id']

        if chat_id != CHAT_ID_SUPERUSER:
            return False

        if cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('pin'):
            return True
        elif cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('msg'):
            return True
        elif cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('pinmsg'):
            return True
        elif (cmd_obj.is_param_semicolon() and cmd_obj.is_cmd_eq('msg') and \
              cmd_obj.param.isdigit() and len(cmd_obj.value) > 0):
            return True
        else:
            return False

    @staticmethod
    def do(msg):
        cmd_obj = Command(msg['text'])
        chat_id = msg['chat']['id']
        
        if chat_id != CHAT_ID_SUPERUSER:
            return False

        if cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('pin'):
            res = API.sendMsg(CHAT_ID_DORM_CHAT, cmd_obj.value)
            if res is not None:
                API.pinMsg(CHAT_ID_DORM_CHAT, res['message_id'])
            return True

        elif cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('msg'):
            API.sendMsg(CHAT_ID_DORM_CHAT, cmd_obj.value)
            return True

        elif cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('pinmsg'):
            API.sendMsgAndPin(CHAT_ID_DORM_CHAT, cmd_obj.value)
            return True

        elif (cmd_obj.is_param_semicolon() and cmd_obj.is_cmd_eq('msg') and \
              cmd_obj.param.isdigit() and len(cmd_obj.value) > 0):

            send_to_chat_id = int(cmd_obj.param)
            if API.sendMsg(send_to_chat_id, cmd_obj.value):
                API.sendMsg(CHAT_ID_SUPERUSER, 'SUCCESSFULLY SENT "{}" to "{}"'.format(cmd_obj.value, send_to_chat_id))
            else:
                API.sendMsg(CHAT_ID_SUPERUSER, 'NOT SENT "{}" to "{}"'.format(cmd_obj.value, send_to_chat_id))
            return True

        return False