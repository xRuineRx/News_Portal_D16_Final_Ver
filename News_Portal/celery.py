import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

#Для Еженедельной рассылки
from celery.schedules import crontab

# app.conf.beat_schedule = {
#     'send_notify_every_monday_8am': {
#         'task': 'simpleapp.tasks.my_job',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#     },
# }

app.conf.beat_schedule = {
    'send_notify_every_monday_8am': {
        'task': 'simpleapp.tasks.my_job',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}