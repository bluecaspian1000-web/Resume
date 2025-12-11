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
            'major', 
            'entry_year', 
            'national_id',
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

    
   
