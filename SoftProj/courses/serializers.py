from rest_framework import serializers
from .models import Course , CourseSchedule
import re


class CourseSerializer(serializers.ModelSerializer):
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['name', 'code']

    #def get_professor_name(self, obj):
    #    return str(obj.professor)
    
    def validate_code(self, value):
        # create
        if self.instance is None:
            if Course.objects.filter(code=value).exists():
                raise serializers.ValidationError("Course code already exists.")
        # update ?
        return value
    


class CourseScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = CourseSchedule
        fields = [
            'course',          
            'course_name',     
            'course_code',  
            'capacity',   
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


from rest_framework import serializers
from .models import Course


class PrerequisiteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def validate(self, data):
        course = self.context.get("course")
        mode = self.context.get("mode")  # add یا remove
        code = data["code"]

        try:
            prereq = Course.objects.get(code=code)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"code": "Course with this code not found."})

        if mode == "add":
            if course.id == prereq.id:
                raise serializers.ValidationError({"code": "A course cannot be prerequisite of itself."})

            if course.prerequisites.filter(id=prereq.id).exists():
                raise serializers.ValidationError({"code": "This prerequisite already exists."})

        elif mode == "remove":
            if not course.prerequisites.filter(id=prereq.id).exists():
                raise serializers.ValidationError({"code": "This prerequisite is not assigned to this course."})

        data["prereq"] = prereq
        return data
