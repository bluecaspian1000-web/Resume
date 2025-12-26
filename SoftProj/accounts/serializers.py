from django.contrib.auth.models import User, Group
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']

    
