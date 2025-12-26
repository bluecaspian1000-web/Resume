from rest_framework import serializers
from .models import *
from students.models import Semester
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
import re


class CourseSerializer(serializers.ModelSerializer):

    prerequisites = serializers.SlugRelatedField(
        queryset=Course.objects.all(),  
        slug_field="code",              
        many=True,
        required=False,     
        allow_empty=True , 
    )

    class Meta:
        model = Course
        fields = ['name', 'code', 'unit','prerequisites']


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'code', 'unit']  # بدون prerequisites

class CourseReadSerializer(serializers.ModelSerializer):
    prerequisites = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id','name', 'code', 'unit','prerequisites']  # بدون prerequisites

    def get_prerequisites(self, obj):
        return [{'id': p.id, 'name': p.name, 'code': p.code} for p in obj.prerequisites.all()]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["day_of_week", "time_slot", "location"]

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['year', 'term', 'code', 'is_active']
        read_only_fields = ['code'] 

class CourseOfferingWriteSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(write_only=True)
    prof_id = serializers.IntegerField(write_only=True)
    sessions = SessionSerializer(many=True, required=False)

    class Meta:
        model = CourseOffering
        fields = [
            'course_code',
            'group_code',
            #'semester',
            'capacity',
            'prof_id',
            'sessions',
        ]

    def create(self, validated_data):
        course_code = validated_data.pop('course_code')
        prof_id = validated_data.pop('prof_id')
        sessions_data = validated_data.pop('sessions', [])

        try:
            course = Course.objects.get(code=course_code)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course_code": "Course not found"})
        
        try:
            prof = User.objects.get(id=prof_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"prof_id": "professor not found"})
        
        try:
            semester = Semester.objects.get(is_active=True)
        except Semester.DoesNotExist:
            raise serializers.ValidationError({"active-semester":"active-semester not found"})

        offering = CourseOffering.objects.create(course=course,prof=prof,semester=semester, **validated_data)

        for session_data in sessions_data:
              session, _ = Session.objects.get_or_create(**session_data)
              offering.sessions.add(session)
              
        return offering

    def update(self, instance, validated_data):
        if 'course_code' in validated_data:
            course_code = validated_data.pop('course_code')
            try:
                instance.course = Course.objects.get(code=course_code)
            except Course.DoesNotExist:
                raise serializers.ValidationError({"course_code": "Course not found"})
            
        if 'prof_id' in validated_data:
            prof_id = validated_data.pop('prof_id')
            try:
                instance.prof = User.objects.get(id=prof_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"prof_id": "Professor not found"})
            
        
        sessions_data = validated_data.pop('sessions', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if sessions_data is not None:
            instance.sessions.all().delete()
            for session_data in sessions_data:
                session = Session.objects.create(**session_data)
                instance.sessions.add(session)

        return instance
    


class CourseOfferingReadSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)
    course = CourseReadSerializer(read_only=True)
    #sessions = serializers.StringRelatedField(many=True)
    #Course = serializers.StringRelatedField()
    #prof = serializers.StringRelatedField()
    prof = UserSerializer(read_only=True)
    semester = serializers.StringRelatedField()



    class Meta:
        model = CourseOffering
        fields = [
            'id',
            'code',
            'course',
            'prof',
            'group_code',
            'semester',
            'capacity',
            #'prof_name',
            'sessions',
        ]



# courses/serializers.py
from rest_framework import serializers
from courses.models import Course

class PrerequisiteSerializer(serializers.Serializer):
    coursecode = serializers.CharField(required=True)
    prereqcode = serializers.CharField(required=True)

    def validate(self, data):
        mode = self.context.get("mode")  
        course_code = data["coursecode"]
        prereq_code = data["prereqcode"]

        try:
            course = Course.objects.get(code=course_code)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"coursecode": "Course with this code not found."})

        try:
            prereq = Course.objects.get(code=prereq_code)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"prereqcode": "Course with this code not found."})

        if mode == "add":
            if course.id == prereq.id:
                raise serializers.ValidationError({"prereqcode": "A course cannot be prerequisite of itself."})
            if course.prerequisites.filter(id=prereq.id).exists():
                raise serializers.ValidationError({"prereqcode": "This prerequisite already exists."})

        elif mode == "remove":
            if not course.prerequisites.filter(id=prereq.id).exists():
                raise serializers.ValidationError({"prereqcode": "This prerequisite is not assigned to this course."})

        data["course"] = course
        data["prereq"] = prereq
        return data
