from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#from students.models import *
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="course name")
    code = models.CharField(max_length=20, unique=True, verbose_name="course code")
    unit = models.PositiveIntegerField(
        default=3,
        verbose_name="unit",
        validators=[MinValueValidator(1),MaxValueValidator(3)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        null=True,
        related_name="required_for"
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        db_table = 'courses'
        ordering = ['code']
        verbose_name = "course"
        verbose_name_plural = "courses"



class Session(models.Model):
    
    class DayOfWeek(models.TextChoices):
        SATURDAY = 'Saturday', 'Saturday'
        SUNDAY = 'Sunday', 'Sunday'
        MONDAY = 'Monday', 'Monday'
        TUESDAY = 'Tuesday', 'Tuesday'
        WEDNESDAY = 'Wednesday', 'Wednesday'

    day_of_week = models.CharField(
        max_length=10,
        choices=DayOfWeek.choices,
        verbose_name="day of week",
        blank= True,
        null=True,
    )

    class TimeSlot(models.TextChoices):
        SLOT_8_10 = '8-10', '8:00 - 10:00'
        SLOT_10_12 = '10-12', '10:00 - 12:00'
        SLOT_14_16 = '14-16', '14:00 - 16:00'
        SLOT_16_18 = '16-18', '16:00 - 18:00'

    time_slot = models.CharField(
        max_length=10,
        choices=TimeSlot.choices,
        verbose_name="time slot"
    )

    location = models.CharField(max_length=50,blank=True,null=True, verbose_name="location")

    def __str__(self):
        return f"{self.day_of_week} ({self.time_slot})" 
    
class Semester(models.Model):
    year = models.PositiveIntegerField(verbose_name="year",default=2025,blank=True,null=True)
    term = models.PositiveSmallIntegerField(
        verbose_name="term",
        help_text="1=First, 2=Second, 3=Summer",
        default=1,
        blank=True,
        null=True,
    )
    code = models.PositiveIntegerField(
        unique=True,
        editable=False,
        verbose_name="semester code"
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('year', 'term')

    def save(self, *args, **kwargs):
        self.code = self.year * 10 + self.term
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.code)


class CourseOffering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules', verbose_name="course")
    capacity = models.PositiveIntegerField(verbose_name="capacity",default=30)
    #prof_name = models.CharField(max_length=50, verbose_name="prof_name",blank=True,null=True,default="نامشخص")  
    prof = models.ForeignKey(User,on_delete=models.CASCADE, related_name='professor', verbose_name="prof-name")  
    sessions = models.ManyToManyField(Session,blank=True,null=True, related_name="course_schedules")
    #semester = models.IntegerField(max_length=30,default=20251,blank=True,null=True, verbose_name="semester") 
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE, related_name='semester', verbose_name="semester-course")
    group_code = models.CharField(
        max_length=10,
        verbose_name="group code"
    )
    
    code = models.CharField(    # offerin-course-code
        max_length=50,
        unique=True,
        editable=False
    ) 

    def save(self, *args, **kwargs):
        self.code = f"{self.course.code}{self.group_code}{self.semester.code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.code}"

    class Meta:
        verbose_name = "course offering"
        verbose_name_plural = "course offering"


