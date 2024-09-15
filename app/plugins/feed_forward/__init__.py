from sqlalchemy import select

from app.db.session import dbsession
from app.bot import Bot
from app.bot.models import ChatInfo, MediaGroupMessage

from .models import ChatFeed, ForwardedMessage


@dbsession
def forward_media_group(
    bot: Bot, src_chat_id: int, media_group_id: str, dst_chat_id: int, session=None
):
    group_messages = (
        session.query(MediaGroupMessage)
        .filter(
            MediaGroupMessage.chat_id == src_chat_id,
            MediaGroupMessage.media_group_id == media_group_id,
        )
        .all()
    )
    msg_ids = [m.msg_id for m in group_messages]
    bot.forward_messages(src_chat_id, msg_ids, dst_chat_id)
    return msg_ids


@dbsession
def forward_to_bound_channel(bot: Bot, chat_id: int, msg: dict, session=None):
    chat_feed = (
        session.query(ChatFeed).filter(ChatFeed.chat_id == chat_id).one_or_none()
    )
    if chat_feed is None:
        return (
            False,
            "Неизвестный чат",
            None,
        )

    if chat_feed.feed_channel_id is None:
        return (
            False,
            f"Привяжите канал командой /bind@{bot.me['username']} `<id канала>`",
            None,
        )

    # Each gallery is presented to a bot as multiple messages, each with its own ID.
    # Each media-containing message contains a "media_group" information, basically
    # multiple IDs of media files of different quality.
    #
    # Forwarding a single message from the gallery will forward that particular media.
    # To preserve the original gallery, `forwardMessages` method should be used instead.
    #
    # If we assume that gallery messages will not be interleaved with other messages,
    # which seems reasonable enough, we could leverage `forwardMessages`. The only
    # limitation is that the caller should not act on the first message of the gallery.

    if "media_group_id" in msg:
        mgm = session.execute(
            select(MediaGroupMessage).join(
                ForwardedMessage,
                MediaGroupMessage.chat_id == ForwardedMessage.chat_id,
                MediaGroupMessage.msg_id == ForwardedMessage.message_id,
            )
        ).all()
        if mgm:
            return False, "Это сообщение уже переслано в канал.", 10

        msg_ids = forward_media_group(
            bot,
            chat_id,
            msg["media_group_id"],
            chat_feed.feed_channel_id,
            session=session,
        )
        for msg_id in msg_ids:
            session.add(ForwardedMessage(chat_id=chat_id, message_id=msg_id))
        session.commit()
        session.flush()
        return None, "Сообщения успешно пересланы.", None

    forward_msg_id = msg["message_id"]
    forwarded = (
        session.query(ForwardedMessage)
        .filter(
            ForwardedMessage.chat_id == chat_id,
            ForwardedMessage.message_id == forward_msg_id,
        )
        .one_or_none()
    )

    if forwarded:
        return False, "Это сообщение уже переслано в канал.", 10
    else:
        result = bot.forward_message(chat_id, forward_msg_id, chat_feed.feed_channel_id)
        if not result["ok"]:
            return (
                False,
                "Не удалось переслать сообщение в привязанный канал. Проверьте, есть ли у бота необходимые права.",
                None,
            )
        else:
            forwarded = ForwardedMessage(chat_id=chat_id, message_id=forward_msg_id)
            session.add(forwarded)
            session.commit()
            return True, "Сообщение успешно переслано.", 5


def pinned_message_handler(bot: Bot, update: dict, chat_info: ChatInfo) -> bool:
    if (
        "message" not in update
        or update["message"]["chat"]["type"] == "private"
        or "pinned_message" not in update["message"]
    ):
        return False

    forward_to_bound_channel(bot, chat_info.id, update["message"]["pinned_message"])
    return True


def channel_command_handler(bot: Bot, update: dict, chat_info: ChatInfo, cmd: str):
    if cmd != "/channel":
        return False

    msg = update["message"]
    msg_id = msg["message_id"]
    from_id = msg["from"]["id"]

    admins = bot.get_chat_admins(chat_info.id)
    if not admins["ok"]:
        bot.send_message(
            chat_info.id, "Не удалось получить список администраторов.", reply_to=msg_id
        )
        return

    admins = admins["result"]
    admin_ids = [admin["user"]["id"] for admin in admins]
    if from_id not in admin_ids:
        return

    if "reply_to_message" not in msg:
        bot.send_message(
            chat_info.id,
            "Используйте команду вместе с реплаем на сообщение, которое нужно переслать.",
        )
        return True

    reply_to = update["message"]["reply_to_message"]
    _, message, countdown = forward_to_bound_channel(bot, chat_info.id, reply_to)

    bot.send_message(chat_info.id, message, reply_to=msg_id, countdown=countdown)
    return True
