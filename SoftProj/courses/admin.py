from django.contrib import admin
from .models import Course, Session, CourseOffering, Semester


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'unit')
    search_fields = ('code', 'name')
    ordering = ('code',)
    filter_horizontal = ('prerequisites',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'time_slot', 'location')
    list_filter = ('day_of_week', 'time_slot')
    search_fields = ('location',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('code', 'year', 'term', 'is_active')
    list_filter = ('year', 'term', 'is_active')
    search_fields = ('code',)
    readonly_fields = ('code',)

@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ('course', 'prof', 'semester', 'group_code', 'capacity')
    list_filter = ('semester', 'course','prof')
    search_fields = ('course__name', 'course__code', 'prof__name')
    filter_horizontal = ('sessions',)
    readonly_fields = ('code',)
