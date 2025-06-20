from celery.schedules import crontab
from tasks import celery, clone_disk

celery.conf.beat_schedule = {
    'weekly-clone': {
        'task': 'tasks.clone_disk',
        'schedule': crontab(hour=3, minute=0, day_of_week='sun'),
        'args': ['source.example.com', '/mnt/weekly_backup/disk.img']
    }
}

