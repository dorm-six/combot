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

    @staticmethod
    def pinMsg(chat_id, msg_id):

        # prepare payload
        payload = {
            'chat_id': chat_id,
            'message_id': msg_id
        }

        # make request
        r = requests.get(BASE_URL + 'pinChatMessage', params=payload)
        data = r.json()

        # return
        return data['result'] if data['ok'] is True else None

    @staticmethod
    def sendMsgAndPin(chat_id, text):

        # send msg
        msg = API.apiSendMsg(chat_id, text)
        if msg is None:
            return None

        # pin msg
        API.apiPinMsg(chat_id, msg['message_id'])

        # return
        return msg

    @staticmethod
    def sendPhoto(chat_id, photo_url, caption=None, explicit_return=False):

        # prepare payload
        payload = {
            'chat_id': chat_id,
            'photo': photo_url
        }
        if caption:
            payload['caption'] = caption

        # make request
        r = requests.get(BASE_URL + 'sendPhoto', params=payload)
        data = r.json()

        # prepare result
        res = None
        if explicit_return:
            res = data
        elif data['ok'] is True:
            res = data['result']

        return res

    @staticmethod
    def forwardMsg(from_chat_id, to_chat_id, msg_id):

        # prepare payload
        payload = {
            'chat_id': to_chat_id,
            'from_chat_id': from_chat_id,
            'message_id': msg_id
        }

        # make request
        r = requests.get(BASE_URL + 'forwardMessage', params=payload)
        data = r.json()

        # return
        return data['result'] if data['ok'] is True else None

    @staticmethod
    def unpinMsg(chat_id):

        # prepare payload
        payload = {
            'chat_id': chat_id,
        }
        
        # make request
        r = requests.get(BASE_URL + 'unpinChatMessage', params=payload)
        data = r.json()

        # return
        return data['result'] if data['ok'] is True else None
