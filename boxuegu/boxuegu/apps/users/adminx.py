from .models import UserProfile,EmailVerifyRecord,Banner
import xadmin

class UserProfileAdmin(object):
    list_display = ['nick_name','birthday','gender','address','mobile','image']
    search_fields = ['nick_name',]
    list_editable = ['nick_name','birthday','gender','address','mobile','image']
    list_filter = ['nick_name','birthday','gender','address','mobile','image']
class EmailVerifyRecordAdmin(object):
    pass
class BannerAdmin(object):
    pass
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
