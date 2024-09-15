from ...bot import Bot


_pin_id = "combat_protector"


def pin(bot: Bot, msg: dict):
    chat_id = msg["chat"]["id"]
    msg = bot.send_message(chat_id=chat_id, text="КОМБАТЫ")
    if msg["ok"]:
        bot.pin(chat_id, msg_id=msg["result"]["message_id"], pin_id=_pin_id)


def unpin(bot: Bot, msg: dict):
    chat_id = msg["chat"]["id"]
    bot.unpin_by_pin_id(chat_id, pin_id=_pin_id)
    bot.send_message(chat_id=chat_id, text="ОТКРЕПЛЕНО")


def handle(bot: Bot, update: dict, command: str):
    if command == "pin":
        pin(bot, update)
        return True
    elif command == "unpin":
        unpin(bot, update)
        return True
    return False
