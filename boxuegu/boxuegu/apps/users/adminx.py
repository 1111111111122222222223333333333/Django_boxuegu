import xadmin
from .models import Banner, EmailVerifyRecord, UserProfile


class BannerAdmin(object):
    pass


class EmailVerifyRecordAdmin(object):
    pass


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
