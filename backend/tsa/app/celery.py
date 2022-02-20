import asyncio

from celery import Celery

from tsa.config import config

celery_app = Celery("tsa-tasks", broker=config.CELERY_BROKER, include=["tsa.app.celery_tasks"])


def async_task(**celery_kwargs):
    """Register an async function as a celery task."""

    def wrapper(task_coroutine):
        task_name = celery_app.gen_task_name(task_coroutine.__name__, task_coroutine.__module__)

        @celery_app.task(name=task_name, bind=True, **celery_kwargs)
        def inner(_, *args, **kwargs):
            asyncio.run(task_coroutine(*args, **kwargs))

        return inner

    return wrapper
