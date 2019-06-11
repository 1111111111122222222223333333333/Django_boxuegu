from django.shortcuts import render
from django.views import View
from courses.models import Course
from operation.models import UserCourse


class CoursesList(View):
    def get(self, request):
        courses = Course.objects.all()

        return render(request, 'course-list.html', {'all_courses': courses})


class CoursesDetail(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'course-detail.html', {'course': courses})

class CoursesInfo(View):
    def get(self, request):

        return render(request, 'course-comment.html')

