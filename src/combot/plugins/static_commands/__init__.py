import os
from typing import NamedTuple, Optional

from ...bot import Bot
from ...bot.models import ChatInfo


extension_to_parse_mode = {
    ".txt": (None, False),
    ".md": ("Markdown", False),
    ".v2_md": ("MarkdownV2", False),
    ".html": ("HTML", False),
    ".htm": ("HTML", False),
    ".nopreview_txt": (None, True),
    ".nopreview_md": ("Markdown", True),
    ".nopreview_v2_md": ("MarkdownV2", True),
    ".nopreview_html": ("HTML", True),
    ".nopreview_htm": ("HTML", True),
}


class CommandContent(NamedTuple):
    text: str
    parse_mode: str
    no_preview: bool


class StaticCommands:
    def __init__(self, search_root: str = os.path.dirname(__file__)) -> None:
        self._search_root = search_root
        self._discovered_commands: dict[str, CommandContent] = {}

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
                pm = extension_to_parse_mode[ext]
                return CommandContent(text=f.read(), parse_mode=pm[0], no_preview=pm[1])
        return None

    def handle(
        self, bot: Bot, update: dict, chat_info: ChatInfo, command: str
    ) -> Optional[bool]:
        if command.startswith("/"):
            command = command[1:]
        else:
            return False

        if command not in self._discovered_commands:
            self._discovered_commands[command] = self._lookup_command(command)

        dc = self._discovered_commands.get(command)
        if dc is None:
            return False

        msg_id = update["message"]["message_id"]
        bot.send_message(
            chat_id=update["message"]["chat"]["id"],
            text=dc.text,
            reply_to=msg_id,
            parse_mode=dc.parse_mode,
            no_preview=dc.no_preview,
        )
        return True
