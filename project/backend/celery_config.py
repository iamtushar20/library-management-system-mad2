from celery import Celery
from celery.schedules import crontab


# Update Redis port to 6380
celery = Celery(__name__, broker='redis://localhost:6380/0', backend='redis://localhost:6380/0')

# Celery beat schedule
CELERY_BEAT_SCHEDULE = {
    'generate_monthly_report': {
        'task': 'tasks.generate_monthly_report',
        # 'schedule': 45.0,  # Executes every 10 seconds
        'schedule': crontab(day_of_month=10, hour=13, minute=4)
        # 'schedule': crontab(minute='*/2')
    },
    'send_daily_reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=13, minute=4),  # Executes every day at 6 PM
        # 'schedule': 37.0,  # Executes every 10 seconds
    },
}

celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE