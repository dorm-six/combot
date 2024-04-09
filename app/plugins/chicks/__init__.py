from __future__ import unicode_literals, absolute_import, print_function

import random
from datetime import datetime, timedelta
from app.api import API


class Chicks:
    _chicks = {
        "Megan Fox": "https://pp.userapi.com/c840322/v840322120/45c9b/oiJ4RHqVYTI.jpg",
        "Jessica Alba": "https://pp.userapi.com/c621705/v621705776/8224c/kNfdB8EJeXM.jpg",
        "Jessica Alba 2": "https://pp.userapi.com/c840227/v840227855/8eea9/goF2Tcrk-To.jpg",
        "Sasha Grey": "https://pp.userapi.com/c621511/v621511163/6a44e/NXEPY7GXl5c.jpg",
        "Scarlett Johansson": "https://sun9-8.userapi.com/c840520/v840520285/6a6db/qxI7cbg5mjU.jpg",
        "Margot Robbie": "https://sun9-9.userapi.com/c840426/v840426620/6b540/zPEXaRUC2ZQ.jpg",
        "Jennifer Lawrence": "https://pp.userapi.com/c621511/v621511648/6cc89/yvQ1cIvO5FE.jpg",
        "Amber Heard": "https://pp.userapi.com/c840221/v840221545/8f505/ey9_lJAWLC0.jpg",
        "Miranda Kerr": "https://pp.userapi.com/c621706/v621706850/7dc15/WlA3cQlL0qY.jpg",
        "Rihanna": "https://sun9-7.userapi.com/c840526/v840526105/6ab69/34LcCIQdzqE.jpg",
        "Lizzy Caplan": "https://pp.userapi.com/c840325/v840325631/6e827/BchgGnPyfis.jpg",
        "Emma Watson": "https://sun9-5.userapi.com/c840433/v840433317/6cafd/aHgSpcrSTaU.jpg",
        "Rachel Nicols": "https://pp.userapi.com/c840331/v840331377/7073d/L6SdkSOr04M.jpg",
        "Fat Man": "https://pp.userapi.com/c840127/v840127496/8ffd9/X8IcN9CV-aA.jpg",
        "Emily Ratajkowski": "https://pp.userapi.com/c849420/v849420949/6ba61/tM4djwe3uBE.jpg",
        "Rihanna 2": "https://pp.userapi.com/c849420/v849420426/6d6d7/Tdvtt-mIoDo.jpg",
        "Irina Shayk": "https://pp.userapi.com/c849420/v849420426/6d6f6/YmZQe1uMG7w.jpg",
        "Candice Swanepoel": "https://pp.userapi.com/c849420/v849420949/6ba1a/hR1m9p9Cfhg.jpg",
        "Mila Kunis": "https://pp.userapi.com/c850236/v850236810/24ed4/aqRvgk6Y5jM.jpg",
        "Nina Dobrev": "https://pp.userapi.com/c850236/v850236810/24eed/zNFQUK63Obo.jpg",
        "Kaley Cuoco": "https://pp.userapi.com/c849536/v849536635/6d2b1/AmMt9Wt6CJw.jpg",
        "Anna Kendrick": "https://pp.userapi.com/c845523/v845523102/e9901/DeSn09KLGh4.jpg",
        "Laura Vandervoort": "https://pp.userapi.com/c846322/v846322635/e634c/ybxh7VxCR2w.jpg",
        "Laura Vandervoort 2": "https://pp.userapi.com/c849124/v849124555/74ee6/bG138EgEt2s.jpg",
        "Laura Vandervoort 3": "https://pp.userapi.com/c847016/v847016635/e39f2/CmWvYPl9WR0.jpg",
        "Elisha Cuthbert": "https://pp.userapi.com/c845523/v845523102/e9915/LnL4P0D1zSE.jpg",
        "Anna Korsun": "https://pp.userapi.com/c852320/v852320640/194c4/7L44OkTQB6g.jpg",
        # 'Alica Ѕchmidt': 'https://pp.userapi.com/c850636/v850636587/41fb4/rE5kD9SDj-w.jpg',
        "Alice Matos": "https://pp.userapi.com/c849216/v849216967/b3f7f/0a-AWPK0qOo.jpg",
        # 'Ana Cheri': 'https://pp.userapi.com/c849216/v849216967/b3f87/x2T1RON5Ph0.jpg',
        "Marie Avgeropoulos": "https://pp.userapi.com/c855120/v855120126/aac26/EJf3eFVZtIs.jpg",
        "Gal Gadot": "https://pp.userapi.com/c855532/v855532529/afc9e/d0cp3OSJmLQ.jpg",
        "Hayden Panettiere": "https://pp.userapi.com/c850420/v850420414/17ce96/z4gcEMDuP74.jpg",
        # 04.10.19
        "Vanessa Kirby": "https://sun9-21.userapi.com/c857520/v857520573/35c2d/BfkdvQJaT8g.jpg",
        "Lindsey Morgan": "https://sun9-29.userapi.com/c854320/v854320374/111c66/KCuNNFQeXaw.jpg",
        # 28.03.20
        "Kylie Jenner": "https://sun9-21.userapi.com/c858336/v858336839/1ad7b9/xL5sN2jamiI.jpg",
        "Kylie Jenner 2": "https://sun9-26.userapi.com/c813024/v813024751/5c468/MQdddOXhKs4.jpg",
        "Camila Cabello": "https://sun9-63.userapi.com/c857428/v857428001/1b3fae/Sh7o_gTcNxk.jpg",
        "Alexandra Daddario": "https://sun9-25.userapi.com/c857728/v857728673/1a9429/8GzwXQlecVs.jpg",
        "Alexandra Daddario 2": "https://sun9-4.userapi.com/c857132/v857132900/138305/bciL-jUP7Pk.jpg",
        "Kelly Rohrbach": "https://sun9-31.userapi.com/c858124/v858124650/1bf162/mA1AxZCd9j0.jpg",
        "Kelly Rohrbach 2": "https://sun9-22.userapi.com/c850608/v850608187/10d41b/VLCiO3pzOpE.jpg",
        "Priyanka Chopra": "https://sun9-45.userapi.com/c858528/v858528650/135587/3PDUgu7zNPU.jpg",
        "Priyanka Chopra 2": "https://sun9-35.userapi.com/c205628/v205628668/c0060/baU7nuvLXgI.jpg",
        "Lily Collins": "https://sun9-69.userapi.com/c205528/v205528107/c1646/laWcwdnErCw.jpg",
        "Lily Collins 2": "https://sun9-60.userapi.com/c858324/v858324662/1bae34/4LvZSJuPSnA.jpg",
        "Ana de Armas": "https://sun9-52.userapi.com/c205528/v205528359/c2ad2/Ufhq9SQnJwM.jpg",
        "Ana de Armas 2": "https://sun9-37.userapi.com/c205628/v205628103/c3cb3/LmDzPZbgc78.jpg",
        "Ana de Armas 3": "https://sun9-2.userapi.com/c205816/v205816274/b8ce4/bfauFa97EOU.jpg",
        "Zoe Kravitz": "https://st.kp.yandex.net/im/kadr/3/3/3/kinopoisk.ru-Zoe-Kravitz-3338878.jpg",
        "Zoe Kravitz 2": "https://st.kp.yandex.net/im/kadr/3/2/8/kinopoisk.ru-Zoe-Kravitz-3283733.jpg",
    }

    @staticmethod
    def _get_random_chick():
        name, url = random.choice(list(Chicks._chicks.items()))

        # remove number from the end
        splitted = name.strip().rsplit(" ")
        if len(splitted) > 1 and splitted[-1].isdigit():
            name = " ".join(splitted[:-1])

        return name, url

    @staticmethod
    def do(msg):
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]

        if API.getChatMember(chat_id, user_id)["status"] in [
            "creator",
            "administrator",
        ]:
            if random.randint(0, 100) < 30:
                API.sendMsg(chat_id, "Типичный пример малолетнего дебила.")
            elif random.randint(0, 100) < 50:
                API.sendPhoto(
                    chat_id,
                    "https://www.reed.edu/biology/courses/BIO342/2012_syllabus/2012_WEBSITES/CSLP%20Nov%2020%20Monkey%20and%20Addiction/images/rhesus-monkey%20self.jpg",
                    caption="{} {}".format(
                        msg["from"]["first_name"], msg["from"].get("last_name", "")
                    ).strip(),
                )
            return

        restricted = False
        if random.randint(0, 100) < 80:
            API.restrictUser(
                chat_id,
                user_id,
                {"can_send_messages": False},
                int(
                    (
                        datetime.utcnow()
                        + timedelta(minutes=random.randint(9000, 14400))
                    ).timestamp()
                ),
            )
            restricted = True

        name, url = Chicks._get_random_chick()
        if restricted:
            name += "."
        API.sendPhoto(chat_id, url, caption=name)
