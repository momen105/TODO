from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .form import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import json

class HomeView(View):

    def get(self,request):
        form = TODoForm(request.POST or None)
        edit_id = request.GET.get("edit_id")
        edit_task = None
        if edit_id:
            edit_task = TODO.objects.filter(id=edit_id).last()
            
        data = {
            "todo":TODO.objects.order_by('-id'),
            "all_todo":TODO.objects.count(),
            "form":form,
            "edit_task": edit_task 
        }
        return render(request,'home.html',context=data)
    
    def post(self,request):
        id = request.POST.get("edit_id")
        if id:
            todo = TODO.objects.get(id=id)
            form = TODoForm(request.POST or None, instance=todo)
            if form.is_valid():
                form.save()
            return redirect("home")


        form = TODoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('home')
        

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        task_id = data.get("task_id")

        if not task_id:
            return redirect('home')

        data = get_object_or_404(TODO, id=task_id)
        data.delete()
        return redirect('home')
        

class HomeAPIView(APIView):
    def get(self,request):
        todo = TODO.objects.order_by('-id')
        ser = ToDoserializer(todo,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)

    def post(self,request):
  
        ser = ToDoserializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

    
