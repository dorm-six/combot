import os


def require_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise KeyError("Missing required environment variable {}".format(var_name))


TELEGRAM_TOKEN = require_env_var("TELEGRAM_TOKEN")  # id:str
DATABASE_URL = require_env_var("DATABASE_URL")

CHAT_ID_SUPERUSER = int(require_env_var("CHAT_ID_SUPERUSER"))
CHAT_ID_DORM_CHAT = int(require_env_var("CHAT_ID_DORM_CHAT"))
CHAT_ID_TEST_CHAT = int(require_env_var("CHAT_ID_TEST_CHAT"))

DORM_CHAT_IDS = list(
    {
        CHAT_ID_TEST_CHAT,
        CHAT_ID_DORM_CHAT,
    }
)
