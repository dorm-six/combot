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

BODIES = [
    239745097,  # Jeka_DJ
    129085681,  # Denis_Eminem
    1591398,    # Vlad_Kulak
]
OBWAGA_CHAT_ID = [
    -1001176853573,     # testgroup
    -1001131239095,     # 
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

IS_ALIVE = True
"""
    Heartbeat thread
"""
class HeartbeatThread(threading.Thread):
    def run(self):
        while IS_ALIVE is True:
            payload = {
                'chat_id': 239745097, # Jeka_DJ
                'text': '[<3] Combot Heartbeat'
            }
            requests.get(BASE_URL + 'sendMessage', params=payload)
            print('[<3] {} Heartbeat sent'.format(str(datetime.datetime.now())))

            time.sleep(5*60)

"""
    Foos
"""

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
        return res['update_id'] > LAST_UPDATE_ID and res['message']['chat']['id'] in OBWAGA_CHAT_ID
    except KeyError:
        return False

def combatLogger(message):
    t = datetime.datetime.fromtimestamp(
            message['date']
        ).strftime('%Y-%m-%d %H:%M:%S')
    chat_id = message['chat']['id']
    chat_title = message['chat']['title']

    print("[!] {} COMBAT DETECTED!!! {} {}".format(t, chat_id, chat_title))

def broadcastWarning(message):
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
    payload = {
        'chat_id': msg['chat']['id'],
        'message_id': msg['message_id']
    }
    r = requests.get(BASE_URL + 'pinChatMessage', params=payload)

    t = getTimeStringOfMessage(msg)

    print('[+] {} PINNED in chat {}:{}'.format(t, msg['chat']['id'], msg['chat']['title']))

    return msg

def getTimeStringOfMessage(msg):
    return datetime.datetime.fromtimestamp(
            msg['date']
        ).strftime('%Y-%m-%d %H:%M:%S')
"""
    /hw
"""
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

def mainActivity():
    global UPDATE_OFFSET
    global BASE_URL
    global LAST_UPDATE_ID

    """
        initializing
    """
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

    res = data['result']

    if len(res) != 0:
        last_msg = res[-1]
        LAST_UPDATE_ID = last_msg['update_id']

    """
        init heartbeat thread
    """

    heartbeat_thread = HeartbeatThread()  # ...Instantiate a thread and pass a unique ID to it
    heartbeat_thread.start()

    """
        main work
    """
    print('Main Work started...')

    while True:
        try:
            data = getUpdatesOrExit()
        except ValueError as e:
            print(e)
            time.sleep(1)
            continue

        ress = data['result']
        results = list(filter(filterByUpdateIdandChatId, ress))

        if len(results) == 0:
            time.sleep(3)
            continue

        for res in results:
            msg = res['message']

            try:
                if combatFinder(msg['text']) == True and '@CombatDetectorBot' not in msg['text']:
                    broadcastWarning(msg)
                    combatLogger(msg)
                elif msg['text'] == '/pin@CombatDetectorBot' or msg['text'] == '/pin':
                    msg = sendWarningAndPin(msg)
                    broadcastWarning(msg)
                elif msg['text'] == '/unpin@CombatDetectorBot' or msg['text'] == '/unpin':
                    payload = {
                        'chat_id': msg['chat']['id'],
                    }
                    r = requests.get(BASE_URL + 'unpinChatMessage', params=payload)
                    if r.json()['ok'] is True:
                        payload = {
                            'chat_id': msg['chat']['id'],
                            'text': 'ОТКРЕПЛЕНО'
                        }
                        requests.get(BASE_URL + 'sendMessage', params=payload)

                    t = getTimeStringOfMessage(msg)
                    print('[+] {} Unpinned'.format(t))
                elif msg['text'] == '/hw':
                    hwHandle(msg)

            except KeyError:
                pass

            LAST_UPDATE_ID = res['update_id']

        LAST_UPDATE_ID = ress[-1]['update_id']

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