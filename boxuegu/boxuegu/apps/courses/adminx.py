import xadmin
from .models import BannerCourse, Course, CourseResource, Lesson, Video


class BannerCourseAdmin(object):
    pass


class OrderAdmin(object):
    pass


# class CourseAdmin(object):
#     pass


class CourseResourceAdmin(object):
    pass


class LessonAdmin(object):
    pass


class VideoAdmin(object):
    pass


xadmin.site.register(BannerCourse, BannerCourseAdmin)
# xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
