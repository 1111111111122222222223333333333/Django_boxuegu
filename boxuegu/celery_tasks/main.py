from celery import Celery
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "boxuegu.settings.dev"

app = Celery('boxuegu')

app.config_from_object('celery_tasks.config')

# 自动识别任务
app.autodiscover_tasks([
    'celery_tasks.mail',

])
