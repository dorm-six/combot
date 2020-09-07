from __future__ import unicode_literals, absolute_import, print_function

from app.api import API


class Schedule:

    @staticmethod
    def do(msg):
        def get_msg():
            msg = "*Расписание смены постельного белья:*\n"

            msg += "пн-ср: 09:00-12:00, 15:00-17:00\n"
            msg += "пт: 09:00-12:00, 14:00-16:00\n\n"

            msg += "*Душ:*\n"
            msg += "6ф: 06:00-12:00, 15:00-24:00\n"
            msg += "6м: 06:00-09:00, 12:00-24:00\n"
            msg += "Санитарный день (не работает):\n"
            msg += "10:00-18:00 (6ф - четверг, 6м - среда)\n\n"

            msg += "*Расписание работы паспортного стола:*\n"
            msg += "пн-чт: 09:00-17:30\n"
            msg += "пт: 09:00-16:30\n"
            msg += "обед: 13:00-13:30\n\n"

            msg += "*Коменда:*\n"
            msg += "пн-чт: 09:00-17:30\n"
            msg += "пт: 09:00-16:30\n"
            msg += "обед: 13:00-13:30\n\n"

            msg += "*Военкомат:*\n"
            msg += "пн: 10:00-17:00\n"
            msg += "ср: 10:00-17:00\n"
            msg += "пт: 10:00-13:00\n"
            msg += "обед: 13:00-13:45\n"
            msg += "Если с повесткой, то в любой день можешь приходить\n\n"

            msg += "*Гости:*\n"
            msg += "по будням: вход с 14 до 22, выход до 23.\n"
            msg += "по выходных: вход с 10 до 22, выход до 23.\n"
            msg += "*ВРЕМЕННО НЕ ПУСКАЮТ*\n\n"

            msg += "`Если расписание изменилось, напишите боту в личку`"

            return msg

        chat_id = msg['chat']['id']
        API.sendMsg(chat_id, get_msg(), parse_mode='Markdown')
