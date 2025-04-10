from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('api/home/',HomeAPIView.as_view(),name='home-api')
]

