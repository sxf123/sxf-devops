from __future__ import absolute_import
import os
from celery import Celery,platforms

os.environ.setdefault("DJANGO_SETTINGS_MODULE","devops.settings")
from django.conf import settings

app = Celery("devops")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    print("Result: {0!r}".format(self.request))
