from django.core.mail import send_mail
from django.conf import settings
from celery_tasks.main import app


@app.task(name='send_user_mail', bind=True, retry_backoff=3)
def send_user_mail(self, to_email, verify_url):
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用博学谷。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail('博学谷-邮箱验证', '', settings.EMAIL_FROM, [to_email], html_message=html_message)
    except Exception as e:
        self.retry(exc=e, max_retries=2)
