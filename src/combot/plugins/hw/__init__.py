import random
from ...bot import Bot


# I don't expect these to change. The meme it refers to is long forgotten,
# so no need to externalize the strings.
_hw = [
    "делаете",
    "пидоры то такие",
    "не учитесь",
    "бухаете",
    "пишите",
    "творите",
    "кушаете",
    "не спите",
    "можете?",
    "имеете против меня?",
    "такие динозавры",
    "опять спамите эту хуйню",
    "курите?",
    "заебываете меня!!",
    "?? не пойти ли вам н@&yi?" "такие дерзские?",
    "комбатов не боитесь",
    "выселения не боитесь",
    "отчисления не боитесь",
    "удивляетесь",
    "доебались",
    "приперлись, вас никто не ждал здесь",
    "? почему вы ? да идите нахуй просто! Я бот, мне можно все.",
    "понтуетесь?",
    "шумите!!!",
    "хотели-то?",
]

_candidates = [
    ", бро, хватит уже",
    ", бро, заебал",
    ", бро, заебал с этой херней",
    ", заебал, реально",
    ", прекрати",
    ", твоюжмать, хватит уже!",
]


def handle(bot: Bot, msg: dict):
    if random.randint(0, 1) != 0:
        return

    if random.randint(0, 1) == 0:
        _from = msg["from"]
        name = _from.get("username", "")
        name = (
            "@" + name
            if name
            else (_from.get("first_name") + " " + _from.get("last_name", "")).strip()
        )
        name = name or "Эй"
        resp_msg = name + random.choice(_candidates)
    else:
        resp_msg = "Huli Wi {}".format(random.choice(_hw))

    bot.send_message(msg["chat"]["id"], resp_msg)
