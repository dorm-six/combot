import csv
import os
import random
from datetime import datetime, timedelta, timezone
from ...bot import Bot
from ...bot.models import ChatInfo, UserInfo


class RandomPics:
    _csv_path: str
    _pics: list[list[str]]

    def __init__(
        self, csv_relative_path=None, csv_absolute_path=None,
    ):
        if csv_absolute_path:
            self._csv_path = csv_absolute_path
        elif csv_relative_path:
            self._csv_path = str(os.path.join(os.path.dirname(__file__), csv_relative_path))
        else:
            raise RuntimeError("RandomPics plugin requires a CSV path")

        self._load_pics()

    def _load_pics(self) -> None:
        self._pics = []
        with open(self._csv_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    self._pics.append(row)

    def clear(self) -> None:
        self._load_pics()

    def _get_random_pic(self) -> tuple[str, str, int, int]:
        line = random.choice(self._pics)
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

        name, url, min_mute, max_mute = self._get_random_pic()

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
