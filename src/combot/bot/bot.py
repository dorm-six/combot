import abc
import logging
import random
import string
import traceback
from collections import defaultdict
from typing import Optional, Callable, Iterable

import requests

from .models import (
    PinnedMsg,
    MediaGroupMessage,
)
from .utils import pretty_json
from ..db.session import dbsession


class UnexpectedTelegramResponseCode(Exception):
    def __init__(
        self, method: str, request_id: str, params: dict, code: int, response_text: str
    ):
        self.method = method
        self.request_id = request_id
        self.params = params
        self.code = code
        self.response_text = response_text
        super().__init__(
            f"{method}#{request_id} returned code {code}\n\n"
            f"Parameters: {pretty_json(params)}\n\n"
            f"Response: {response_text}"
        )


class UnexpectedTelegramResponseType(Exception):
    def __init__(self, method: str, request_id: str, params: dict, response_text: str):
        self.method = method
        self.request_id = request_id
        self.params = params
        self.response_text = response_text
        super().__init__(
            f"{method}#{request_id} response is not JSON serializable\n\n"
            f"Parameters: {pretty_json(params)}\n\n"
            f"Response: {response_text}"
        )


class Bot(abc.ABC):
    public_id_offset = -1000000000000

    def __init__(self, api_key: str, superuser_id: int, proxy=None):
        self._api_key = api_key
        self._proxy = proxy
        self._superuser_id = superuser_id
        self._update_offset = 0
        self._logger = logging.getLogger(
            f"{self.__class__.__name__}#{api_key.split(':', 2)[0]}"
        )
        self._session: Optional[requests.Session] = None
        self._pre_hooks: dict[str, list[Callable[[dict], None]]] = defaultdict(list)
        self._post_hooks: dict[str, list[Callable[[dict, dict], None]]] = defaultdict(
            list
        )
        self._configure_requests_session()
        self._update_me()
        self._username = self._me["username"]
        self._logger.debug(f"Bot @{self._username} initialized")

    def _configure_requests_session(self) -> None:
        if self._session:
            self._logger.debug("Tried to reconfigure session for some reason?")
            return
        self._logger.debug("Configuring session")
        self._session = requests.Session()
        if self._proxy:
            self._session.proxies = {"http": self._proxy, "https": self._proxy}
            self._logger.debug(f"Session proxies: {self._session.proxies}")
        self._logger.debug("Session configured")

    def register_pre_hook(self, method: string, callback: Callable[[dict], None]):
        self._pre_hooks[method].append(callback)

    def register_post_hook(
        self, method: string, callback: Callable[[dict, dict], None]
    ):
        self._post_hooks[method].append(callback)

    def _api_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self._api_key}/{method}"

    def _process_telegram_response(
        self,
        response: requests.Response,
        method: str,
        request_id: str,
        params: dict = None,
    ) -> Optional[dict]:
        if response.status_code != 200:
            raise UnexpectedTelegramResponseCode(
                method=method,
                request_id=request_id,
                params=params,
                code=response.status_code,
                response_text=response.text,
            )

        try:
            r = response.json()
        except Exception as e:
            raise UnexpectedTelegramResponseType(
                method=method,
                request_id=request_id,
                params=params,
                response_text=response.text,
            ) from e

        if "ok" in r and not r["ok"]:
            e = (
                f"{method}#{request_id} failed\n\n"
                f"Parameters: {pretty_json(params)}\n\n"
                f"Response: {pretty_json(r)}"
            )
            self._logger.error(e)
            self.send_message(chat_id=self._superuser_id, text=e)
        return r

    def _call_method(
        self, get_response: Callable, method: str, params: dict = None, **kwargs
    ) -> dict:
        url = self._api_url(method)
        request_id = "".join(random.choices(string.ascii_letters, k=7))

        if method in self._pre_hooks:
            for m in self._pre_hooks[method]:
                m(params)

        self._logger.debug(f"{method}#{request_id}: {pretty_json(params)}")

        result = self._process_telegram_response(
            response=get_response(url, params=params, **kwargs),
            method=method,
            request_id=request_id,
            params=params,
        )

        if method in self._post_hooks:
            for m in self._post_hooks[method]:
                m(params, result)

        self._logger.debug(
            f"{method}#{request_id} succeeded\n\n" f"Response: {pretty_json(result)}"
        )

        return result

    def _get_method(self, method: str, params: dict = None, **kwargs) -> dict:
        def get_response(url: str, params: dict, **kwargs):
            return self._session.get(url, params=params, **kwargs)

        return self._call_method(get_response, method, params, **kwargs)

    def _post_method(self, method: str, params: dict, **kwargs) -> dict:
        def get_response(url: str, params: dict, **kwargs):
            return self._session.post(url, json=params, **kwargs)

        return self._call_method(get_response, method, params, **kwargs)

    def _update_me(self) -> None:
        self._me = self._get_method("getMe")["result"]
        self._logger.info(pretty_json(self._me))

    @property
    def me(self):
        return self._me

    def answer_callback_query(self, query_id: int, text: str, alert=False) -> dict:
        return self._post_method(
            "answerCallbackQuery",
            params={"callback_query_id": query_id, "text": text, "show_alert": alert},
        )

    def edit_message_reply_markup(
        self, chat_id: int, message_id: int, reply_markup: dict
    ) -> dict:
        return self._post_method(
            "editMessageReplyMarkup",
            params={
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": reply_markup,
            },
        )

    def edit_message_text(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: str = "Markdown",
        reply_markup: dict = None,
    ) -> dict:
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        if reply_markup:
            data["reply_markup"] = reply_markup
        return self._post_method("editMessageText", params=data)

    @abc.abstractmethod
    def delete_deferred(
        self, chat_ids: list[int], message_ids: list[int], delay: int = 0
    ) -> dict:
        pass

    def send_message(
        self,
        chat_id: int,
        text: str,
        reply_to: Optional[int] = None,
        parse_mode: str = "Markdown",
        reply_markup: dict = None,
        no_preview=False,
        countdown: int = None,
        remove_reply=True,
    ) -> dict:
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": no_preview,
        }
        if reply_markup:
            data["reply_markup"] = reply_markup
        if reply_to:
            data["reply_to_message_id"] = reply_to
        result = self._post_method("sendMessage", params=data)

        if result["ok"] and countdown is not None:
            ids = [result["result"]["message_id"]]
            if remove_reply:
                ids.append(reply_to)
            self.delete_deferred(chat_ids=ids, message_ids=ids, delay=countdown)
        return result

    def send_photo(
        self,
        chat_id: int,
        photo: str,
        caption: str,
        reply_to: Optional[int] = None,
        parse_mode: str = "Markdown",
        show_caption_above_media: bool = False,
        has_spoiler: bool = False,
        disable_notification: bool = False,
        protect_content: bool = False,
        reply_markup: dict = None,
        no_preview=False,
        countdown: int = None,
        remove_reply: bool = True,
    ) -> dict:
        data = {
            "chat_id": chat_id,
            "photo": photo,
            "text": caption,
            "parse_mode": parse_mode,
            "disable_web_page_preview": no_preview,
            "has_spoiler": has_spoiler,
            "show_caption_above_media": show_caption_above_media,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
        }
        if reply_markup:
            data["reply_markup"] = reply_markup
        if reply_to:
            data["reply_to_message_id"] = reply_to
        result = self._post_method("sendPhoto", params=data)

        if result["ok"] and countdown is not None:
            ids = [result["result"]["message_id"]]
            if remove_reply:
                ids.append(reply_to)
            self.delete_deferred(chat_ids=ids, message_ids=ids, delay=countdown)
        return result

    def forward_message(self, chat_id: int, msg_id: int, to_id: int) -> dict:
        return self._post_method(
            "forwardMessage",
            params={"chat_id": to_id, "from_chat_id": chat_id, "message_id": msg_id},
        )

    def forward_messages(self, chat_id: int, msg_ids: Iterable[int], to_id: int):
        return self._post_method(
            "forwardMessages",
            params={
                "chat_id": to_id,
                "from_chat_id": chat_id,
                "message_ids": list(msg_ids),
            },
        )

    def delete_message(self, chat_id: int, msg_id: int) -> dict:
        return self._post_method(
            "deleteMessage",
            params={"chat_id": chat_id, "message_id": msg_id},
        )

    def get_chat_admins(self, chat_id: int) -> dict:
        return self._post_method("getChatAdministrators", params={"chat_id": chat_id})

    def get_chat_member(self, chat_id: int, user_id: int) -> dict:
        return self._post_method(
            "getChatMember",
            params={"chat_id": chat_id, "user_id": user_id},
        )

    def restrict_chat_member(
        self, chat_id: int, user_id: int, permissions: dict, until_date: int
    ) -> dict:
        return self._post_method(
            "restrictChatMember",
            params={
                "chat_id": chat_id,
                "user_id": user_id,
                "permissions": permissions,
                "until_date": until_date,
            },
        )

    def send_media_group(self, chat_id: int, media_group: dict) -> dict:
        return self._post_method(
            "sendMediaGroup",
            params={"chat_id": chat_id, "media": media_group},
        )

    @dbsession
    def pin(
        self, msg: dict, pin_id: str = None, notify=True, session=None
    ) -> Optional[dict]:
        chat_id = msg["chat"]["id"]
        message_id = msg["message_id"]
        if msg["chat"]["type"] == "private":
            return None

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "disable_notification": not notify,
        }
        result = self._post_method("pinChatMessage", params=data)
        if result["ok"]:
            session.add(
                PinnedMsg(
                    chat_id=chat_id, message_id=message_id, pin_id=pin_id, pinned=True
                )
            )

        return result

    @dbsession
    def unpin(
        self, chat_id: int, message_id: int = None, pin_id: str = None, session=None
    ) -> dict:
        messages = []
        message_ids = []
        if message_id is not None:
            message_ids.append(message_id)
        elif pin_id is not None:
            messages = (
                session.query(PinnedMsg)
                .filter(
                    PinnedMsg.chat_id == chat_id,
                    PinnedMsg.pin_id == pin_id,
                    PinnedMsg.pinned == True,
                )
                .all()
            )
            message_ids = [m.message_id for m in messages]

        if not message_ids:
            return self._post_method("unpinChatMessage", params={"chat_id": chat_id})

        successfully_unpinned = set()
        for message_id in message_ids:
            resp = self._post_method(
                "unpinChatMessage",
                params={"chat_id": chat_id, "message_id": message_id},
            )
            if resp["ok"]:
                successfully_unpinned.add(message_id)

        for m in messages:
            if m.message_id in successfully_unpinned:
                m.pinned = False
                session.add(m)
        session.commit()
        session.flush()

    @dbsession
    def unpin(self, msg: dict, pin_id: str = None, session=None) -> dict:
        return self.unpin(
            chat_id=msg["chat"]["id"],
            message_id=msg["message_id"],
            pin_id=pin_id,
            session=session,
        )

    def finalize_media_group(self, mg: MediaGroupMessage, session=None) -> bool:
        # Provide your own implementation
        return True

    @dbsession
    def media_group_save_handler(self, update: dict, session=None) -> bool:
        if "message" not in update:
            return False

        msg = update["message"]
        chat_id = msg["chat"]["id"]
        if "media_group_id" not in msg:
            unfinalized_media_groups = (
                session.query(MediaGroupMessage)
                .filter_by(chat_id=chat_id, finalized=False)
                .all()
            )

            for mg in unfinalized_media_groups:
                mg.finalized = self.finalize_media_group(mg)
                session.add(mg)

            session.commit()
            session.flush()
            return False

        mgm = MediaGroupMessage(
            chat_id=chat_id,
            media_group_id=msg["media_group_id"],
            msg_id=msg["message_id"],
            caption=msg["caption"] if "caption" in msg else None,
        )

        # TODO Catch existing pk
        session.add(mgm)
        session.commit()
        session.flush()
        return True

    def handle(self, update: dict) -> None:
        self.media_group_save_handler(update)

    def get_updates(self, timeout=60, cutting_index=50):
        payload = {
            "allowed_updates": ["message"],
            "offset": self._update_offset + 1,
            "timeout": max(timeout, 30) - 5,
        }

        try:
            response = self._get_method("getUpdates", params=payload, timeout=timeout)
            if "ok" in response:
                result = response["result"]

                if self._update_offset == 0 and len(result) > cutting_index:
                    self._update_offset = result[cutting_index]["update_id"]
                    result = result[:cutting_index]
                return result
            else:
                raise Exception("getUpdates failed")
        except Exception as e:
            traceback.print_exc()
        return []

    def get_and_process_updates(self, timeout=60, cutting_index=50):
        result = self.get_updates(timeout=timeout, cutting_index=cutting_index)
        for update in result:
            if update["update_id"] + 1 > self._update_offset:
                self._update_offset = update["update_id"] + 1

            try:
                self.handle(update)
            except Exception as e:
                traceback.print_exc()
                log = traceback.format_exc()

                crashed_chat = "<UNKNOWN>"
                if "message" in update:
                    crashed_chat = str(update["message"]["chat"]["id"])
                if "callback_query" in update:
                    crashed_chat = str(
                        update["callback_query"]["message"]["chat"]["id"]
                    )

                self.send_message(
                    self._superuser_id, f"Crash in {crashed_chat}:\n```{log}```"
                )
                raise e
