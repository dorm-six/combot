import csv
import random
import os.path

_exp_scale: list[int] = []
_levels: list[str] = []
_levelup_messages: list[str] = []
_luck_messages: list[str] = []


def load_experience() -> tuple[list[int], list[str]]:
    global _exp_scale, _levels
    if not _exp_scale or not _levels:
        p = os.path.join(os.path.dirname(__file__), "experience.csv")
        with open(p, "r") as f:
            with csv.reader(f) as csvfile:
                for row in csvfile:
                    _exp_scale.append(row[0])
                    _levels.append(row[1])
    return _exp_scale, _levels


def load_messages(src: str, dest: list[str]) -> list[str]:
    p = os.path.join(os.path.dirname(__file__), src)
    with open(p, "r") as f:
        for line in f:
            if not line:
                continue
            dest.append(line.strip())
    return dest


def load_levelup_messages() -> list[str]:
    global _levelup_messages
    if not _levelup_messages:
        load_messages("levelup_messages.txt", _levelup_messages)
    return _levelup_messages


def load_luck_messages() -> list[str]:
    global _luck_messages
    if not _luck_messages:
        load_messages("luck_messages.txt", _luck_messages)
    return _luck_messages


def calculate_level(xp):
    exp_scale, levels = load_experience()
    current_level = 0
    current_level_name = levels[0]
    if xp is not None:
        for i, n in enumerate(levels):
            if xp > exp_scale[i]:
                current_level = i
                current_level_name = n
    till_next = -1
    if current_level + 1 != len(levels):
        till_next = exp_scale[current_level + 1]
    return current_level, current_level_name, till_next


def generate_levelup_message(who, level_name, xp):
    random_comments = load_levelup_messages()
    return random.choice(random_comments).format(who=who, level_name=level_name, xp=xp)


def generate_luck_message(who, xp):
    random_comments = load_luck_messages()
    return random.choice(random_comments).format(who=who, xp=xp)


def cleanup():
    global _exp_scale, _levels, _levelup_messages, _luck_messages
    _exp_scale = []
    _levels = []
    _levelup_messages = []
    _luck_messages = []
