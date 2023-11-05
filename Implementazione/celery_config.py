from datetime import timedelta


BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

timezone = 'Europe/Rome'
"""
beat_schedule = {
    'check_every_minute': {
        'task': 'tasks.run_scans',
        'schedule': timedelta(seconds=15),
    },
}
"""