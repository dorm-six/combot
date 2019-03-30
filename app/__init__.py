# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import time
import json
import random
import datetime
import requests
import threading
import traceback
from time import gmtime, strftime

from app.plugins.hw import HW
from app.plugins.mall import Mall
from app.plugins.chicks import Chicks
from app.plugins.schedule import Schedule
from app.plugins.admin_commands import AdminCommands
from app.plugins.combat_protector import Combat_Protector

from app.api import API
from app.command import Command
from app.settings import JEKA_DJ_CHAT_ID, DENIS_EMINEM_CHAT_ID, VLAD_KULAK_CHAT_ID, BODIES
from app.settings import BASE_URL, OBWAGA6_CHAT_ID, TESTGROUP_CHAT_ID, OBWAGA_CHAT_IDS

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

        payload = {'allowed_updates': ['message'], 'offset': UPDATE_OFFSET}

        try:
            r = requests.get(BASE_URL + 'getUpdates', params=payload)
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError) as e:
            traceback.print_exc()
            exc_trace = traceback.format_exc()
            API.sendMsg(JEKA_DJ_CHAT_ID, exc_trace)
            time.sleep(30)
            continue

        data = r.json()
        if data['ok'] == False:
            print('status "False" on getUpdates returned')
            raise Exception

        CUTTING_IDX = 50
        if len(data['result']) > CUTTING_IDX:
            UPDATE_OFFSET = data['result'][CUTTING_IDX]['update_id']

        return data

def filterByUpdateId(res):
    try:
        return res['update_id'] > LAST_UPDATE_ID
    except KeyError:
        return False

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
    to_chat_id = JEKA_DJ_CHAT_ID
    msg_id = msg['message_id']

    API.sendMsg(to_chat_id, 'chat_id: {}. msg_id: {}'.format(from_chat_id, msg_id))
    API.forwardMsg(from_chat_id, to_chat_id, msg_id)

# --------------------
# --- mainActivity ---
# --------------------

def mainActivity():
    global UPDATE_OFFSET
    global LAST_UPDATE_ID

    # --------------------
    # --- initializing ---
    # --------------------
    
    print('Initializing...')

    payload = {'allowed_updates': ['message'], 'offset': UPDATE_OFFSET}
    r = requests.get(BASE_URL + 'getUpdates', params=payload)
    data = r.json()

    if data['ok'] == False:
        print('status "False" on getUpdates returned')
        print('Exiting...')
        exit()

    if len(data['result']) > 0:
        UPDATE_OFFSET = data['result'][-1]['update_id']
        LAST_UPDATE_ID = UPDATE_OFFSET

    # -----------------
    # --- main work ---
    # -----------------
    
    print('Main Work started...')

    while True:
        try:
            data = getUpdatesOrExit()
        except ValueError as e:
            traceback.print_exc()
            exc_trace = traceback.format_exc()
            API.sendMsg(JEKA_DJ_CHAT_ID, exc_trace)
            time.sleep(1)
            continue

        ress = data['result']
        results = list(filter(filterByUpdateId, ress))

        if len(results) == 0:
            time.sleep(3)
            continue

        for res in results:
            try:
                msg = res['message']
                chat_id = msg['chat']['id']
                cmd_obj = Command(msg['text'])
            except KeyError:
                continue

            if cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/buy'):
                Mall.buy(msg)
            elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/ping'):
                handlePing(msg)
            elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/baby'):
                Chicks.do(msg)
            elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/schedule'):
                Schedule.do(msg)

            elif chat_id in OBWAGA_CHAT_IDS:
                if Combat_Protector.scanForCombat(msg):
                    Combat_Protector.notificationForwarding(msg)
                elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/pin'):
                    Combat_Protector.pin(msg)
                elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/unpin'):
                    Combat_Protector.unpin(msg)
                elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/hw'):
                    HW.do(msg)
                
            else:
                if cmd_obj.is_cmd_eq('/sell'):
                    Mall.sell(msg)
                elif cmd_obj.is_cmd_eq('/delsell'):
                    Mall.delete(msg)
                elif cmd_obj.is_cmd_eq('/edit') and cmd_obj.is_param_semicolon():
                    Mall.edit(msg)

                # others
                elif AdminCommands.is_ok(msg):
                    AdminCommands.do(msg)
                else:
                    handleExternalMessage(msg)

        LAST_UPDATE_ID = ress[-1]['update_id']

        time.sleep(3)


def run():
    while True:
        try:
            mainActivity()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print('Exception: type:{}. msg:{}'.format(type(e), e))
            print('--------------------')
            try:
                traceback.print_exc()
                exc_trace = traceback.format_exc()
                API.sendMsg(JEKA_DJ_CHAT_ID, exc_trace)
            except Exception:
                pass
            print('--------------------')
            time.sleep(3)

if __name__ == "__main__":
    run()
