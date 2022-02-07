import os
from celery import Celery
from django.conf import settings
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
app = Celery()
app.conf.update(settings.CELERY)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
