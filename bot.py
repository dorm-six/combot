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

UPDATE_OFFSET = 0
LAST_UPDATE_ID = 0

# ------------------------
# --- Heartbeat thread ---
# ------------------------

IS_ALIVE = True

class HeartbeatThread(threading.Thread):
    def run(self):
        while IS_ALIVE is True:
            payload = {
                'chat_id': JEKA_DJ_CHAT_ID, # Jeka_DJ
                'text': '[<3] Combot Heartbeat'
            }
            requests.get(BASE_URL + 'sendMessage', params=payload)
            print('[<3] {} Heartbeat sent'.format(str(datetime.datetime.now())))

            time.sleep(15*60)

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

def filterByUpdateIdandChatId(res):
    try:
        cond1 = res['update_id'] > LAST_UPDATE_ID
        cond21 = res['message']['chat']['id'] in OBWAGA_CHAT_IDS
        cond22 = res['message']['chat']['id'] == 239745097
        cond2 = cond21 or cond22
        return cond1 and cond2
    except KeyError:
        return False

def filterByUpdateId(res):
    try:
        return res['update_id'] > LAST_UPDATE_ID
    except KeyError:
        return False

def combatLogger(message):
    t = datetime.datetime.fromtimestamp(
            message['date']
        ).strftime('%Y-%m-%d %H:%M:%S')
    chat_id = message['chat']['id']
    chat_title = message['chat']['title']

    print("[!] {} COMBAT DETECTED!!! {} {}".format(t, chat_id, chat_title))

def broadcastWarning(msg):
    for chat_id in BODIES:
        payload = {
            'chat_id': chat_id,
            'from_chat_id': msg['chat']['id'],
            'message_id': msg['message_id']
        }
        r = requests.get(BASE_URL + 'forwardMessage', params=payload)

def sendWarningAndPin(msg):
    # print('sendWarningAndPin')

    payload = {
        'chat_id': msg['chat']['id'],
        'text': 'КОМБАТЫ'
    }
    r = requests.get(BASE_URL + 'sendMessage', params=payload)
    data = r.json()

    if data['ok'] == False:
        return

    msg = data['result']
    apiPinMsg(msg['chat']['id'], msg['message_id'])

    t = getTimeStringOfMessage(msg)
    print('[+] {} PINNED in chat {}:{}'.format(t, msg['chat']['id'], msg['chat']['title']))

    return msg

def getTimeStringOfMessage(msg):
    return datetime.datetime.fromtimestamp(
            msg['date']
        ).strftime('%Y-%m-%d %H:%M:%S')

def handleUnpin(msg):
    payload = {
        'chat_id': msg['chat']['id'],
    }
    r = requests.get(BASE_URL + 'unpinChatMessage', params=payload)
    if r.json()['ok'] is True:
        apiSendMsg(msg['chat']['id'], 'ОТКРЕПЛЕНО')
    t = getTimeStringOfMessage(msg)
    print('[+] {} Unpinned'.format(t))

def handleBroadcastNotification(msg):
    broadcastWarning(msg)
    combatLogger(msg)

def handlePin(msg):
    msg = sendWarningAndPin(msg)
    broadcastWarning(msg)

def handlePing(msg):
    chat_id = msg['chat']['id']
    text = 'I am Alive, сучка'
    apiSendMsg(chat_id, text)
    print('[+] handlePing')

# -----------
# --- /hw ---
# -----------

def hwHandle_response(msg):
    resp_msg = 'Huli Wi {}'.format(random.choice(HW))
    payload = {
        'chat_id': msg['chat']['id'],
        'text': resp_msg
    }
    r = requests.get(BASE_URL + 'sendMessage', params=payload)

def hwHandle_body(msg):
    _from = msg['from']
    name = _from['first_name'] or _from['username'] or _from['last_name'] or 'Эй'

    candidates = [
        ', бро, хватит уже', ', бро, заебал',
        ', бро, заебал с этой херней', ', заебал, реально',
        ', прекрати', ', твоюжмать, хватит уже!'
    ]

    resp_msg = name + random.choice(candidates)
    payload = {
        'chat_id': msg['chat']['id'],
        'text': resp_msg
    }
    r = requests.get(BASE_URL + 'sendMessage', params=payload)


def hwHandle(msg):
    if random.randint(0, 3) != 0:
        return
    if random.randint(0, 1) == 0:
        hwHandle_body(msg)
    else:
        hwHandle_response(msg)

# -----------------
# --- API CALLS ---
# -----------------

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

# ----------------------
# --- ADMIN COMMANDS ---
# ----------------------

def handleAdminCommands(msg):
    text = msg['text']
    if text.find('pin: ') == 0:
        print('[PIN] {}'.format(text))
        # PIN MESSAGE
        text = text[5:]
        res = apiSendMsg(TESTGROUP_CHAT_ID, text)
        if res is not None:
            apiPinMsg(TESTGROUP_CHAT_ID, res['message_id'])

    elif text.find('msg: ') == 0:
        print('[MSG] {}'.format(text))
        # SEND MESSAGE
        text = text[5:]
        apiSendMsg(TESTGROUP_CHAT_ID, text)

# -------------------------
# --- External messages ---
# -------------------------

def handleExternalMessage(msg):
    from_chat_id = msg['chat']['id']
    to_chat_id = JEKA_DJ_CHAT_ID
    msg_id = msg['message_id']
    res = apiForwardMsg(from_chat_id, to_chat_id, msg_id)
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

    # -----------------------------
    # --- init heartbeat thread ---
    # -----------------------------

    heartbeat_thread = HeartbeatThread()  # ...Instantiate a thread and pass a unique ID to it
    heartbeat_thread.start()

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
                        handleBroadcastNotification(msg)
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
            IS_ALIVE = False
            break
        except Exception as e:
            print(e)
            IS_ALIVE = False
            time.sleep(10)
            