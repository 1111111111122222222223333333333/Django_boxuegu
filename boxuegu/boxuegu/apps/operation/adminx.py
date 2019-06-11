from .models import UserCourse,UserMessage,UserFavorite,CourseComments,UserAsk
import xadmin

class UserCourseAdmin(object):
    pass
class UserMessageAdmin(object):
    pass
class UserFavoriteAdmin(object):
    pass
class CourseCommentsAdmin(object):
    pass
class UserAskAdmin(object):
    pass
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserAsk,UserAskAdmin)
