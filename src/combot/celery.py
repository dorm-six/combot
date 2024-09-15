import os
import traceback

from celery import Celery, Task

from .combot import ComBot
from .settings import TELEGRAM_TOKEN, CHAT_ID_SUPERUSER, CHAT_ID_DORM_CHAT, CHAT_ID_TEST_CHAT

celery = Celery(
    "dormcelery",
    backend=os.environ["CELERY_BACKEND"],
    broker=os.environ["CELERY_BACKEND"],
)

class BotTask(Task):
    def __init__(self, *args, **kwargs):
        if "IN_CELERY" in os.environ:
            self._bot = ComBot(
                api_key=TELEGRAM_TOKEN,
                superuser_id=CHAT_ID_SUPERUSER,
                dorm_chat_ids=[CHAT_ID_DORM_CHAT, CHAT_ID_TEST_CHAT],
            )
        super(BotTask, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super(BotTask, self).__call__(
            *args, **kwargs, bot=self._bot
        )

@celery.task(base=BotTask)
def delete_task(chat_id, msg_ids, bot=None):
    print("Deleting " + str(msg_ids))
    failed = []
    for msg_id in msg_ids:
        try:
            response = bot.delete_message(chat_id, msg_id)
            print(response)
        except Exception as e:
            traceback.print_exc()
            if msg_id:
                failed.append(msg_id)
            pass
    if failed:
        delete_task.apply_async((chat_id, failed), countdown=3)