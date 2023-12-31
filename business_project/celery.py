# celery' nin django ile birlikte kullanılabilmesi için gerekli ayarlar
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery as CeleryPackage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "business_project.settings")
app = CeleryPackage("business_project")

app.config_from_object("django.conf:settings", namespace='CELERY')

app.autodiscover_tasks()
