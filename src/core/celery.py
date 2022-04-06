import os

from celery import Celery
from celery.schedules import crontab
from django.utils.timezone import localtime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


class MyCelery(Celery):
    def now(self):
        return localtime()


celery_app = MyCelery('core')
celery_app.config_from_object(
    obj='django.conf:settings', namespace='CELERY',
)
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'populate_flights_data': {
        'task': 'flights.tasks.populate_flights_data',
        'schedule': crontab(hour='0', minute='0')
    },
    'check_flights': {
        'task': 'flights.tasks.populate_flights_data',
        'schedule': crontab(hour='0', minute='0')
    }
}
