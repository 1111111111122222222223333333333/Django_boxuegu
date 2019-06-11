import xadmin
from .models import Course, UserAsk, UserCourse, UserFavorite, UserMessage


class CourseAdmin(object):
    pass


class UserAskAdmin(object):
    pass


class UserCourseAdmin(object):
    pass


class UserFavoriteAdmin(object):
    pass


class UserMessageAdmin(object):
    pass


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
