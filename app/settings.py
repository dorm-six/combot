from __future__ import unicode_literals, absolute_import, print_function

import subprocess
import os

# ---------------
# --- GLOBALS ---
# ---------------


def requireEnvVar(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise KeyError("Missing required environment variable {}".format(var_name))


# -------------------
# --- SECRET DATA ---
# -------------------

# Example of your code beginning
#           Config vars
TOKEN = requireEnvVar("TELEGRAM_TOKEN")  # id:str
BASE_URL = "https://api.telegram.org/bot" + TOKEN + "/"
DATABASE_URL = requireEnvVar("DATABASE_URL")

CHAT_ID_SUPERUSER = int(requireEnvVar("CHAT_ID_SUPERUSER"))
CHAT_ID_DORM_CHAT = int(requireEnvVar("CHAT_ID_DORM_CHAT"))
CHAT_ID_TEST_CHAT = int(requireEnvVar("CHAT_ID_TEST_CHAT"))

DORM_CHAT_IDS = list(
    {
        CHAT_ID_TEST_CHAT,
        CHAT_ID_DORM_CHAT,
    }
)
