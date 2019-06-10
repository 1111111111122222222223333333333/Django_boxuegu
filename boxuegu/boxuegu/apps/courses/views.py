from django.shortcuts import render
from django.views import View
# Create your views here.
from courses.models import Course


class CourseListView(View):
    def get(self,request):
        return render(request, 'course-detail.html')

class Course_infoView(View):
    def get(self,request,couser_id):
        return render(request,'course-detail.html')

class CourseDetailView(View):
    def get(self,requset, couser_id):
        return render(requset,'course-detail.html')


