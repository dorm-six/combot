import contextlib
import json
import re
from typing import Optional

from .models import ChatInfo, UserInfo


def escape_md(text: str) -> str:
    r = r"([_*\[\]\(\)\~`])"
    result = re.sub(r, r"\\\g<1>", text)
    return result


def extract_user(msg: dict) -> tuple[int, str, str, str, str]:
    f = msg["from"]
    user_id = f["id"]
    first_name = f["first_name"]
    last_name = f.get("last_name", "")
    username = f.get("username", "")
    full_name = f"{first_name} {last_name}".strip()
    return user_id, first_name, last_name, full_name, username


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
        chat_info.handle = update["message"]["chat"].get("username", None)

    user_id, first_name, last_name, _, username = extract_user(update)
    user_info = session.query(UserInfo).filter(UserInfo.id == user_id).one_or_none()
    if user_info is None:
        user_info = UserInfo(id=user_id)
    user_info.first_name = first_name
    user_info.last_name = last_name
    user_info.username = username

    try:
        yield chat_info, user_info
    finally:
        if chat_info is not None:
            session.add(chat_info)
        if user_info is not None:
            session.add(user_info)
        session.commit()
        session.flush()


def pretty_json(obj):
    return json.dumps(obj, indent=2, sort_keys=True)
