import os


def require_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise KeyError("Missing required environment variable {}".format(var_name))


TELEGRAM_TOKEN = require_env_var("TELEGRAM_TOKEN")
DATABASE_URL = require_env_var("DATABASE_URL")

CHAT_ID_SUPERUSER = int(os.environ.get("CHAT_ID_SUPERUSER", "0"))
CHAT_ID_DORM_CHAT = int(os.environ.get("CHAT_ID_DORM_CHAT", "0"))
CHAT_ID_TEST_CHAT = int(os.environ.get("CHAT_ID_TEST_CHAT", "0"))
