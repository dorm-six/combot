import contextlib
import json
import re
from typing import NamedTuple, Optional

from .models import ChatInfo, UserInfo


def escape_md(text: str) -> str:
    r = r"([_*\[\]\(\)\~`])"
    result = re.sub(r, r"\\\g<1>", text)
    return result


class TgUser(NamedTuple):
    id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]


def extract_user(update):
    f = update["from"]
    return TgUser(
        id=f["id"],
        first_name=f["first_name"],
        last_name=f.get("last_name", ""),
        username=f.get("username", ""),
    )


@contextlib.contextmanager
def user_and_chat_info(update, session):
    chat_info: Optional[ChatInfo] = None
    if "message" in update and update["message"]["chat"]["type"] != "private":
        chat_info = (
            session.query(ChatInfo)
            .filter(ChatInfo.id == update["message"]["chat"]["id"])
            .one_or_none()
        )
        if chat_info is None:
            chat_info = ChatInfo(id=update["message"]["chat"]["id"])
    user = extract_user(update["message"])
    user_info = session.query(UserInfo).filter(UserInfo.id == user.id).one_or_none()
    if user_info is None:
        user_info = UserInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )

    try:
        yield chat_info, user_info, user
    finally:
        if chat_info is not None:
            session.add(chat_info)
        if user_info is not None:
            session.add(user_info)
        session.commit()
        session.flush()


def pretty_json(obj):
    return json.dumps(obj, indent=2, sort_keys=True)
