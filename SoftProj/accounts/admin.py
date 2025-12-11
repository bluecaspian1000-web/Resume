from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # بقیه کاربرا (مثل is_professor)
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('is_professor',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('is_professor',)}),
    )

    list_display = ('username', 'email', 'is_staff', 'is_professor', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_professor', 'is_active')
