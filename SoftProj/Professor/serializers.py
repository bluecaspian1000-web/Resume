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

        if User.objects.filter(username=user_data["username"]).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        if  Professor.objects.filter(professor_code=validated_data.get("professor_code")).exists():
            raise serializers.ValidationError({"professor_code": "This professor code is already taken."})

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
    
    """
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