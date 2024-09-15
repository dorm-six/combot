import random
from datetime import datetime, timedelta

from ...bot import Bot
from ...bot.models import ChatInfo, UserInfo
from ...db.session import dbsession
from .data import generate_luck_message, generate_levelup_message
from .models import ChatJackpotProbability, ChatExperience


def notify_luck(bot: Bot, chat_id: int, name: str, points: int):
    bot.send_message(chat_id=chat_id, text=generate_luck_message(name, points))


def notify_levelup(bot: Bot, chat_id: int, name: str, level: str, points: int):
    bot.send_message(
        chat_id=chat_id, text=generate_levelup_message(name, level, points)
    )


@dbsession
def add_experience(
    bot: Bot,
    chat_id: int,
    user_id: int,
    amount: int,
    full_name=None,
    timed=False,
    silent=False,
    session=None,
):
    user_exp = (
        session.query(ChatExperience)
        .filter(ChatExperience.chat_id == chat_id, ChatExperience.user_id == user_id)
        .one_or_none()
    )
    if user_exp is None:
        user_exp = ChatExperience(chat_id=chat_id, user_id=user_id)
    if full_name:
        user_exp.last_user_name = full_name

    # Ignore experience buff if timed
    five_minutes_ago = datetime.now() - timedelta(minutes=5)
    if (
        timed
        and user_exp.last_exp_update is not None
        and user_exp.last_exp_update > five_minutes_ago
    ):
        return

    old_experience = 0 if user_exp.experience is None else user_exp.experience
    new_experience = old_experience + amount

    if new_experience < 0:
        new_experience = 0

    user_exp.experience = new_experience

    if timed:
        user_exp.last_exp_update = datetime.now()

    session.add(user_exp)
    session.commit()
    session.flush()

    old_level, _, _ = data.calculate_level(old_experience)
    new_level, level_name, _ = data.calculate_level(new_experience)

    if not silent and old_level != new_level:
        notify_levelup(
            bot=bot,
            chat_id=chat_id,
            name=full_name,
            level=level_name,
            points=new_experience,
        )


@dbsession
def experience_handler(
    bot: Bot,
    update: dict,
    chat_info: ChatInfo,
    user_info: UserInfo,
    session=None,
):
    if "message" not in update:
        return

    prob = (
        session.query(ChatJackpotProbability)
        .filter(ChatJackpotProbability.chat_id == chat_info.id)
        .one_or_none()
    )
    if prob is None:
        prob = ChatJackpotProbability(chat_id=chat_info.id, jackpot_prob=0)

    prob.jackpot_prob += 1 / 300.0
    session.add(prob)

    points = random.randint(1, 12)
    timed = True
    if 0.5 <= prob.jackpot_prob < random.uniform(0, 1):
        points *= random.randint(2, 4)
        timed = False
        prob.jackpot_prob = 0
        notify_luck(
            bot=bot, chat_id=chat_info.id, name=user_info.full_name, points=points
        )
    session.add(prob)
    session.commit()

    add_experience(
        bot=bot,
        chat_id=chat_info.id,
        user_id=user_info.id,
        amount=points,
        full_name=user_info.full_name,
        silent=False,
        timed=timed,
    )


def handle(
    bot: Bot,
    msg: dict,
    chat_info: ChatInfo,
    user_info: UserInfo,
    command: str,
) -> bool:
    # Circular dependencies resolution
    from .cmd_addexp import cmd_addexp
    from .cmd_mylvl import cmd_mylvl
    from .cmd_toplvl import cmd_toplvl

    if command == "/addexp":
        cmd_addexp(bot=bot, msg=msg)
    elif command == "/mylvl":
        cmd_mylvl(bot=bot, msg=msg)
    elif command == "/toplvl":
        cmd_toplvl(bot=bot, msg=msg)
    else:
        return False
    return True
