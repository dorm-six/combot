import os

from celery import Task


class BotCeleryTask(Task):
    _celery_bot = None

    def __init__(self, bot, *args, **kwargs):
        if not self._celery_bot and "IN_CELERY" in os.environ:
            kwargs.update({"proxy": os.environ.get("PROXY")})
            self._celery_bot = bot(os.environ["API_KEY"], *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super(BotCeleryTask, self).__call__(
            *args, **kwargs, bot=self._celery_bot
        )
