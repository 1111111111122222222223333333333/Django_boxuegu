from django.core.mail import send_mail
from django.conf import settings
from celery_tasks.main import app


@app.task(bind=True, name='send_active_mail', retry_backoff=3)
def send_active_mail(self, to, verify_url):
    subject = '博学谷-忘记密码'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用博学谷。</p>' \
                   '<p>您的邮箱为：%s 。请点击此修改您的密码：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to, verify_url, verify_url)
    try:
        send_mail(subject, '', settings.EMAIL_FROM, [to], html_message=html_message)
    except Exception as e:
        self.retry(exc=e, max_retries=3)