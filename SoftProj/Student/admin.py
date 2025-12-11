from django.contrib import admin
from .models import Student


@admin.register(Student)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['student_code', 'first_name', 'last_name']
    search_fields = ['student_code', 'first_name', 'last_name']

    fields = ['first_name', 'last_name', 'student_code']