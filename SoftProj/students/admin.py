from django.contrib import admin
from .models import *
from courses.models import CourseOffering
from django.contrib.auth.models import User



"""
@admin.register(StudentSemester)
class StudentSemesterAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'total_units', 'min_units', 'max_units')
    list_filter = ('semester',)
    search_fields = ('student__username', 'student__first_name', 'student__last_name')

  
@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student_semester', 'course_offering', 'grade', 'status')
    list_filter = ('status', 'course_offering__course')
    search_fields = (
        'student_semester__student__username',
        'student_semester__student__first_name',
        'student_semester__student__last_name',
        'course_offering__course__code',
        'course_offering__course__name'
    )
"""


# -----------------------------
# Admin برای StudentSemester
# -----------------------------
@admin.register(StudentSemester)
class StudentSemesterAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'total_units', 'passed_units', 'is_active', 'registration_date')
    list_filter = ('is_active', 'semester')
    search_fields = ('student__username', 'student__email')
    ordering = ('-semester__year', '-semester__term')
    readonly_fields = ('total_units', 'passed_units')  # فقط برای نمایش
    
    def total_units(self, obj):
        return obj.total_units
    total_units.short_description = 'واحد کل'

    def passed_units(self, obj):
        return obj.passed_units
    passed_units.short_description = 'واحدهای گذرانده شده'


# -----------------------------
# Admin برای StudentCourse
# -----------------------------
@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'unit', 'status_fa', 'grade', 'enrollment_date', 'is_active')
    list_filter = ('status', 'is_active')
    search_fields = ('student_semester__student__username', 'course_offering__course__name', 'course_offering__course__code')
    ordering = ('-enrollment_date',)

    def student(self, obj):
        return obj.student
    student.short_description = 'دانشجو'

    def course(self, obj):
        return obj.course
    course.short_description = 'درس'

    def unit(self, obj):
        return obj.unit
    unit.short_description = 'واحد'

    def status_fa(self, obj):
        return obj.get_status_display_fa()
    status_fa.short_description = 'وضعیت درس'
