from django.db import models
from accounts.models import User
from courses.models import CourseOffering
from semester.models import StudentSemester

class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    first_name = models.CharField(max_length=100, verbose_name="first name")
    last_name = models.CharField(max_length=100, verbose_name="last name")
    student_code = models.CharField(max_length=20, unique=True, verbose_name="professor code")

    major = models.CharField(max_length=100,blank=True, null=True)
    entry_year = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male','Male'),('female','Female')], blank=True, null=True)
    national_id = models.CharField(max_length=10, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"

class StudentCourse(models.Model):
    student_semester = models.ForeignKey(StudentSemester, on_delete=models.CASCADE)
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)

    grade = models.FloatField(null=True, blank=True)
    status = models.CharField(
        choices=[
            ('enrolled','Enrolled'),
            ('passed','Passed'),
            ('failed','Failed'),
            ('dropped','Dropped')
        ],
        default='enrolled'
    )
