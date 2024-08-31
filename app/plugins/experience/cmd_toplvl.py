from datetime import datetime, timezone, timedelta

from app.bot import Bot
from app.bot.utils import escape_md
from app.db.session import dbsession
from .data import calculate_level
from .models import ChatExperience


@dbsession
def cmd_toplvl(bot: Bot, msg: dict, session=None) -> None:
    msg_id = msg["message_id"]
    chat_id = msg["chat"]["id"]
    is_private = msg["chat"]["type"] == "private"
    if is_private:
        bot.send_message(chat_id, "И кто с кем здесь должен соревноваться?")
        return

    rating = (
        session.query(ChatExperience)
        .filter(
            ChatExperience.chat_id == chat_id,
            datetime.now(timezone.utc) - ChatExperience.last_exp_update
            < timedelta(days=90),
        )
        .order_by(ChatExperience.experience.desc())
        .limit(10)
        .all()
    )

    if len(rating) == 0:
        message = "Рейтинг пуст."
    else:
        message = "*Рейтинг:*"
        for p in rating:
            level, level_name, till_next = calculate_level(p.experience)
            message += f"\n`{level + 1}` *{level_name}* {escape_md(p.last_user_name)} `({p.experience}/{till_next})`"
    bot.send_message(chat_id, message, reply_to=msg_id, countdown=300)
