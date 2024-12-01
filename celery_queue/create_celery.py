from celery import Celery
import datetime as dt
import logging

from celery.signals import after_setup_logger, beat_init

from app.core.config import settings

from celery_queue.tasks import check_notification_to_send

logger = logging.getLogger(__name__)

celery_app = Celery('tasks', broker=settings.redis_url)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
)

celery_app.autodiscover_tasks()

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('logs/celery_logs.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)



interval_check = dt.timedelta(minutes=30)

celery_app.conf.beat_schedule = {
    "periodic_check_notification": {
        'task': 'celery_queue.tasks.check_notification_to_send',
        'schedule': interval_check
    }
}

@beat_init.connect
def setup_periodic_task(sender, **kwargs):
    check_notification_to_send.apply_async()



if __name__ == '__main__':
    celery_app.start()