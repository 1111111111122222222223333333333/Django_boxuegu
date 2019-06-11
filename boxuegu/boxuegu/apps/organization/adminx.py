from .models import Teacher,CourseOrg,CityDict
import xadmin

class TeacherAdmin(object):
    pass
class CourseOrgAdmin(object):
    pass
class CityDictAdmin(object):
    pass
xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(CityDict,CityDictAdmin)
