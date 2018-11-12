from __future__ import unicode_literals, absolute_import, print_function

import random
from app.api import API
from app.command import Command
from api.settings import OBWAGA6_CHAT_ID, JEKA_DJ_CHAT_ID


class AdminCommands:


    @staticmethod
    def is_ok(msg):
        cmd_obj = Command(msg['text'])
        chat_id = msg['chat']['id']

        if chat_id != JEKA_DJ_CHAT_ID:
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
        
        if chat_id != JEKA_DJ_CHAT_ID:
            return False

        if cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('pin'):
            res = API.sendMsg(OBWAGA6_CHAT_ID, cmd_obj.value)
            if res is not None:
                API.pinMsg(OBWAGA6_CHAT_ID, res['message_id'])
            return True

        elif cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('msg'):
            API.sendMsg(OBWAGA6_CHAT_ID, cmd_obj.value)
            return True

        elif cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('pinmsg'):
            API.sendMsgAndPin(OBWAGA6_CHAT_ID, cmd_obj.value)
            return True

        elif (cmd_obj.is_param_semicolon() and cmd_obj.is_cmd_eq('msg') and \
              cmd_obj.param.isdigit() and len(cmd_obj.value) > 0):

            send_to_chat_id = int(cmd_obj.param)
            if API.sendMsg(send_to_chat_id, cmd_obj.value):
                API.sendMsg(JEKA_DJ_CHAT_ID, 'SUCCESSFULLY SENT "{}" to "{}"'.format(cmd_obj.value, send_to_chat_id))
            else:
                API.sendMsg(JEKA_DJ_CHAT_ID, 'NOT SENT "{}" to "{}"'.format(cmd_obj.value, send_to_chat_id))
            return True

        return False