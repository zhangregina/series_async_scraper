from __future__ import absolute_import
import os
from celery import Celery

from main import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

app = Celery("main")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(settings.INSTALLED_APPS)
