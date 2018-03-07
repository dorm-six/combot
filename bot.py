# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import time
import datetime
from time import gmtime, strftime
import threading
import random
import os

# Example of your code beginning
#           Config vars
TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

RUSIK_CHAT_ID = -172022743
JEKA_DJ_CHAT_ID = 239745097
DENIS_EMINEM_CHAT_ID = 129085681
VLAD_KULAK_CHAT_ID = 1591398
BODIES = [
    JEKA_DJ_CHAT_ID,        # Jeka_DJ
    DENIS_EMINEM_CHAT_ID,   # Denis_Eminem
    VLAD_KULAK_CHAT_ID,     # Vlad_Kulak
]

OBWAGA6_CHAT_ID = -1001131239095
TESTGROUP_CHAT_ID = -1001176853573
OBWAGA_CHAT_IDS = [
    TESTGROUP_CHAT_ID,     # testgroup
    OBWAGA6_CHAT_ID,       # 
]

MALICIOUS = [
    u'комбат', u'кмбат', u'камбат', u'комбта', u'комбот',
    u'combat', u'cmbat', u'cambat', u'combta', u'combot',
]

UPDATE_OFFSET = 0
LAST_UPDATE_ID = 0

# ------------
# --- Foos ---
# ------------

def combatFinder(msg):
    msg = msg.lower()

    for word in MALICIOUS:
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
            print(e)
            print('[!] {} Sleeping for 30 seconds...'.format(t))
            time.sleep(30)
            print('[!] {} Trying to getUpdates again...'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            continue

        data = r.json()
        if data['ok'] == False:
            print('status "False" on getUpdates returned')
            print('Exiting...')
            exit()

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
    if apiUnpinMsg(chat_id):
        apiSendMsg(chat_id, 'ОТКРЕПЛЕНО')

    t = getTimeStringOfMessage(msg)
    print('[+] {} Unpinned'.format(t))

    if chat_id == OBWAGA6_CHAT_ID:
        apiSendMsg(RUSIK_CHAT_ID, 'ОТКРЕПЛЕНО')

def handleCombotNotification(msg):
    for chat_id in BODIES:
        apiForwardMsg(msg['chat']['id'], chat_id, msg['message_id'])
    combatLogger(msg)

def handlePin(msg):
    msg = sendMsgAndPin(msg['chat']['id'], 'КОМБАТЫ')
    if msg:
        for chat_id in BODIES:
            apiForwardMsg(msg['chat']['id'], chat_id, msg['message_id'])

    if msg['chat']['id'] == OBWAGA6_CHAT_ID:
        apiSendMsg(RUSIK_CHAT_ID, 'КОМБАТЫ')

def handlePing(msg):
    chat_id = msg['chat']['id']
    text = 'I am Alive, сучка'
    apiSendMsg(chat_id, text)
    print('[+] handlePing')

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
    apiSendMsg(msg['chat']['id'], resp_msg)

def hwHandle_body(msg):

    candidates = [
        ', бро, хватит уже', ', бро, заебал',
        ', бро, заебал с этой херней', ', заебал, реально',
        ', прекрати', ', твоюжмать, хватит уже!'
    ]

    _from = msg['from']
    name = _from['first_name'] or _from['username'] or _from['last_name'] or 'Эй'

    resp_msg = name + random.choice(candidates)
    apiSendMsg(msg['chat']['id'], resp_msg)

def hwHandle(msg):
    if random.randint(0, 1) != 0:
        return
    if random.randint(0, 1) == 0:
        hwHandle_body(msg)
    else:
        hwHandle_response(msg)

# -----------------
# --- API CALLS ---
# -----------------

def sendMsgAndPin(chat_id, text):

    msg = apiSendMsg(chat_id, text)
    if msg is None:
        print('[!] sendMsgAndPin : result of apiSendMsg is None')
        return None
    apiPinMsg(chat_id, msg['message_id'])

    t = getTimeStringOfMessage(msg)
    print('[+] {} PINNED in chat {}:{}'.format(t, chat_id, msg['chat']['title']))

    return msg

def apiSendMsg(chat_id, msg):
    payload = {
        'chat_id': chat_id,
        'text': msg
    }
    r = requests.get(BASE_URL + 'sendMessage', params=payload)
    data = r.json()

    if data['ok'] == False:
        return None
    else:
        return data['result']

def apiPinMsg(chat_id, msg_id):
    payload = {
        'chat_id': chat_id,
        'message_id': msg_id
    }
    r = requests.get(BASE_URL + 'pinChatMessage', params=payload)
    data = r.json()

    if data['ok'] == False:
        return None
    else:
        return data['result']

def apiForwardMsg(from_chat_id, to_chat_id, msg_id):
    payload = {
        'chat_id': to_chat_id,
        'from_chat_id': from_chat_id,
        'message_id': msg_id
    }
    r = requests.get(BASE_URL + 'forwardMessage', params=payload)
    data = r.json()

    if data['ok'] == False:
        return None
    else:
        return data['result']

def apiUnpinMsg(chat_id):
    payload = {
        'chat_id': chat_id,
    }
    r = requests.get(BASE_URL + 'unpinChatMessage', params=payload)
    data = r.json()

    if data['ok'] == False:
        return None
    else:
        return data['result']

# ----------------------
# --- ADMIN COMMANDS ---
# ----------------------

def handleAdminCommands(msg):
    text = msg['text']

    if text.find('pin:') == 0:
        print('[PIN] {}'.format(text))
        # PIN MESSAGE
        text = text[4:]
        res = apiSendMsg(OBWAGA6_CHAT_ID, text)
        if res is not None:
            apiPinMsg(OBWAGA6_CHAT_ID, res['message_id'])

    elif text.find('msg:') == 0:
        print('[MSG] {}'.format(text))
        # SEND MESSAGE
        text = text[4:]
        apiSendMsg(OBWAGA6_CHAT_ID, text)

    elif text.find('msg') == 0:
        colon_idx = text.find(':')
        space_idx = text.find(' ')

        cond1 = colon_idx > 4
        cond2 = space_idx > 2
        cond3 = space_idx < colon_idx

        if cond1 and cond2 and cond3:
            chat_id = text[space_idx+1:colon_idx]
            if chat_id.isdigit():
                if apiSendMsg(chat_id, text[colon_idx+1:]):
                    apiSendMsg(msg['chat']['id'], 'SUCCESSFULLY SENT "{}" to "{}"'.format(text[colon_idx+1:], chat_id))
                else:
                    apiSendMsg(msg['chat']['id'], 'NOT SENT "{}" to "{}"'.format(text[colon_idx+1:], chat_id))

    else:
        handleExternalMessage(msg)

# -------------------------
# --- External messages ---
# -------------------------

def handleExternalMessage(msg):
    from_chat_id = msg['chat']['id']
    to_chat_id = JEKA_DJ_CHAT_ID
    msg_id = msg['message_id']
    text = "{}:{}".format(from_chat_id, msg['chat']['title'])

    apiSendMsg(to_chat_id, text)
    apiForwardMsg(from_chat_id, to_chat_id, msg_id)
    print('[+] handleExternalMessage. from:{}. to:{}. text:{}'.format(from_chat_id, to_chat_id, msg['text']))

# --------------------
# --- mainActivity ---
# --------------------

def mainActivity():
    global UPDATE_OFFSET
    global BASE_URL
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
            print(e)
            time.sleep(1)
            continue

        ress = data['result']
        results = list(filter(filterByUpdateId, ress))

        if len(results) == 0:
            time.sleep(3)
            continue

        for res in results:
            msg = res['message']
            chat_id = msg['chat']['id']

            if chat_id in OBWAGA_CHAT_IDS:
                try:
                    if combatFinder(msg['text']) == True and '@CombatDetectorBot' not in msg['text']:
                        handleCombotNotification(msg)
                    elif msg['text'] == '/pin@CombatDetectorBot' or msg['text'] == '/pin':
                        handlePin(msg)
                    elif msg['text'] == '/unpin@CombatDetectorBot' or msg['text'] == '/unpin':
                        handleUnpin(msg)
                    elif msg['text'] == '/hw':
                        hwHandle(msg)
                    elif msg['text'] == '/ping@CombatDetectorBot' or msg['text'] == '/ping':
                        handlePing(msg)
                except KeyError:
                    pass
            elif chat_id == JEKA_DJ_CHAT_ID:
                handleAdminCommands(msg)
            else:
                handleExternalMessage(msg)

        LAST_UPDATE_ID = results[-1]['update_id']

        time.sleep(3)

if __name__ == "__main__":
    while True:
        try:
            mainActivity()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            time.sleep(10)
