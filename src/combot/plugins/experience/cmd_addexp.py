from ...bot import Bot
from ...bot.utils import extract_user
from . import add_experience


def cmd_addexp(bot: Bot, msg: dict) -> None:
    msg_id = msg["message_id"]
    chat_id = msg["chat"]["id"]
    from_id = msg["from"]["id"]
    is_private = msg["chat"]["type"] == "private"
    if is_private:
        return

    admins = bot.get_chat_admins(chat_id)
    if not admins["ok"]:
        bot.send_message(
            chat_id, "Не удалось получить список администраторов.", reply_to=msg_id
        )
        return

    admin_ids = [admin["user"]["id"] for admin in admins["result"]]

    if from_id not in admin_ids:
        bot.send_message(
            chat_id,
            "Вы не администратор. В эту сторону хвостиками лучше не хитрить.",
            reply_to=msg_id,
            countdown=10,
        )
        return

    if "reply_to_message" not in msg:
        bot.send_message(
            chat_id,
            "Но кому добавлять опыт? Ответьте командой на сообщение пользователя.",
            reply_to=msg_id,
            countdown=10,
        )
        return

    text = msg["text"]
    arguments = text.split(" ")[1:]
    exp_to_add = None
    try:
        exp_to_add = int(arguments[0])
    except ValueError as e:
        pass
    if exp_to_add is None:
        bot.send_message(
            chat_id,
            "Формат команды: `/addexp <количество очков опыта>`",
            reply_to=msg_id,
            countdown=10,
        )
        return

    rtm = msg["reply_to_message"]
    user_id, _, _, full_name, _ = extract_user(rtm)

    if user_id < 0 or rtm["from"]["is_bot"]:
        bot.send_message(
            chat_id,
            "У автора сообщения не может быть опыта.",
            reply_to=msg_id,
            countdown=10,
        )
        return

    add_experience(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        points=exp_to_add,
        fullname=full_name,
        silent=True,
        timed=False,
    )
    bot.send_message(chat_id, "Очки опыта добавлены.", reply_to=msg_id, countdown=300)
    return
