from django.shortcuts import render
from django.views import View
from .models import Teacher


class OrgList(View):
    def get(self,request):

        return render(request,'org-list.html')


class TeacherList(View):
    def get(self,request):

        teachers=Teacher.objects.all()
        pass

class AddfavView(View):
    def get(self,request):
        pass