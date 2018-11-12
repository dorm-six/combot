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

from app.api import API
from app.plugins.schedule import Schedule
from app.plugins.chicks import Chicks
from app.plugins.mall import Mall
from app.command import Command
from app.settings import BASE_URL
from app.settings import RUSIK_CHAT_ID, JEKA_DJ_CHAT_ID, DENIS_EMINEM_CHAT_ID, VLAD_KULAK_CHAT_ID, BODIES
from app.settings import OBWAGA6_CHAT_ID, TESTGROUP_CHAT_ID, OBWAGA_CHAT_IDS

# ---------------
# --- GLOBALS ---
# ---------------

UPDATE_OFFSET = 0
LAST_UPDATE_ID = 0

# ------------
# --- Foos ---
# ------------

def combatFinder(msg):
    msg = msg.lower()

    malicious_words = [
        u'комбат', u'кмбат', u'камбат', u'комбта', u'комбот',
        u'combat', u'cmbat', u'cambat', u'combta', u'combot',
    ]

    for word in malicious_words:
        if word in msg:
            return True

    return False

def getUpdatesOrExit():
    global UPDATE_OFFSET

    while True:

        payload = {'allowed_updates': ['message'], 'offset': UPDATE_OFFSET}

        try:
            r = requests.get(BASE_URL + 'getUpdates', params=payload)
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError) as e:
            t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            print('[!] {} Exception in getUpdatesOrExit()'.format(t))
            traceback.print_exc()
            exc_trace = traceback.format_exc()
            API.sendMsg(JEKA_DJ_CHAT_ID, exc_trace)
            print('[!] {} Sleeping for 30 seconds...'.format(t))
            time.sleep(30)
            print('[!] {} Trying to getUpdates again...'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            continue

        data = r.json()
        if data['ok'] == False:
            print('status "False" on getUpdates returned')
            print('Exiting...')
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

def combatLogger(msg):
    t = datetime.datetime.fromtimestamp(
            msg['date']
        ).strftime('%Y-%m-%d %H:%M:%S')
    chat_id = msg['chat']['id']
    chat_title = msg['chat']['title']

    print("[!] {} COMBAT DETECTED!!! {} {}".format(t, chat_id, chat_title))

def getTimeStringOfMessage(msg):
    return datetime.datetime.fromtimestamp(
            msg['date']
        ).strftime('%Y-%m-%d %H:%M:%S')

# ----------------
# --- Handlers ---
# ----------------

def handleUnpin(msg):
    chat_id = msg['chat']['id']
    if API.unpinMsg(chat_id):
        API.sendMsg(chat_id, 'ОТКРЕПЛЕНО')

    t = getTimeStringOfMessage(msg)
    # print('[+] {} Unpinned'.format(t))

    if chat_id == OBWAGA6_CHAT_ID:
        API.sendMsg(RUSIK_CHAT_ID, 'ОТКРЕПЛЕНО')

def handleCombotNotification(msg):
    for chat_id in BODIES:
        API.forwardMsg(msg['chat']['id'], chat_id, msg['message_id'])
    combatLogger(msg)

def handlePin(msg):
    msg = API.sendMsgAndPin(msg['chat']['id'], 'КОМБАТЫ')
    if msg:
        for chat_id in BODIES:
            API.forwardMsg(msg['chat']['id'], chat_id, msg['message_id'])

    if msg['chat']['id'] == OBWAGA6_CHAT_ID:
        API.sendMsg(RUSIK_CHAT_ID, 'КОМБАТЫ')

def handlePing(msg):
    chat_id = msg['chat']['id']
    text = 'I am Alive, сучка'
    API.sendMsg(chat_id, text)
    # print('[+] handlePing')

# -----------
# --- /hw ---
# -----------

def hwHandle_response(msg):

    HW = [
        'делаете', 'пидоры то такие', 'не учитесь',
        'бухаете', 'пишите', 'творите', 'кушаете',
        'не спите', 'можете?', 'имеете против меня?',
        'такие динозавры', 'опять спамите эту хуйню',
        'курите?', 'заебываете меня!!', '?? не пойти ли вам н@&yi?'
        'такие дерзские?', 'комбатов не боитесь', 'выселения не боитесь',
        'отчисления не боитесь', 'удивляетесь', 'доебались',
        'приперлись, вас никто не ждал здесь',
        '? почему вы ? да идите нахуй просто! Я бот, мне можно все.',
        'понтуетесь?', 'шумите!!!', 'хотели-то?'
    ]

    resp_msg = 'Huli Wi {}'.format(random.choice(HW))
    API.sendMsg(msg['chat']['id'], resp_msg)

def hwHandle_body(msg):

    candidates = [
        ', бро, хватит уже', ', бро, заебал',
        ', бро, заебал с этой херней', ', заебал, реально',
        ', прекрати', ', твоюжмать, хватит уже!'
    ]

    _from = msg['from']
    name = _from['first_name'] or _from['username'] or _from['last_name'] or 'Эй'

    resp_msg = name + random.choice(candidates)
    API.sendMsg(msg['chat']['id'], resp_msg)

def hwHandle(msg):
    if random.randint(0, 1) != 0:
        return
    if random.randint(0, 1) == 0:
        hwHandle_body(msg)
    else:
        hwHandle_response(msg)


# ----------------------
# --- ADMIN COMMANDS ---
# ----------------------

def handleAdminCommands(msg):
    text = msg['text']
    chat_id = msg['chat']['id']
    cmd_obj = Command(text)

    if text.find('pin:') == 0:
        # print('[PIN] {}'.format(text))
        # PIN MESSAGE
        text = text[4:]
        res = API.sendMsg(OBWAGA6_CHAT_ID, text)
        if res is not None:
            API.pinMsg(OBWAGA6_CHAT_ID, res['message_id'])

    elif cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('msg'):
        API.sendMsg(OBWAGA6_CHAT_ID, cmd_obj.value)

    elif text.find('pinmsg:') == 0:
        # print('[PINMSG] {}'.format(text))
        text = text[7:]
        API.sendMsgAndPin(OBWAGA6_CHAT_ID, text)

    elif (cmd_obj.is_param_semicolon() and \
          cmd_obj.is_cmd_eq('msg') and \
          cmd_obj.param.isdigit() and \
          len(cmd_obj.value) > 0
         ):
        if API.sendMsg(chat_id, cmd_obj.value):
            API.sendMsg(msg['chat']['id'], 'SUCCESSFULLY SENT "{}" to "{}"'.format(cmd_obj.value, chat_id))
        else:
            API.sendMsg(msg['chat']['id'], 'NOT SENT "{}" to "{}"'.format(cmd_obj.value, chat_id))

    else:
        handleExternalMessage(msg)

# -------------------------
# --- External messages ---
# -------------------------

def handleExternalMessage(msg):
    from_chat_id = msg['chat']['id']
    to_chat_id = JEKA_DJ_CHAT_ID
    msg_id = msg['message_id']

    API.sendMsg(to_chat_id, 'chat_id: {}. msg_id: {}'.format(from_chat_id, msg_id))
    API.forwardMsg(from_chat_id, to_chat_id, msg_id)
    # print('[+] handleExternalMessage. from:{}. to:{}. text:{}'.format(from_chat_id, to_chat_id, msg['text']))

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
            except KeyError:
                msg = '-'*30 + '\n' + str(res) + '\n'
                msg += traceback.format_exc() + '\n' + '-'*30
                API.sendMsg(JEKA_DJ_CHAT_ID, msg)
                continue

            chat_id = msg['chat']['id']
            try:
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
                if combatFinder(msg['text']) == True and '@CombatDetectorBot' not in msg['text']:
                    handleCombotNotification(msg)
                elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/pin'):
                    handlePin(msg)
                elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/unpin'):
                    handleUnpin(msg)
                elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/hw'):
                    hwHandle(msg)

            else:
                if cmd_obj.is_cmd_eq('/sell'):
                    Mall.sell(msg)
                elif cmd_obj.is_cmd_eq('/delsell'):
                    Mall.delete(msg)
                elif cmd_obj.is_cmd_eq('/edit') and cmd_obj.is_param_semicolon():
                    Mall.edit(msg)

                # others
                elif chat_id == JEKA_DJ_CHAT_ID:
                    handleAdminCommands(msg)
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
