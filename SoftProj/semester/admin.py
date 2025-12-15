from django.contrib import admin
from .models import Semester


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('code', 'year', 'term', 'is_active')
    list_filter = ('year', 'term', 'is_active')
    search_fields = ('code',)
    ordering = ('-year', 'term')
    readonly_fields = ('code',)  

