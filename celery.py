from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

app = Celery('ip_tracking')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configuration de la tâche périodique
app.conf.beat_schedule = {
    'detect-suspicious-ips': {
        'task': 'ip_tracking.tasks.detect_suspicious_ips',
        'schedule': 3600.0,  # Exécution toutes les heures
    },
}