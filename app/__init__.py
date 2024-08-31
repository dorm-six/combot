import logging


from app.bot import Bot
from app.bot.utils import user_and_chat_info
from app.command import Command
from app.db.session import dbsession
from app.plugins import combat_protector, hw
from app.plugins.chicks import Chicks
from app.plugins.static_commands import StaticCommands
from app.settings import (
    TELEGRAM_TOKEN,
    CHAT_ID_DORM_CHAT,
    CHAT_ID_TEST_CHAT,
    DORM_CHAT_IDS,
)
from app.settings import CHAT_ID_SUPERUSER

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
        self, chat_ids: list[int], message_ids: list[int], delay: int = 0
    ) -> dict:
        pass

    def handle_ping(self, msg):
        chat_id = msg["chat"]["id"]
        self.send_message(chat_id=chat_id, text="I am Alive, сучка")

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
        try:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            cmd_obj = Command(msg["text"])
        except KeyError:
            return

        with user_and_chat_info(update, session) as uci:
            chat_info, user_info, user = uci

            if cmd_obj.is_single_cmd():
                if cmd_obj.is_cmd_eq("/ping", self._username):
                    self.handle_ping(msg)
                elif cmd_obj.is_cmd_eq("/baby", self._username):
                    chicks.handle(self, msg, chat_info, user_info)
                elif static_commands.handle(self, update, chat_info, cmd_obj.cmd):
                    # `handle` will return true if static command was found
                    pass
                elif chat_id in DORM_CHAT_IDS:
                    if cmd_obj.is_cmd_eq("/pin", self._username):
                        combat_protector.pin(self, msg)
                    elif cmd_obj.is_cmd_eq("/unpin", self._username):
                        combat_protector.unpin(self, msg)
                    elif cmd_obj.is_cmd_eq("/hw", self._username):
                        hw.handle(self, msg)
            elif chat_id not in DORM_CHAT_IDS:
                self.handle_personal_message(msg)


def main():
    logging.basicConfig(level=logging.DEBUG)
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


if __name__ == "__main__":
    main()
