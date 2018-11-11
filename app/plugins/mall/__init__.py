from __future__ import unicode_literals, absolute_import, print_function

from app.api import API
from app.db import new_session, CombotMall


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