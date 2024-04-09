# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import time
import json
import random
import logging
import datetime
import requests
import threading
import traceback
from time import gmtime, strftime

from app.plugins.hw import HW
from app.plugins.chicks import Chicks
from app.plugins.schedule import Schedule
from app.plugins.admin_commands import AdminCommands
from app.plugins.combat_protector import Combat_Protector

from app.api import API
from app.command import Command
from app.settings import CHAT_ID_SUPERUSER
from app.settings import BASE_URL, CHAT_ID_DORM_CHAT, CHAT_ID_TEST_CHAT, DORM_CHAT_IDS

# ---------------
# --- GLOBALS ---
# ---------------

UPDATE_OFFSET = 0
LAST_UPDATE_ID = 0

# ------------
# --- Foos ---
# ------------

def getUpdatesOrExit():
    global UPDATE_OFFSET

    while True:
        payload = {'allowed_updates': ['message'], 'offset': UPDATE_OFFSET + 1, 'timeout': 55}

        try:
            r = requests.get(BASE_URL + 'getUpdates', params=payload, timeout=60)
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError) as e:
            traceback.print_exc()
            exc_trace = traceback.format_exc()
            API.sendMsg(CHAT_ID_SUPERUSER, exc_trace)
            time.sleep(30)
            continue

        data = r.json()
        if data['ok'] == False:
            logging.error(
                'status "False" on getUpdates returned. Response body: %s',
                json.dumps(body, sort_keys=True, indent=4)
            )
            raise Exception()

        CUTTING_IDX = 50
        if len(data['result']) > CUTTING_IDX:
            UPDATE_OFFSET = data['result'][CUTTING_IDX]['update_id']

        logging.debug(data)

        return data

# ----------------
# --- Handlers ---
# ----------------

def handlePing(msg):
    chat_id = msg['chat']['id']
    text = 'I am Alive, сучка'
    API.sendMsg(chat_id, text)

# -------------------------
# --- External messages ---
# -------------------------

def handleExternalMessage(msg):
    from_chat_id = msg['chat']['id']
    to_chat_id = CHAT_ID_SUPERUSER
    msg_id = msg['message_id']

    API.sendMsg(to_chat_id, 'chat_id: {}. msg_id: {}'.format(from_chat_id, msg_id))
    API.forwardMsg(from_chat_id, to_chat_id, msg_id)

# --------------------
# --- mainActivity ---
# --------------------

def mainActivity():
    global UPDATE_OFFSET

    # --------------------
    # --- initializing ---
    # --------------------
    
    logging.info('Initializing...')

    payload = {'allowed_updates': ['message'], 'offset': UPDATE_OFFSET, 'timeout': 55}
    r = requests.get(BASE_URL + 'getUpdates', params=payload, timeout=60)
    data = r.json()

    if data['ok'] == False:
        logging.error(
            'status "False" on getUpdates returned. Response body: %s',
            json.dumps(body, sort_keys=True, indent=4)
        )
        exit(1)

    if len(data['result']) > 0:
        UPDATE_OFFSET = data['result'][-1]['update_id']

    # -----------------
    # --- main work ---
    # -----------------
    
    logging.info('Main Work started...')

    while True:
        try:
            data = getUpdatesOrExit()
        except ValueError as e:
            traceback.print_exc()
            exc_trace = traceback.format_exc()
            API.sendMsg(CHAT_ID_SUPERUSER, exc_trace)
            time.sleep(1)
            continue

        results = data['result']

        for res in results:
            try:
                msg = res['message']
                chat_id = msg['chat']['id']
                cmd_obj = Command(msg['text'])
            except KeyError:
                continue

            if cmd_obj.is_single_cmd():
                if cmd_obj.is_cmd_eq('/ping'):
                    handlePing(msg)
                elif cmd_obj.is_cmd_eq('/baby'):
                    Chicks.do(msg)
                elif cmd_obj.is_cmd_eq('/schedule'):
                    Schedule.do(msg)

                elif chat_id in DORM_CHAT_IDS:
                    if cmd_obj.is_cmd_eq('/pin'):
                        Combat_Protector.pin(msg)
                    elif cmd_obj.is_cmd_eq('/unpin'):
                        Combat_Protector.unpin(msg)
                    elif cmd_obj.is_cmd_eq('/hw'):
                        HW.do(msg)
            elif AdminCommands.is_ok(msg):
                AdminCommands.do(msg)
            else:
                handleExternalMessage(msg)

        if results:
            UPDATE_OFFSET = results[-1]['update_id']


def run():
    logging.basicConfig(level=logging.DEBUG)
    while True:
        try:
            mainActivity()
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.exception("run() exception caught")
            try:
                exc_trace = traceback.format_exc()
                API.sendMsg(CHAT_ID_SUPERUSER, exc_trace)
            except Exception:
                pass
            time.sleep(3)

if __name__ == "__main__":
    run()
