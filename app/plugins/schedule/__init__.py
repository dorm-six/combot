from __future__ import unicode_literals, absolute_import, print_function

from app.api import API


class Schedule:

    def do(msg):
        def get_msg():
            msg = "*Расписание смены постельного белья:*\n"
            msg += "пн: 9:00-12:00, 15:00-17:30\n"
            msg += "ср: 9:00-12:00, 15:00-17:30\n"
            msg += "чт: 9:00-12:00, 15:00-17:30\n"
            msg += "пт: 9:00-12:00, 14:00-16:30\n\n"

            msg += "*Душ:*\n"
            msg += "6:00-12:00, 15:00-24:00\n"
            msg += "Санитарный день (не работает):\n"
            msg += "10:00-18:00 (6ф - четверг, 6м - среда)\n\n"

            msg += "*Коменда:*\n"
            msg += "пн-чт: 9:00-17:30\n"
            msg += "пт: 9:00-16:30\n"
            msg += "обед: 13:00-13:30\n\n"

            msg += "`Если расписание изменилось, напишите боту в личку`"

            return msg

        chat_id = msg['chat']['id']
        API.sendMsg(chat_id, get_msg(), parse_mode='Markdown')
