import os
from celery import Celery
import django
django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_upload_service.settings")
app = Celery("file_upload_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

