from __future__ import unicode_literals, absolute_import, print_function

import random
from app.api import API


class HW:
    _hw = [
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

    _candidates = [
        ', бро, хватит уже', ', бро, заебал',
        ', бро, заебал с этой херней', ', заебал, реально',
        ', прекрати', ', твоюжмать, хватит уже!'
    ]

    @staticmethod
    def do(msg):
        if random.randint(0, 1) != 0:
            return

        if random.randint(0, 1) == 0:
            _from = msg['from']
            name = _from['first_name'] or _from['username'] or _from['last_name'] or 'Эй'
            resp_msg = name + random.choice(HW._candidates)
        
        else:
            resp_msg = 'Huli Wi {}'.format(random.choice(HW._hw))
        
        API.sendMsg(msg['chat']['id'], resp_msg)

