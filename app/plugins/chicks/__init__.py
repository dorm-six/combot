from __future__ import unicode_literals, absolute_import, print_function

import random
from app.api import API


class Chicks:
    _chicks = {
        'Megan Fox' : 'https://pp.userapi.com/c840322/v840322120/45c9b/oiJ4RHqVYTI.jpg',
        'Jessica Alba' : 'https://pp.userapi.com/c621705/v621705776/8224c/kNfdB8EJeXM.jpg',
        'Jessica Alba 2' : 'https://pp.userapi.com/c840227/v840227855/8eea9/goF2Tcrk-To.jpg',
        'Sasha Grey' : 'https://pp.userapi.com/c621511/v621511163/6a44e/NXEPY7GXl5c.jpg',
        'Scarlett Johansson' : 'https://sun9-8.userapi.com/c840520/v840520285/6a6db/qxI7cbg5mjU.jpg',
        'Margot Robbie' : 'https://sun9-9.userapi.com/c840426/v840426620/6b540/zPEXaRUC2ZQ.jpg',
        'Jennifer Lawrence' : 'https://pp.userapi.com/c621511/v621511648/6cc89/yvQ1cIvO5FE.jpg',
        'Amber Heard' : 'https://pp.userapi.com/c840221/v840221545/8f505/ey9_lJAWLC0.jpg',
        'Miranda Kerr' : 'https://pp.userapi.com/c621706/v621706850/7dc15/WlA3cQlL0qY.jpg',
        'Rihanna' : 'https://sun9-7.userapi.com/c840526/v840526105/6ab69/34LcCIQdzqE.jpg',
        'Lizzy Caplan' : 'https://pp.userapi.com/c840325/v840325631/6e827/BchgGnPyfis.jpg',
        'Emma Watson' : 'https://sun9-5.userapi.com/c840433/v840433317/6cafd/aHgSpcrSTaU.jpg',
        'Rachel Nicols' : 'https://pp.userapi.com/c840331/v840331377/7073d/L6SdkSOr04M.jpg',
        'Fat Man' : 'https://pp.userapi.com/c840127/v840127496/8ffd9/X8IcN9CV-aA.jpg',

        'Emily Ratajkowski': 'https://pp.userapi.com/c849420/v849420949/6ba61/tM4djwe3uBE.jpg',
        'Rihanna 2' : 'https://pp.userapi.com/c849420/v849420426/6d6d7/Tdvtt-mIoDo.jpg',
        'Irina Shayk' : 'https://pp.userapi.com/c849420/v849420426/6d6f6/YmZQe1uMG7w.jpg',
        'Candice Swanepoel' : 'https://pp.userapi.com/c849420/v849420949/6ba1a/hR1m9p9Cfhg.jpg',
        'Mila Kunis' : 'https://pp.userapi.com/c850236/v850236810/24ed4/aqRvgk6Y5jM.jpg',
        'Nina Dobrev' : 'https://pp.userapi.com/c850236/v850236810/24eed/zNFQUK63Obo.jpg',

        'Kaley Cuoco' : 'https://pp.userapi.com/c849536/v849536635/6d2b1/AmMt9Wt6CJw.jpg',
        'Anna Kendrick' : 'https://pp.userapi.com/c845523/v845523102/e9901/DeSn09KLGh4.jpg',
        'Laura Vandervoort' : 'https://pp.userapi.com/c846322/v846322635/e634c/ybxh7VxCR2w.jpg',
        'Laura Vandervoort 2' : 'https://pp.userapi.com/c849124/v849124555/74ee6/bG138EgEt2s.jpg',
        'Laura Vandervoort 3' : 'https://pp.userapi.com/c847016/v847016635/e39f2/CmWvYPl9WR0.jpg',
        'Elisha Cuthbert' : 'https://pp.userapi.com/c845523/v845523102/e9915/LnL4P0D1zSE.jpg',
        
        'Anna Korsun': 'https://pp.userapi.com/c852320/v852320640/194c4/7L44OkTQB6g.jpg',
        'Alica Ѕchmidt': 'https://pp.userapi.com/c850636/v850636587/41fb4/rE5kD9SDj-w.jpg',
        'Alice Matos': 'https://pp.userapi.com/c849216/v849216967/b3f7f/0a-AWPK0qOo.jpg',
        'Ana Cheri': 'https://pp.userapi.com/c849216/v849216967/b3f87/x2T1RON5Ph0.jpg',

        'Marie Avgeropoulos': 'https://pp.userapi.com/c855120/v855120126/aac26/EJf3eFVZtIs.jpg',
        'Gal Gadot': 'https://pp.userapi.com/c855532/v855532529/afc9e/d0cp3OSJmLQ.jpg',
        'Hayden Panettiere': 'https://pp.userapi.com/c850420/v850420414/17ce96/z4gcEMDuP74.jpg',
    }

    @staticmethod
    def _get_random_chick():
        name, url = random.choice(list(Chicks._chicks.items()))

        # remove number from the end
        splitted = name.strip().rsplit(' ')
        if len(splitted) > 1 and splitted[-1].isdigit():
            name = ' '.join(splitted[:-1])

        return name, url

    @staticmethod
    def do(msg):
        chat_id = msg['chat']['id']
        name, url = Chicks._get_random_chick()
        API.sendPhoto(chat_id, url, caption=name)
