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
        phrases = ["Типичный представитель дарвиновской премии.",
                   "Типичный пример малолетнего дебила.",
                   "Гордость мамкиных чатов.",
                   "Пример того, как естественный отбор промахнулся.",
                   "Громко, но без толку — прямо как ты.",
                   "Мог бы молчать — казался бы умнее.",
                   "Пример того, что эволюция иногда делает шаг назад."]
        user = "{} {}".format(user_info.first_name, user_info.last_name).strip()
        stupid_pics = [
            ("https://avatars.mds.yandex.net/i?id=b626dc887eb60fe0132d655a446aa686_sr-16921443-images-thumbs&n=13",
             f"За тобой выехали, {user}"),
            ("https://i.pinimg.com/originals/eb/89/2d/eb892d69bfb40cd8e4b07e7f451f83e4.jpg",
             f"Пойман с поличным, {user}"),
            ("https://i.pinimg.com/1200x/31/33/01/313301fdf1589fedb6d562e18b3f8da2.jpg",
             f"Ну заплачь, {user}"),
            ("https://www.reed.edu/biology/courses/BIO342/2012_syllabus/2012_WEBSITES/CSLP%20Nov%2020%20Monkey%20and%20Addiction/images/rhesus-monkey%20self.jpg",
             f"{user}")
        ]

        name, url, min_mute, max_mute = self._get_random_pic()
        if is_admin:
            if random.randint(0, 100) < 15:
                bot.send_message(
                    chat_id=chat_info.id,
                    text=random.choice(phrases),
                    reply_to=msg_id,
                    parse_mode=None
                )
            elif random.randint(0, 100) < 30:
                pic = random.choice(stupid_pics)
                bot.send_photo(
                    chat_id=chat_info.id,
                    photo=pic[0],
                    caption=pic[1],
                    reply_to=msg_id
                )
            elif random.randint(0, 100) < 80:
                bot.send_photo(chat_id=chat_info.id, photo=url, caption=name + ".", reply_to=msg_id)
            return True

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

class ChickPics (RandomPics):
    def _get_random_pic(self) -> tuple[str, str, int, int]:
        if random.randint(1, 100000) == 1:
            return ("Lia Habibullina",
                    "https://sun9-80.userapi.com/s/v1/ig2/izCzXV-hQI17Cd_U1mLRC_vl20S8JE3cDimz10PS3Hy5d9qlAU73jNsUc520rIYE65k7MYNtGBZGohDVhI2zDPc-.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu&cs=1920x0",
                    20000, 25000)
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