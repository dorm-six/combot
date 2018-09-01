# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import time
import random
import datetime
import requests
import threading
from time import gmtime, strftime

from db import new_session, CombotMall
from settings import BASE_URL


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
    print('[+] {} PINNED in chat {}'.format(t, chat_id))

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

def apiSendPhoto(chat_id, photo_url, explicit_return=False):
    payload = {
        'chat_id': chat_id,
        'photo': photo_url
    }
    r = requests.get(BASE_URL + 'sendPhoto', params=payload)
    data = r.json()

    if explicit_return:
        return data
    else:
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

    apiSendMsg(to_chat_id, str(from_chat_id))
    apiForwardMsg(from_chat_id, to_chat_id, msg_id)
    print('[+] handleExternalMessage. from:{}. to:{}. text:{}'.format(from_chat_id, to_chat_id, msg['text']))

# ---------------------
# --- Baby messages ---
# ---------------------

def babyHandle(msg):
    chicks = {
        'Megan Fox' : 'https://pp.userapi.com/c840322/v840322120/45c9b/oiJ4RHqVYTI.jpg',
        'Jessica Alba' : 'https://pp.userapi.com/c621705/v621705776/8224c/kNfdB8EJeXM.jpg',
        'Jessica Alba 2' : 'https://pp.userapi.com/c840227/v840227855/8eea9/goF2Tcrk-To.jpg',
        'Sasha Grey' : 'https://pp.userapi.com/c621511/v621511163/6a44e/NXEPY7GXl5c.jpg',
        'Scarlett Johansson' : 'https://sun9-8.userapi.com/c840520/v840520285/6a6db/qxI7cbg5mjU.jpg',
        'Margot Robbie' : 'https://sun9-9.userapi.com/c840426/v840426620/6b540/zPEXaRUC2ZQ.jpg',
        'Jennifer Lawrence' : 'https://pp.userapi.com/c621511/v621511648/6cc89/yvQ1cIvO5FE.jpg',
        'Amber Heard' : 'https://pp.userapi.com/c840221/v840221545/8f505/ey9_lJAWLC0.jpg',
        'Miranda Kerr' : 'https://pp.userapi.com/c621706/v621706850/7dc15/WlA3cQlL0qY.jpg',
        'Rihanna' : 'https://sun9-7.userapi.com/c840526/v840526105/6ab69/34LcCIQdzqE.jpg',
        'Lizzy Caplan' : 'https://pp.userapi.com/c840325/v840325631/6e827/BchgGnPyfis.jpg',
        'Emma Watson' : 'https://sun9-5.userapi.com/c840433/v840433317/6cafd/aHgSpcrSTaU.jpg',
        'Rachel Nicols' : 'https://pp.userapi.com/c840331/v840331377/7073d/L6SdkSOr04M.jpg',
        'Fat Man' : 'https://pp.userapi.com/c840127/v840127496/8ffd9/X8IcN9CV-aA.jpg'
    }

    chat_id = msg['chat']['id']
    baby, photo_url = random.choice(list(chicks.items()))

    print('[+] babyHandle {} : {} : {}'.format(chat_id, baby, photo_url))

    apiSendPhoto(chat_id, photo_url, explicit_return=True)

# ------------------
# --- Bed linnin ---
# ------------------

def bedHandle(msg):

    chat_id = msg['chat']['id']
    msg = "Расписание смены постельного белья:\n"
    msg += "пн: 8:30-12:00, 15:00-17:00\n"
    msg += "ср: 8:30-12:00, 15:00-17:00\n"
    msg += "чт: 8:30-12:00, 15:00-17:00\n"
    msg += "пт: 8:30-12:00, 14:00-16:00\n"
    msg += "Если расписание изменилось, напишите боту в личку"

    apiSendMsg(chat_id, msg)
    print('[+] babyHandle.')

# ----------------
# --- The Mall ---
# ----------------

def sellHandle(msg):

    # Get optional args
    try:
        user = msg['from']
        description = msg['text']
    except KeyError:
        apiSendMsg(JEKA_DJ_CHAT_ID, 'ERROR: sellHandle: {}'.format(msg))
        return

    # Get args
    chat_id = msg['chat']['id']
    seller_id = user['id']
    seller_username = user.get('username', 'UNKNOWN')

    # open db connection
    session = new_session()

    # count actual value
    count = session.query(CombotMall).filter(CombotMall.seller_id == seller_id).count()
    if count >= 5:
        apiSendMsg(chat_id, 'Too much sell entries for you')
        return

    # create new sell entry
    cm = CombotMall(seller_id=seller_id, seller_username=seller_username, description=description)
    session.add(cm)
    session.commit()
    session.close()

    # success notification
    apiSendMsg(chat_id, 'Done')

    return
        
def buyHandle(msg):

    chat_id = msg['chat']['id']

    session = new_session()
    entries = session.query(CombotMall).all()
    session.close()

    msg = ''
    for entry in entries:
        msg += '{}:{} {}\n'.format(entry.seller_id, entry.seller_username, entry.description)

    apiSendMsg(chat_id, msg)

    return


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

            if msg['text'] == '/ping@CombatDetectorBot' or msg['text'] == '/ping':
                handlePing(msg)
            elif msg['text'] == '/baby':
                babyHandle(msg)
            elif msg['text'] == '/bed' or msg['text'] == '/bed@CombatDetectorBot':
                bedHandle(msg)
            elif (msg['text'] == '/sell' or msg['text'] == '/sell@CombatDetectorBot') and chat_id not in OBWAGA_CHAT_IDS:
                sellHandle(msg)
            elif (msg['text'] == '/buy' or msg['text'] == '/buy@CombatDetectorBot') and chat_id not in OBWAGA_CHAT_IDS:
                buyHandle(msg)
            elif chat_id in OBWAGA_CHAT_IDS:
                try:
                    if combatFinder(msg['text']) == True and '@CombatDetectorBot' not in msg['text']:
                        handleCombotNotification(msg)
                    elif msg['text'] == '/pin@CombatDetectorBot' or msg['text'] == '/pin':
                        handlePin(msg)
                    elif msg['text'] == '/unpin@CombatDetectorBot' or msg['text'] == '/unpin':
                        handleUnpin(msg)
                    elif msg['text'] == '/hw':
                        hwHandle(msg)
                except KeyError:
                    pass
            elif chat_id == JEKA_DJ_CHAT_ID:
                handleAdminCommands(msg)
            else:
                handleExternalMessage(msg)

        LAST_UPDATE_ID = ress[-1]['update_id']

        time.sleep(3)

if __name__ == "__main__":
    while True:
        try:
            mainActivity()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print('Exception: type:{}. msg:{}'.format(type(e), e))
            time.sleep(5)
