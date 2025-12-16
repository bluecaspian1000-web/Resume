from rest_framework import serializers
from .models import *
#from accounts.models import User
from semester.serializers import *
from rest_framework import serializers
from .models import Student

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Student
        fields = [
            'username',      
            'password',     
            'student_code',
            'major',
            'entry_year',
            'gender',
            'national_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        student = Student.objects.create(user=user, **validated_data)
        return student


    
class StudentSemesterUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSemester
        fields = ['min_units', 'max_units']

    def validate(self, data):
        
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
    class Meta:
        model = StudentSemester
        fields = [
            #'id',
            'student',
            'semester',
            'total_units',
            'status',
            'min_units',
            'max_units',
        ]
    def validate_term(self, value):
        if value not in (1, 2, 3):
            raise serializers.ValidationError("Invalid term")
        return value


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['id', 'student_semester', 'course_offering', 'grade', 'status']
