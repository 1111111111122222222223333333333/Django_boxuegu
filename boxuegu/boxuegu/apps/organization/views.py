from django.shortcuts import render
from django.views import View


class OrgList(View):
    def get(self, request):
        return render(request, 'org-list.html')


# 获取教师列表
class TeacherList(View):
    def get(self, request):
        return render(request, 'teachers-list.html')


class TeacherDetail(View):
    def get(self, request):
        return render(request, 'teacher-detail.html')


class AddAsk(View):
    def get(self, request):
        return render(request, 'org-detail-desc.html')


class OrgHome(View):
    def get(self, request):
        return render(request, 'org-detail-homepage.html')


class OrgDesc(View):
    def get(self, request):
        return render(request, 'org-detail-desc.html')


class OrgCourse(View):
    def get(self, request):
        return render(request, 'org-detail-course.html')
