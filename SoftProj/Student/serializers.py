from rest_framework import serializers
from .models import Student
from accounts.models import User


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email', required=False)
    password = serializers.CharField(write_only=True, source='user.password')

    class Meta:
        model = Student
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'student_code',
            #'major', 
            #'entry_year', 
            #'national_id',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
     
        if User.objects.filter(username=user_data["username"]).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})


        if Student.objects.filter(student_code=validated_data.get("student_code")).exists():
            raise serializers.ValidationError({"student_code": "This student code is already taken."})

        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data.get("email"),
            password=user_data["password"],
        )

        student = Student.objects.create(
            user=user,
            **validated_data
        )

        return student

    
    """
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        user = instance.user

        if user_data:
            validated_data.pop("first_name", None)
            validated_data.pop("last_name", None)

            new_username = user_data.get("username", user.username)
            #if new_username != user.username and User.objects.filter(username=new_username).exists():
            #    raise serializers.ValidationError({"username": "This username is already taken."})

            user.username = new_username
            user.email = user_data.get("email", user.email)
            user.first_name = user_data.get("first_name", user.first_name)
            user.last_name = user_data.get("last_name", user.last_name)

            if "password" in user_data:
                user.set_password(user_data["password"])

            user.save()

        return super().update(instance, validated_data)

    
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
