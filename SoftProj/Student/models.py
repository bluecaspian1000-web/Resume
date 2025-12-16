from django.db import models
from courses.models import CourseOffering
from semester.models import Semester
from django.contrib.auth.models import User

class Student(models.Model):
    
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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



class StudentSemester(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    total_units = models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    status = models.CharField(
        choices=[('normal','Normal'), ('probation','Probation')],
        default='normal',
        blank=True,
        null=True,
    )

    min_units = models.PositiveSmallIntegerField(default=12,blank=True,null=True)
    max_units = models.PositiveSmallIntegerField(default=24,blank=True,null=True)

    class Meta:
        unique_together = ('student', 'semester')

    def __str__(self):
        return f"{self.student} - {self.semester}"
    



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



