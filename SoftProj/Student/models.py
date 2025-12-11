from django.db import models
from accounts.models import User

class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    first_name = models.CharField(max_length=100, verbose_name="first name")
    last_name = models.CharField(max_length=100, verbose_name="last name")
    student_code = models.CharField(max_length=20, unique=True, verbose_name="professor code")
    """
    major = models.CharField(max_length=100) # رشته تحصیلی
    entry_year = models.PositiveIntegerField() # سال ورود

    national_id = models.CharField(max_length=10, blank=True, null=True)
    
    gender = models.CharField(max_length=10, choices=[   # جنس
        ('male', 'Male'),
        ('female', 'Female'),
    ], blank=True, null=True)
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"