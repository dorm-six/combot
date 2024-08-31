import os
from typing import NamedTuple, Optional

from app.bot import Bot
from app.bot.models import ChatInfo


extension_to_parse_mode = {
    ".txt": None,
    ".md": "Markdown",
    ".v2.md": "MarkdownV2",
    ".html": "HTML",
    ".htm": "HTML",
}


class CommandContent(NamedTuple):
    text: str
    parse_mode: str


class StaticCommands:
    _search_root: str
    _discovered_commands: dict[str, CommandContent]

    def __init__(self, search_root: str = os.path.dirname(__file__)) -> None:
        self._search_root = search_root

    def clear(self):
        self._discovered_commands.clear()

    def _lookup_command(self, command: str) -> Optional[CommandContent]:
        for item in os.scandir(self._search_root):
            if item.is_dir() or not item.name.startswith(command):
                continue

            ext = None
            for e in extension_to_parse_mode.keys():
                if item.name.endswith(e):
                    ext = e
                    break

            if item.name != command + ext:
                continue

            with open(item.path, "r", encoding="utf-8") as f:
                return CommandContent(
                    text=f.read(), parse_mode=extension_to_parse_mode[ext]
                )
        return None

    def handle(
        self, bot: Bot, update: dict, chat_info: ChatInfo, command: str
    ) -> Optional[bool]:
        if command not in self._discovered_commands:
            self._discovered_commands[command] = self._lookup_command(command)

        dc = self._discovered_commands.get(command)
        if dc is None:
            return False

        msg_id = update["message"]["message_id"]
        bot.send_message(
            chat_id=chat_info.id,
            text=dc.text,
            reply_to=msg_id,
            parse_mode=dc.parse_mode,
        )
        return True
