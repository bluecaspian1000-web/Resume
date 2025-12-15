# filters.py
import django_filters
from .models import Student, StudentSemester, StudentCourse

class StudentFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    student_code = django_filters.CharFilter(lookup_expr='icontains')
    major = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.CharFilter(lookup_expr='icontains')
    entry_year = django_filters.NumberFilter()  # فیلتر دقیق روی سال ورود

    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'student_code', 'major', 'gender', 'entry_year']


class StudentSemesterFilter(django_filters.FilterSet):
    student_username = django_filters.CharFilter(field_name='student__user__username', lookup_expr='icontains')
    student_first_name = django_filters.CharFilter(field_name='student__first_name', lookup_expr='icontains')
    student_last_name = django_filters.CharFilter(field_name='student__last_name', lookup_expr='icontains')
    semester_name = django_filters.CharFilter(field_name='semester__name', lookup_expr='icontains')  # فرض بر اینکه Semester فیلد name دارد
    status = django_filters.CharFilter(lookup_expr='icontains')
    min_total_units = django_filters.NumberFilter(field_name='total_units', lookup_expr='gte')
    max_total_units = django_filters.NumberFilter(field_name='total_units', lookup_expr='lte')

    class Meta:
        model = StudentSemester
        fields = [
            'student_username', 
            'student_first_name', 
            'student_last_name', 
            'semester_name', 
            'status',
            'min_total_units',
            'max_total_units'
        ]


class StudentCourseFilter(django_filters.FilterSet):
    # student
    student_username = django_filters.CharFilter(
        field_name='student_semester__student__user__username', lookup_expr='icontains'
    )
    student_first_name = django_filters.CharFilter(
        field_name='student_semester__student__first_name', lookup_expr='icontains'
    )
    student_last_name = django_filters.CharFilter(
        field_name='student_semester__student__last_name', lookup_expr='icontains'
    )

    # course
    course_name = django_filters.CharFilter(
        field_name='course_offering__course_name', lookup_expr='icontains'
    )
    course_code = django_filters.CharFilter(
        field_name='course_offering__course_code', lookup_expr='icontains'
    )

    
    status = django_filters.CharFilter(lookup_expr='icontains')
    min_grade = django_filters.NumberFilter(field_name='grade', lookup_expr='gte')
    max_grade = django_filters.NumberFilter(field_name='grade', lookup_expr='lte')

    class Meta:
        model = StudentCourse
        fields = [
            'student_username', 'student_first_name', 'student_last_name',
            'course_name', 'course_code',
            'status', 'min_grade', 'max_grade'
        ]
