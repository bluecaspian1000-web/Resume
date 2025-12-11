from rest_framework import serializers
from .models import Professor
from accounts.models import User


class ProfessorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email', required=False)
    password = serializers.CharField(write_only=True, source='user.password')

    class Meta:
        model = Professor
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'professor_code',
        ]

    def create(self, validated_data):

        user_data = validated_data.pop("user")

        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data.get("email"),
            password=user_data["password"],
        )

        professor = Professor.objects.create(
            user=user,
            **validated_data
        )

        return professor

    def update(self, instance, validated_data):
        
        user_data = validated_data.pop("user", None)
        user = instance.user

        if user_data:
            user.username = user_data.get("username", user.username)
            user.email = user_data.get("email", user.email)

            if "password" in user_data:
                user.set_password(user_data["password"])

            user.save()

        return super().update(instance, validated_data)

"""
class ProfessorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    department = serializers.CharField()  

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'department')

    def create(self, validated_data):

        dept = validated_data.pop('department')
        user = User.objects.create_user(**validated_data, is_professor=True)
        Professor.objects.create(user=user, department=dept)
        return user
"""