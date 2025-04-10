from django.views import View
from django.shortcuts import render,redirect
from .models import *
from .form import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

class HomeView(View):

    def get(self,request):
        form = TODoForm(request.POST or None)
        data = {
            "todo":TODO.objects.order_by('-id'),
            "all_todo":TODO.objects.count(),
            "form":form
        }
        return render(request,'home.html',context=data)
    
    def post(self,request):

        form = TODoForm(request.POST or None)
        if form.is_valid():
            form.save()
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

    
