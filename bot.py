# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import time
import random
import datetime
import requests
import threading
import traceback
import json
from time import gmtime, strftime

from db import new_session, CombotMall, delete_by_id
from command import Command
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

def apiSendMsg(chat_id, msg, parse_mode=None, disable_web_page_preview=False, explicit_return=False):
    payload = {
        'chat_id': chat_id,
        'text': msg
    }

    print(payload)

    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_web_page_preview is True:
        payload['disable_web_page_preview'] = True

    r = requests.get(BASE_URL + 'sendMessage', json=payload)
    data = r.json()

    if explicit_return:
        return data
    else:
        if data['ok'] == False:
            return None
        else:
            return data['result']

def apiSendPhoto(chat_id, photo_url, caption=None, explicit_return=False):
    payload = {
        'chat_id': chat_id,
        'photo': photo_url
    }
    if caption:
        payload['caption'] = caption

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
    chat_id = msg['chat']['id']
    cmd_obj = Command(text)

    if text.find('pin:') == 0:
        print('[PIN] {}'.format(text))
        # PIN MESSAGE
        text = text[4:]
        res = apiSendMsg(OBWAGA6_CHAT_ID, text)
        if res is not None:
            apiPinMsg(OBWAGA6_CHAT_ID, res['message_id'])

    elif cmd_obj.is_semicolon() and cmd_obj.is_cmd_eq('msg'):
        apiSendMsg(OBWAGA6_CHAT_ID, cmd_obj.value)

    elif text.find('pinmsg:') == 0:
        print('[PINMSG] {}'.format(text))
        text = text[7:]
        sendMsgAndPin(OBWAGA6_CHAT_ID, text)

    elif (cmd_obj.is_param_semicolon() and \
          cmd_obj.is_cmd_eq('msg') and \
          cmd_obj.param.isdigit() and \
          len(cmd_obj.value) > 0
         ):
        if apiSendMsg(chat_id, cmd_obj.value):
            apiSendMsg(msg['chat']['id'], 'SUCCESSFULLY SENT "{}" to "{}"'.format(cmd_obj.value, chat_id))
        else:
            apiSendMsg(msg['chat']['id'], 'NOT SENT "{}" to "{}"'.format(cmd_obj.value, chat_id))

    else:
        handleExternalMessage(msg)

# -------------------------
# --- External messages ---
# -------------------------

def handleExternalMessage(msg):
    from_chat_id = msg['chat']['id']
    to_chat_id = JEKA_DJ_CHAT_ID
    msg_id = msg['message_id']

    apiSendMsg(to_chat_id, 'chat_id: {}. msg_id: {}'.format(from_chat_id, msg_id))
    apiForwardMsg(from_chat_id, to_chat_id, msg_id)
    print('[+] handleExternalMessage. from:{}. to:{}. text:{}'.format(from_chat_id, to_chat_id, msg['text']))

# ---------------------
# --- Baby messages ---
# ---------------------

def babyHandle(msg):
    chicks = {
        # 'Megan Fox' : 'https://pp.userapi.com/c840322/v840322120/45c9b/oiJ4RHqVYTI.jpg',
        # 'Jessica Alba' : 'https://pp.userapi.com/c621705/v621705776/8224c/kNfdB8EJeXM.jpg',
        # 'Jessica Alba 2' : 'https://pp.userapi.com/c840227/v840227855/8eea9/goF2Tcrk-To.jpg',
        # 'Sasha Grey' : 'https://pp.userapi.com/c621511/v621511163/6a44e/NXEPY7GXl5c.jpg',
        # 'Scarlett Johansson' : 'https://sun9-8.userapi.com/c840520/v840520285/6a6db/qxI7cbg5mjU.jpg',
        # 'Margot Robbie' : 'https://sun9-9.userapi.com/c840426/v840426620/6b540/zPEXaRUC2ZQ.jpg',
        # 'Jennifer Lawrence' : 'https://pp.userapi.com/c621511/v621511648/6cc89/yvQ1cIvO5FE.jpg',
        # 'Amber Heard' : 'https://pp.userapi.com/c840221/v840221545/8f505/ey9_lJAWLC0.jpg',
        # 'Miranda Kerr' : 'https://pp.userapi.com/c621706/v621706850/7dc15/WlA3cQlL0qY.jpg',
        # 'Rihanna' : 'https://sun9-7.userapi.com/c840526/v840526105/6ab69/34LcCIQdzqE.jpg',
        # 'Lizzy Caplan' : 'https://pp.userapi.com/c840325/v840325631/6e827/BchgGnPyfis.jpg',
        # 'Emma Watson' : 'https://sun9-5.userapi.com/c840433/v840433317/6cafd/aHgSpcrSTaU.jpg',
        # 'Rachel Nicols' : 'https://pp.userapi.com/c840331/v840331377/7073d/L6SdkSOr04M.jpg',
        # 'Fat Man' : 'https://pp.userapi.com/c840127/v840127496/8ffd9/X8IcN9CV-aA.jpg',

        # 'Emily Ratajkowski': 'https://pp.userapi.com/c849420/v849420949/6ba61/tM4djwe3uBE.jpg',
        # 'Rihanna 2' : 'https://pp.userapi.com/c849420/v849420426/6d6d7/Tdvtt-mIoDo.jpg',
        # 'Irina Shayk' : 'https://pp.userapi.com/c849420/v849420426/6d6f6/YmZQe1uMG7w.jpg',
        # 'Candice Swanepoel' : 'https://pp.userapi.com/c849420/v849420949/6ba1a/hR1m9p9Cfhg.jpg',
        # 'Mila Kunis' : 'https://pp.userapi.com/c850236/v850236810/24ed4/aqRvgk6Y5jM.jpg',
        # 'Nina Dobrev' : 'https://pp.userapi.com/c850236/v850236810/24eed/zNFQUK63Obo.jpg',

        # 'Kaley Cuoco' : 'https://pp.userapi.com/c849536/v849536635/6d2b1/AmMt9Wt6CJw.jpg',
        # 'Anna Kendrick' : 'https://pp.userapi.com/c845523/v845523102/e9901/DeSn09KLGh4.jpg',
        'Laura Vandervoort' : 'https://pp.userapi.com/c846322/v846322635/e634c/ybxh7VxCR2w.jpg',
        'Laura Vandervoort 2' : 'https://pp.userapi.com/c849124/v849124555/74ee6/bG138EgEt2s.jpg',
        # 'Sarah Jones' : 'https://pp.userapi.com/c847016/v847016635/e39f2/CmWvYPl9WR0.jpg',
        'Elisha Cuthbert' : 'https://pp.userapi.com/c845523/v845523102/e9915/LnL4P0D1zSE.jpg'
    }

    chat_id = msg['chat']['id']
    baby_name, photo_url = random.choice(list(chicks.items()))

    # remove number rom the end
    splitted = baby_name.strip().rsplit(' ', 1)
    if len(splitted) == 2 and splitted[1].isdigit():
        baby_name = splitted[0]

    apiSendPhoto(chat_id, photo_url, caption=baby_name, explicit_return=True)

# ------------------
# --- Bed linnin ---
# ------------------

def scheduleHandle(msg):

    chat_id = msg['chat']['id']

    msg = "*Расписание смены постельного белья:*\n"
    msg += "пн: 9:00-12:00, 15:00-17:30\n"
    msg += "ср: 9:00-12:00, 15:00-17:30\n"
    msg += "чт: 9:00-12:00, 15:00-17:30\n"
    msg += "пт: 9:00-12:00, 14:00-16:30\n"
    msg += "*Душ:*\n"
    msg += "6:00-12:00 15:00-24:00\n"
    msg += "Санитарный день:\n"
    msg += "10:00-18:00 (6ф - четверг, 6м - среда)\n\n"
    msg += "`Если расписание изменилось, напишите боту в личку`"

    apiSendMsg(chat_id, msg, parse_mode='Markdown')

# ----------------
# --- The Mall ---
# ----------------

def sellHandle(msg):

    chat_id = msg['chat']['id']

    # Get optional args
    try:
        user = msg['from']
        text = msg['text']
    except KeyError:
        apiSendMsg(JEKA_DJ_CHAT_ID, 'ERROR: sellHandle: {}'.format(msg))
        return True

    # check text
    splitted = text.split(' ', 1)

    if not (splitted[0] == '/sell' or splitted[0] == '/sell@CombatDetectorBot'):
        return False
    if len(splitted) != 2 or not splitted[1].strip():
        msg = '/sell - позволяет выставить товар на продажу\n'
        msg += 'Формат: /sell \[описание]\n'
        msg += 'Пример: /sell Микроволновка 1000р.\n\n'
        msg += 'Возможно использование Markdown разметки, [подробнее](https://core.telegram.org/bots/api#markdown-style)\n'
        msg += 'Пример: /sell \*Микроволновка\* 1000р. \[Подробнее](https://www.eldorado.ru/cat/detail/71073407/)\n'
        msg += 'Результат: /sell *Микроволновка* 1000р. [Подробнее](https://www.eldorado.ru/cat/detail/71073407/)'
        apiSendMsg(chat_id, msg, parse_mode='Markdown', disable_web_page_preview=True)
        return True

    description = splitted[1]

    # Get args
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

    return True
        
def buyHandle(msg):

    chat_id = msg['chat']['id']

    session = new_session()
    entries = session.query(CombotMall).all()
    session.close()

    if len(entries) > 0:

        message = ''
        for entry in entries:

            fixed_username = ''
            for c in entry.seller_username:
                if c == '_':
                    fixed_username += '\\'
                fixed_username += c

            if msg['chat']['type'] == 'private':
                linked_uid = "[{}](tg://user?id={})".format(entry.seller_id, entry.seller_id)
            else:
                linked_uid = entry.seller_id
            message += 'sellid: {}. uid: {}.'.format(entry.id, linked_uid)

            if fixed_username != 'UNKNOWN':
                if msg['chat']['type'] == 'private':
                    seller_username = '@{}'.format(fixed_username)
                else:
                    seller_username = fixed_username
                message += ' uname: {}.'.format(seller_username)

            message += '\n{}\n\n'.format(entry.description)

            

        if msg['chat']['type'] != 'private':
            message += '`Используйте в приватном чате для отображения ссылок на аккаунты продавцов.`'
    else:
        message = 'No entries'

    res = apiSendMsg(chat_id, message, parse_mode='Markdown', disable_web_page_preview=True)
    if not res:
        apiSendMsg(chat_id, message, disable_web_page_preview=True)

    return

def editHandle(msg):
    try:
        user = msg['from']
    except KeyError:
        apiSendMsg(JEKA_DJ_CHAT_ID, 'ERROR: delsellHandle: {}'.format(msg))
        return

    seller_id = user['id']
    chat_id = msg['chat']['id']
    text = msg['text']
    cmd_obj = Command(text)

    session = new_session()
    entry = session.query(CombotMall).filter(CombotMall.id == int(cmd_obj.param)).first()
    session.close()

    if not entry:
        apiSendMsg(chat_id, 'Неизвестный идентификатор')
        return

    if seller_id not in [entry.seller_id, 239745097]:
        apiSendMsg(chat_id, 'У вас нет прав удалять позиции других людей')
        return

    session = new_session()
    session.query(CombotMall).filter(CombotMall.id == int(cmd_obj.param)).update({CombotMall.description: cmd_obj.value})
    session.commit()
    session.close()

    apiSendMsg(chat_id, 'Done.')

    return

        
def delsellHandle(msg):

    try:
        user = msg['from']
    except KeyError:
        apiSendMsg(JEKA_DJ_CHAT_ID, 'ERROR: delsellHandle: {}'.format(msg))
        return

    seller_id = user['id']
    chat_id = msg['chat']['id']
    text = msg['text']
    cmd_obj = Command(text)

    if not (cmd_obj.is_param() and cmd_obj.param.isdigit()):
        msg = "/delsell - команда для удаления позиций из магазина\n"
        msg += "Формат: /delsell [индетификатор позиции (sellid)]\n"
        msg += "Например: /delsell 7"
        apiSendMsg(chat_id, msg)
        return


    session = new_session()
    entry = session.query(CombotMall).filter(CombotMall.id == int(cmd_obj.param)).first()
    session.close()

    if not entry:
        apiSendMsg(chat_id, 'Неизвестный идентификатор')
        return

    if seller_id not in [entry.seller_id, 239745097]:
        apiSendMsg(chat_id, 'У вас нет прав изменять позиции других людей')
        return

    session = new_session()
    session.query(CombotMall).filter(CombotMall.id == int(cmd_obj.param)).delete()
    session.commit()
    session.close()

    apiSendMsg(chat_id, 'Done.')

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
            cmd_obj = Command(msg['text'])

            if cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/buy'):
                buyHandle(msg)
            elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/ping'):
                handlePing(msg)
            elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/baby'):
                babyHandle(msg)
            elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/schedule'):
                scheduleHandle(msg)

            elif chat_id in OBWAGA_CHAT_IDS:
                if combatFinder(msg['text']) == True and '@CombatDetectorBot' not in msg['text']:
                    handleCombotNotification(msg)
                elif msg['text'] == '/pin@CombatDetectorBot' or msg['text'] == '/pin':
                    handlePin(msg)
                elif msg['text'] == '/unpin@CombatDetectorBot' or msg['text'] == '/unpin':
                    handleUnpin(msg)
                elif cmd_obj.is_single_cmd() and cmd_obj.is_cmd_eq('/hw'):
                    hwHandle(msg)

            else:
                if (msg['text'].find('/sell') == 0) and sellHandle(msg):
                    pass
                elif cmd_obj.is_cmd_eq('/delsell'):
                    delsellHandle(msg)
                elif cmd_obj.is_cmd_eq('/edit') and cmd_obj.is_param_semicolon():
                    editHandle(msg)

                # others
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
            print('--------------------')
            try:
                traceback.print_exc(e)
                exc_trace = traceback.format_exc(e)
                apiSendMsg(JEKA_DJ_CHAT_ID, exc_trace)
            except Exception:
                pass
            print('--------------------')
            time.sleep(3)
