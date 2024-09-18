import csv
import os
import random
from datetime import datetime, timedelta, timezone
from ...bot import Bot
from ...bot.models import ChatInfo, UserInfo


class Chicks:
    _chicks_path: str
    _chicks: list[list[str]]

    def __init__(
        self, chicks_csv=os.path.join(os.path.dirname(__file__), "chicks.csv")
    ):
        self._chicks_path = chicks_csv
        self._load_chicks()

    def _load_chicks(self) -> None:
        self._chicks = []
        with open(self._chicks_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    self._chicks.append(row)

    def clear(self) -> None:
        self._load_chicks()

    def _get_random_chick(self) -> tuple[str, str, int, int]:
        line = random.choice(self._chicks)
        name = line[0]
        url = line[1]
        min_mute = 0
        max_mute = 0
        if len(line) > 2:
            min_mute = int(line[2])
            max_mute = min_mute
        if len(line) > 3:
            max_mute = int(line[3])

        return name, url, min_mute, max_mute

    def handle(
        self, bot: Bot, msg: dict, chat_info: ChatInfo, user_info: UserInfo
    ) -> bool:
        is_admin = chat_info.id < 0 and bot.get_chat_member(
            chat_id=chat_info.id, user_id=user_info.id
        )["result"]["status"] in [
            "creator",
            "administrator",
        ]
        msg_id = msg["message_id"]
        if is_admin:
            if random.randint(0, 100) < 30:
                bot.send_message(
                    chat_id=chat_info.id,
                    text="Типичный пример малолетнего дебила.",
                    reply_to=msg_id,
                    parse_mode=None
                )
            elif random.randint(0, 100) < 50:
                bot.send_photo(
                    chat_id=chat_info.id,
                    photo="https://www.reed.edu/biology/courses/BIO342/2012_syllabus/2012_WEBSITES/CSLP%20Nov%2020%20Monkey%20and%20Addiction/images/rhesus-monkey%20self.jpg",
                    caption="{} {}".format(
                        user_info.first_name, user_info.last_name
                    ).strip(),
                    reply_to=msg_id,
                    parse_mode=None
                )
            return True

        name, url, min_mute, max_mute = self._get_random_chick()

        restricted = False
        if min_mute > 0 and random.randint(0, 100) < 80:
            bot.restrict_chat_member(
                chat_id=chat_info.id,
                user_id=user_info.id,
                permissions={"can_send_messages": False},
                until_date=int(
                    (
                        datetime.now(timezone.utc)
                        + timedelta(
                            minutes=(
                                random.randint(min_mute, max_mute)
                                if min_mute < max_mute
                                else min_mute
                            )
                        )
                    ).timestamp()
                ),
            )
            restricted = True

        if restricted:
            name += "."
        bot.send_photo(chat_id=chat_info.id, photo=url, caption=name, reply_to=msg_id)
        return True
