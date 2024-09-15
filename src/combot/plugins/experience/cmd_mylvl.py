from ...bot import Bot
from ...db.session import dbsession
from .data import calculate_level
from .models import ChatExperience


@dbsession
def cmd_mylvl(bot: Bot, msg: dict, session=None) -> None:
    msg_id = msg["message_id"]
    chat_id = msg["chat"]["id"]
    from_id = msg["from"]["id"]
    is_private = msg["chat"]["type"] == "private"

    message = "*Ваш статус*: "
    if is_private:
        bot.send_message(chat_id, "Эта команда работает только в чатах.")
        return

    rating = (
        session.query(ChatExperience)
        .filter(ChatExperience.chat_id == chat_id, ChatExperience.user_id == from_id)
        .one_or_none()
    )
    if rating is not None:
        level, level_name, till_next = calculate_level(rating.experience)
        message = f"*{level_name} ({rating.experience}/{till_next})"
    else:
        message += "*кто вы? Ид~*"
    bot.send_message(chat_id, message, reply_to=msg_id, countdown=300)
    return
