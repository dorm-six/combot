from __future__ import unicode_literals, absolute_import, print_function

from app.command import Command
from app.api import API
from app.db import new_session, CombotMall
from app.settings import JEKA_DJ_CHAT_ID

class Mall:

    @staticmethod
    def sell(msg):
        def get_help_message():
            sell_help_msg  = '/sell - позволяет выставить товар на продажу\n'
            sell_help_msg += 'Формат: /sell \[описание]\n'
            sell_help_msg += 'Пример: /sell Микроволновка 1000р.\n\n'
            sell_help_msg += 'Возможно использование Markdown разметки, [подробнее](https://core.telegram.org/bots/api#markdown-style)\n'
            sell_help_msg += 'Пример: /sell \*Микроволновка\* 1000р. \[Подробнее](https://www.eldorado.ru/cat/detail/71073407/)\n'
            sell_help_msg += 'Результат: /sell *Микроволновка* 1000р. [Подробнее](https://www.eldorado.ru/cat/detail/71073407/)'
            return sell_help_msg

        chat_id = msg['chat']['id']

        # Get optional args
        try:
            user = msg['from']
            text = msg['text']
        except KeyError:
            API.sendMsg(JEKA_DJ_CHAT_ID, 'ERROR: sellHandle: {}'.format(msg))
            return True

        # check text
        splitted = text.split(' ', 1)

        if not (splitted[0] == '/sell' or splitted[0] == '/sell@CombatDetectorBot'):
            return False
        if len(splitted) != 2 or not splitted[1].strip():
            API.sendMsg(chat_id, get_help_message(), parse_mode='Markdown', disable_web_page_preview=True)
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
            API.sendMsg(chat_id, 'Too much sell entries for you')
            return

        # create new sell entry
        cm = CombotMall(seller_id=seller_id, seller_username=seller_username, description=description)
        session.add(cm)
        session.commit()
        session.close()

        # success notification
        API.sendMsg(chat_id, 'Done')

        return True

    @staticmethod
    def buy(msg):

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

        res = API.sendMsg(chat_id, message, parse_mode='Markdown', disable_web_page_preview=True)
        if not res:
            API.sendMsg(chat_id, message, disable_web_page_preview=True)

        return

    @staticmethod
    def edit(msg):
        try:
            user = msg['from']
        except KeyError:
            API.sendMsg(JEKA_DJ_CHAT_ID, 'ERROR: delsellHandle: {}'.format(msg))
            return

        seller_id = user['id']
        chat_id = msg['chat']['id']
        text = msg['text']
        cmd_obj = Command(text)

        session = new_session()
        entry = session.query(CombotMall).filter(CombotMall.id == int(cmd_obj.param)).first()
        session.close()

        if not entry:
            API.sendMsg(chat_id, 'Неизвестный идентификатор')
            return

        if seller_id not in [entry.seller_id, JEKA_DJ_CHAT_ID]:
            API.sendMsg(chat_id, 'У вас нет прав удалять позиции других людей')
            return

        session = new_session()
        session.query(CombotMall).filter(CombotMall.id == int(cmd_obj.param)).update({CombotMall.description: cmd_obj.value})
        session.commit()
        session.close()

        API.sendMsg(chat_id, 'Done.')

        return

    @staticmethod
    def delete(msg):

        try:
            user = msg['from']
        except KeyError:
            API.sendMsg(JEKA_DJ_CHAT_ID, 'ERROR: delsellHandle: {}'.format(msg))
            return

        seller_id = user['id']
        chat_id = msg['chat']['id']
        text = msg['text']
        cmd_obj = Command(text)

        if not (cmd_obj.is_param() and cmd_obj.param.isdigit()):
            msg = "/delsell - команда для удаления позиций из магазина\n"
            msg += "Формат: /delsell [индетификатор позиции (sellid)]\n"
            msg += "Например: /delsell 7"
            API.sendMsg(chat_id, msg)
            return

        session = new_session()
        entry = session.query(CombotMall).filter(CombotMall.id == int(cmd_obj.param)).first()
        session.close()

        if not entry:
            API.sendMsg(chat_id, 'Неизвестный идентификатор')
            return

        if seller_id not in [entry.seller_id, JEKA_DJ_CHAT_ID]:
            API.sendMsg(chat_id, 'У вас нет прав изменять позиции других людей')
            return

        session = new_session()
        session.query(CombotMall).filter(CombotMall.id == int(cmd_obj.param)).delete()
        session.commit()
        session.close()

        API.sendMsg(chat_id, 'Done.')

        return