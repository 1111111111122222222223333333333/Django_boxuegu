from .models import Course,BannerCourse,Lesson,Video,CourseResource
import xadmin

class CourseAdmin(object):
    list_display = ['course_org','name','desc','teacher','detail','degree','learn_times','students','fav_nums','image','click_nums','is_banner','category','tag','youneed_konw','teacher_tell','add_time']
class BannerCourseAdmin(object):
    pass
class LessonAdmin(object):
    pass
class VideoAdmin(object):
    pass
class CourseResourceAdmin(object):
    pass
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)

