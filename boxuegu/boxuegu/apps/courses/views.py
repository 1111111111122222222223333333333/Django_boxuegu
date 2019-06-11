from django.shortcuts import render
from django.views import View
from .models import Course


class CouresListView(View):
    def get(self,request):
        course=Course.objects.all()

        context={
            'courses':course
        }
        return render(request,'course-list.html',context)


