from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from courses.serializers import CourseOfferingReadSerializer


"""
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['year', 'term', 'code', 'is_active']
        read_only_fields = ['code'] 
"""
    
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

class StudentCourseSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    course_name = serializers.ReadOnlyField(source='course.name')
    course_offering = CourseOfferingReadSerializer(read_only=True)
    unit = serializers.ReadOnlyField()
    status_fa = serializers.SerializerMethodField()

    class Meta:
        model = StudentCourse
        fields = [
            'id',
            'student_semester',
            'course_offering',
            'student',
            'course_name',
            'unit',
            'grade',
            'status',
            'status_fa',
            'enrollment_date',
            'grade_date',
            'last_modified',
            'is_active',
        ]
        read_only_fields = [
            'status',
            'grade_date',
            'last_modified',
        ]

    def get_status_fa(self, obj):
        return obj.get_status_display_fa()
    

class StudentSemesterSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    total_units = serializers.ReadOnlyField()
    passed_units = serializers.ReadOnlyField()
    gpa = serializers.ReadOnlyField()

    courses = StudentCourseSerializer(
        source='studentcourse_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = StudentSemester
        fields = [
            'id',
            'student',
            'semester',
            'min_units',
            'max_units',
            'is_active',
            'registration_date',
            'total_units',
            'passed_units',
            'gpa',
            'courses',
        ]
        read_only_fields = [
            'registration_date',
            'total_units',
            'passed_units',
            'gpa',
        ]

class EnrollCourseSerializer(serializers.Serializer):
    course_offering_id = serializers.IntegerField(write_only=True)

    def validate(self, data):
        student = self.context['request'].user
        student_id = student.id

        course_offering_id = data['course_offering_id']

      
        #student = self.context['request'].user  
        #if not student.is_authenticated:
        #    raise serializers.ValidationError("ابتدا وارد سایت شوید")
        student_active_semester = StudentSemester.objects.filter(student=student, is_active=True)
        if not student_active_semester.exists():
            raise serializers.ValidationError("هیچ ترم فعالی برای دانشجو موجود نیست.")

        current_semester = student_active_semester.latest('semester__year', 'semester__term')

        #course_active_semester = CourseOffering.objects.get(id=course_offering_id).semester
       
        
        # گرفتن درس ارائه‌شده
        try:
            course_offering = CourseOffering.objects.get(id=course_offering_id)
        except CourseOffering.DoesNotExist:
            raise serializers.ValidationError("درس مورد نظر پیدا نشد.")

        # چک ترم درس با ترم فعال
        if course_offering.semester != current_semester.semester:
            raise serializers.ValidationError(
                f"این درس در ترم فعال شما ارائه نشده است. ترم درس: {course_offering.semester}"
            )

        # چک سقف واحد
        if not current_semester.can_add_course(course_offering):
            raise serializers.ValidationError("سقف واحد مجاز این ترم پر شده است.")

        # چک پیش‌نیازها
        prerequisites = course_offering.course.prerequisites.all()
        failed_prereqs = []
        for prereq in prerequisites:
            passed_courses = StudentCourse.objects.filter(
                student_semester__student_id=student_id,
                course_offering__course=prereq,
                status='passed'
            )
            if not passed_courses.exists():
                failed_prereqs.append(prereq.name)
        
        if failed_prereqs:
            raise serializers.ValidationError(
                f"دانشجو پیش‌نیازهای زیر را پاس نکرده است: {', '.join(failed_prereqs)}"
            )

        # افزودن موارد به validated_data
        data['student_semester'] = current_semester
        data['course_offering'] = course_offering
        return data

    def create(self, validated_data):
        return StudentCourse.objects.create(
            student_semester=validated_data['student_semester'],
            course_offering=validated_data['course_offering'] )


"""
class EnrollCourseSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(write_only=True)
    course_offering_id = serializers.IntegerField(write_only=True)

    def validate(self, data):
        student_id = data['student_id']
        course_offering_id = data['course_offering_id']

        # گرفتن ترم فعال
        active_semesters = StudentSemester.objects.filter(student_id=student_id, is_active=True)
        if not active_semesters.exists():
            raise serializers.ValidationError("هیچ ترم فعالی برای دانشجو موجود نیست.")

        current_semester = active_semesters.latest('semester__year', 'semester__term')

        # گرفتن درس ارائه‌شده
        try:
            course_offering = CourseOffering.objects.get(id=course_offering_id)
        except CourseOffering.DoesNotExist:
            raise serializers.ValidationError("درس مورد نظر پیدا نشد.")

        # چک سقف واحد
        if not current_semester.can_add_course(course_offering):
            raise serializers.ValidationError("سقف واحد مجاز این ترم پر شده است.")

        # چک پیش‌نیازها
        prerequisites = course_offering.course.prerequisites.all()
        failed_prereqs = []
        for prereq in prerequisites:
            passed_courses = StudentCourse.objects.filter(
                student_semester__student_id=student_id,
                course_offering__course=prereq,
                status='passed'
            )
            if not passed_courses.exists():
                failed_prereqs.append(prereq.name)
        
        if failed_prereqs:
            raise serializers.ValidationError(
                f"دانشجو پیش‌نیازهای زیر را پاس نکرده است: {', '.join(failed_prereqs)}"
            )

        data['student_semester'] = current_semester
        data['course_offering'] = course_offering
        return data

    def create(self, validated_data):
        return StudentCourse.objects.create(
            student_semester=validated_data['student_semester'],
            course_offering=validated_data['course_offering']
        )


    

class StudentSemesterSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(read_only=False)
    class Meta:
        model = StudentSemester
        fields = [
            'student',
            'semester',
            'total_units',
            'min_units',
            'max_units',
        ]

class StudentSemesterSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(write_only=True)
    semester_code = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentSemester
        fields = ['student_username', 'semester_code', 'total_units', 'min_units', 'max_units']

    def create(self, validated_data):
        student_username = validated_data.pop('student_username')
        semester_code = validated_data.pop('semester_code')

        student = User.objects.get(username=student_username)
        semester = Semester.objects.get(code=semester_code)

        ss = StudentSemester.objects.create(
            student=student,
            semester=semester,
            **validated_data
        )
        return ss

    def update(self, instance, validated_data):
        student_username = validated_data.pop('student_username', None)
        semester_code = validated_data.pop('semester_code', None)

        if student_username:
            instance.student = User.objects.get(username=student_username)
        if semester_code:
            instance.semester = Semester.objects.get(code=semester_code)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            "student": instance.student.username,
            "semester": instance.semester.code,
            "total_units": instance.total_units,
            "min_units": instance.min_units,
            "max_units": instance.max_units,
        }  


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['student_semester', 'course_offering', 'grade', 'status']
"""