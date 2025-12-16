from rest_framework import serializers
from .models import Professor
    
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Professor

class ProfessorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Professor
        fields = [
            'username',      
            'password',      
            'first_name',
            'last_name',
            'professor_code',
        ]

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        professor = Professor.objects.create(user=user, **validated_data)
        return professor
