import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agro_django.settings")

app = Celery("agro_django")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.enable_utc = False
app.conf.timezone = settings.TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    "expire-invoices-every-minute": {
        "task": "payments.tasks.expire_invoices",
        "schedule": 60.0,
    },
}
