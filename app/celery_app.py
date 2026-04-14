from celery import Celery

celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"],
)

celery.conf.update(
    task_track_started=True,
    result_expires=3600,
)