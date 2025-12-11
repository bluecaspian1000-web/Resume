from rest_framework import serializers
from .models import Course , CourseSchedule
import re


class CourseSerializer(serializers.ModelSerializer):
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'capacity', 'professor_name']

    def get_professor_name(self, obj):
        return str(obj.professor)
    


class CourseScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = CourseSchedule
        fields = [
            'id',
            'course',          
            'course_name',     
            'course_code',     
            'professor_name',  
            'day_of_week',
            'time_slot',
            'location',
            'semester',
        ]


    def get_professor_name(self, obj):
        return f"{obj.course.professor.user.first_name} {obj.course.professor.user.last_name}"
    

    def validate_semester(self, value):
        
        pattern = r'^\d{4}-[1-3]$'  # YYYY-N : semester form

        if not re.match(pattern, value):
            raise serializers.ValidationError("Semester must be in format YYYY-N, e.g., 1403-1")
        return value

