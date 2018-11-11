from __future__ import unicode_literals, absolute_import, print_function

import requests

from app.settings import BASE_URL


class API:
    
    @staticmethod
    def sendMsg(chat_id, msg, parse_mode=None, disable_web_page_preview=False, explicit_return=False):

        # prepare payload for request
        payload = {
            'chat_id': chat_id,
            'text': msg
        }
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_web_page_preview is True:
            payload['disable_web_page_preview'] = True

        # make request
        r = requests.get(BASE_URL + 'sendMessage', json=payload)
        data = r.json()

        # prepare return value
        res = None
        if explicit_return:
            res = data
        elif data['ok'] is True:
            res = data['result']

        # return
        return res
