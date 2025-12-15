from rest_framework import serializers
from .models import *
from accounts.models import User
from semester.serializers import *


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

    
class StudentSemesterUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSemester
        fields = ['min_units', 'max_units']

    def validate(self, data):
        # اگه فقط یکیش ارسال شد از قبلی استفاده میکنه
        min_u = data.get('min_units', self.instance.min_units)
        max_u = data.get('max_units', self.instance.max_units)

        if min_u > max_u:
            raise serializers.ValidationError(
                "min_units cannot be greater than max_units"
            )

        return data

    

class StudentSemesterSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    semester = SemesterSerializer(read_only=True)
    def validate_term(self, value):
        if value not in (1, 2, 3):
            raise serializers.ValidationError("Invalid term")
        return value


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['id', 'student_semester', 'course_offering', 'grade', 'status']
