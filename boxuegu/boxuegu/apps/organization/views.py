from django.shortcuts import render
from django.views import View
# Create your views here.

class OrgListView(View):
    def get(self,request):
        return render(request, 'org-list.html')
class Org_teacherView(View):
    def get(self,request,org_id):
        return render(request, 'org-detail-teachers.html')

class Org_descView(View):
    def get(self,request,org_id):
        return render(request, 'org-detail-desc.html')

class Org_courseView(View):
    def get(self,request,org_id):
        return render(request,'org-detail-course.html')

class OrgHomeView(View):
    def get(self,request,org_id):
        return render(request,'org-detail-homepage.html')

class TeacherListView(View):
    def get(self,requset):
        pass

class TeacherDetailView(View):
    def get(self,request,user_id):
        return render(request, 'org-detail-teachers.html')

class AddfavView(View):
    def get(self,requset):
        pass
