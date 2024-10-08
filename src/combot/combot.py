import logging
import os
import traceback
from typing import Iterable

from .bot import Bot
from .bot.utils import user_and_chat_info
from .db.session import dbsession
from .plugins import combat_protector, hw, experience, feed_forward
from .plugins.chicks import Chicks
from .plugins.static_commands import StaticCommands
from .settings import (
    TELEGRAM_TOKEN,
    CHAT_ID_DORM_CHAT,
    CHAT_ID_TEST_CHAT,
)
from .settings import CHAT_ID_SUPERUSER

chicks = Chicks()
static_commands = StaticCommands()


class ComBot(Bot):
    _dorm_chat_ids = []

    def __init__(
        self, api_key: str, superuser_id: int, dorm_chat_ids: list[int], proxy=None
    ):
        self._dorm_chat_ids = dorm_chat_ids
        super().__init__(api_key, superuser_id, proxy)

    def delete_deferred(
        self, chat_id: int, message_ids: Iterable[int], delay: int = 0
    ):
        from .celery import delete_task
        delete_task.apply_async((chat_id, message_ids), countdown=delay)
        pass

    def handle_ping(self, msg, countdown=None):
        chat_id = msg["chat"]["id"]
        self.send_message(chat_id=chat_id, text="I am Alive, сучка", countdown=countdown)

    def handle_personal_message(self, msg):
        from_chat_id = msg["chat"]["id"]
        if from_chat_id < 0:
            # I'm tired of group chats
            return
        to_chat_id = self._superuser_id
        msg_id = msg["message_id"]

        self.send_message(
            chat_id=to_chat_id, text=f"chat_id: {from_chat_id}. msg_id: {msg_id}"
        )
        # TODO Save forwarded => original message ID mapping so that one could reply
        self.forward_message(chat_id=from_chat_id, msg_id=msg_id, to_id=to_chat_id)

    @dbsession
    def handle(self, update: dict, session=None) -> None:
        super().handle(update)

        try:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
        except KeyError:
            return

        with user_and_chat_info(update, session) as uci:
            chat_info, user_info = uci

            # Keep track of experience
            experience.experience_handler(self, update, chat_info, user_info)
            # Forward messages to a feed
            feed_forward.pinned_message_handler(self, update, chat_info)

            cmd = None
            if "text" in msg and msg["text"].startswith("/"):
                cmd = msg["text"].split(" ", 2)[0].split(f"@{self._username}", 2)[0]

            if cmd:
                if cmd == "/ping":
                    # Original command
                    self.handle_ping(msg)
                elif cmd == "/pong":
                    self.handle_ping(msg, countdown=3)
                elif cmd == "/baby":
                    # Original command
                    chicks.handle(self, msg, chat_info, user_info)
                elif static_commands.handle(self, update, chat_info, cmd):
                    # DormBot command. `handle` will return true if static command was found
                    pass
                elif chat_id in self._dorm_chat_ids:
                    #
                    # Original commands
                    #
                    if cmd == "/pin":
                        combat_protector.pin(self, msg)
                    elif cmd == "/unpin":
                        combat_protector.unpin(self, msg)
                    elif cmd == "/hw":
                        hw.handle(self, msg)
                    #
                    # DormBot XP commands
                    #
                    elif experience.handle(self, msg, chat_info, user_info, cmd):
                        # `handle` will return true if the command was handled
                        pass
                    elif feed_forward.command_handler(self, update, chat_info, cmd):
                        pass
            elif chat_id not in self._dorm_chat_ids:
                self.handle_personal_message(msg)


def main():
    logging.basicConfig(level=logging.DEBUG)

    if "SENTRY_DSN" in os.environ:
        import sentry_sdk

        sentry_sdk.init(
            dsn=os.environ["SENTRY_DSN"],
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )

    combot = ComBot(
        api_key=TELEGRAM_TOKEN,
        superuser_id=CHAT_ID_SUPERUSER,
        dorm_chat_ids=[CHAT_ID_DORM_CHAT, CHAT_ID_TEST_CHAT],
    )

    while True:
        try:
            combot.get_and_process_updates()
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    main()
