from rest_framework import serializers
from .models import Course , CourseOffering, Session
import re


class CourseSerializer(serializers.ModelSerializer):
    #professor_name = serializers.SerializerMethodField()

    prerequisites = serializers.SlugRelatedField(
        queryset=Course.objects.all(),  # لیست درس ها برای انتخاب
        slug_field="code",              # از کد درس استفاده می‌کنیم
        many=True
    )

    class Meta:
        model = Course
        fields = ['name', 'code', 'unit','prerequisites']

    
    def validate_code(self, value):
        # create
        if self.instance is None:
            if Course.objects.filter(code=value).exists():
                raise serializers.ValidationError("Course code already exists.")
        return value
    
   

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["day_of_week", "time_slot", "location"]


class CourseOfferingSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_unit = serializers.IntegerField(source='course.unit', read_only=True)
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = CourseOffering
        fields = [
            'code',
            'course_name',
            'course_code',
            'course_unit',
            'capacity',
            'professor_name',
            'sessions',
            'semester',
        ]

    def get_professor_name(self, obj):
        return f"{obj.professor.user.first_name} {obj.professor.user.last_name}"
    
class CreateCourseOfferingSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True)

    class Meta:
        model = CourseOffering
        fields = [
            'course',
            'professor',
            'capacity',
            'semester',
            'group_code',
            'sessions',
        ]

    def validate_semester(self, value):
        if not re.match(r'^\d{4}-[1-3]$', value):
            raise serializers.ValidationError(
                "Semester must be in format YYYY-N, e.g., 1403-1"
            )
        return value


    def create(self, validated_data):
        sessions_data = validated_data.pop('sessions')

        offering = CourseOffering.objects.create(**validated_data)

        for session_data in sessions_data:
            session, _ = Session.objects.get_or_create(**session_data)
            offering.sessions.add(session)

        return offering


"""
class CreateCourseOfferingSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = CourseOffering
        fields = [
            #'course',          
            'course_name',     
            'course_code', 
            'offering-code',
            'capacity',   
            'unit'
            'professor_name',  
            'sessions', # nested object
            'semester',
        ]

    def validate_semester(self, value):        
        pattern = r'^\d{4}[1-3]$'  # YYYYN : semester form
        if not re.match(pattern, value):
            raise serializers.ValidationError("Semester must be in format YYYY-N, e.g., 1403-1")
        return value
    
    def validate_offering_code(self,value):
         if CourseOffering.objects.filter(offering_code=value).exists():
            raise serializers.ValidationError({"offering-code": "This offering-code is already taken."})
         
    def validate_course_code(self,value):
        if not Course.objects.filter(course_code=value).exists():
            raise serializers.ValidationError({"course-code": "Course with this code not found."})
        
    
    def validate(self, attrs):
        unit = attrs.get("couunitrse")
        sessions = attrs.get("sessions", [])

        if unit in [1, 2] and len(sessions) != 1:
            raise serializers.ValidationError(
                {"sessions": "1 and 2 unit courses must have exactly 1 session."}
            )

        if unit == 3 and len(sessions) != 2:
            raise serializers.ValidationError(
                {"sessions": "3 unit courses must have exactly 2 sessions."}
            )
        
        if  len(sessions) not in [1,2] :
             raise serializers.ValidationError(
                {"sessions": "A course must have either 1 session or 2 sessions."}
            )
        return attrs
    
    def create(self, validated_data):
        sessions_data = validated_data.pop("sessions", [])

        offering = CourseOffering.objects.create(**validated_data)

        for session_data in sessions_data:
            session = Session.objects.create(**session_data)
            offering.sessions.add(session)

        return offering
    
    def validate_sessions(self, value):
        
        if len(value) not in [1, 2]:
            raise serializers.ValidationError("A course must have 1 or 2 sessions.")

        seen = set()
        for session in value:
            key = (
                session["day_of_week"],
                session["time_slot"],
                session["location"]
            )

            if key in seen:
                raise serializers.ValidationError("Duplicate sessions are not allowed.")

            seen.add(key)

        return value
"""


class PrerequisiteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def validate(self, data):
        mode = self.context.get("mode")  # add یا remove
        course_code = data["course-code"]
        prereq_code = data["prereq-code"]

        try:
            course = Course.objects.get(code=course_code)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"code": "Course with this code not found."})

        try:
            prereq = Course.objects.get(code=prereq_code)
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
        data["course"] = course
        return data
