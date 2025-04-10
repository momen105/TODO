from rest_framework import serializers
from .models import *

class ToDoserializer(serializers.ModelSerializer):
    class Meta:
        model = TODO
        fields = "__all__"

