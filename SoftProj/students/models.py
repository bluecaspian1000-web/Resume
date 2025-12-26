from django.db import models
from courses.models import Semester, CourseOffering
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

"""
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
"""    

class StudentSemester(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    
    min_units = models.PositiveSmallIntegerField(default=12)  #,blank=True,null=True
    max_units = models.PositiveSmallIntegerField(default=24)
    
    is_active = models.BooleanField(default=True)  
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'semester')
        ordering = ['-semester__year', '-semester__term']
    
    def save(self, *args, **kwargs):
        #if self.semester_id:  
        self.is_active = self.semester.is_active
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.student} - {self.semester}"
    
    @property
    def total_units(self):
        courses = self.studentcourse_set.filter(
            status__in=['enrolled', 'passed']
        )
        return sum(c.course_offering.course.unit for c in courses)
    
    @property
    def passed_units(self):
        courses = self.studentcourse_set.filter(status='passed')
        return sum(c.course_offering.course.unit for c in courses)
    
    @property
    def gpa(self):
        """معدل ترم"""
        # محاسبه GPA
        pass
    

    def can_add_course(self, course_offering):
        new_total = self.total_units + course_offering.course.unit
        return new_total <= self.max_units
    
    


class StudentCourse(models.Model):
    student_semester = models.ForeignKey(StudentSemester, on_delete=models.CASCADE)
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    
    grade = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]  
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('enrolled', 'در حال گذراندن'),
            ('passed', 'قبول شده'),
            ('failed', 'مردود شده'),
            ('dropped', 'حذف شده'),
            ('incomplete', 'ناتمام'),
            ('withdrawn', 'انصراف داده شده'),
        ],
        default='enrolled'
    )
    
    enrollment_date = models.DateTimeField(auto_now_add=True)  
    grade_date = models.DateTimeField(null=True, blank=True)  
    last_modified = models.DateTimeField(auto_now=True)  
    is_active = models.BooleanField(default=True)  
    

    
    class Meta:
        unique_together = ('student_semester', 'course_offering')  
        ordering = ['enrollment_date'] 
        verbose_name = 'درس دانشجو'
        verbose_name_plural = 'StudentCourse'

    def save(self, *args, **kwargs):
        self.is_active = self.student_semester.is_active
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.student_semester.student} - {self.course_offering.course.name}"
    
    @property
    def student(self):
        return self.student_semester.student
    
    @property
    def course(self):
        return self.course_offering.course
    
    @property
    def unit(self):
        return self.course_offering.course.unit
    

    
    def save(self, *args, **kwargs):
     
        if self.grade is not None:
            if self.grade >= 10:  
                self.status = 'passed'
                self.grade_date = timezone.now() if not self.grade_date else self.grade_date
            elif self.grade < 10 and self.status == 'enrolled':
                self.status = 'failed'
                self.grade_date = timezone.now() if not self.grade_date else self.grade_date              
        super().save(*args, **kwargs)

    
    def can_drop(self):
        """آیا می‌تواند درس را حذف کند؟"""
        if self.status != 'enrolled':
            return False
        
        enrollment_age = (timezone.now() - self.enrollment_date).days
        return enrollment_age <= 14  # 2 هفته
    
    def get_status_display_fa(self):
        status_dict = {
            'enrolled': 'در حال گذراندن',
            'passed': 'قبول شده',
            'failed': 'مردود شده',
            'dropped': 'حذف شده',
            'incomplete': 'ناتمام',
            'withdrawn': 'انصراف داده شده',
        }
        return status_dict.get(self.status, self.status)
    


"""
class StudentSemester(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    #student_code = models.CharField(default="none")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    #semester_code = models.IntegerField(default=20251) 

    total_units = models.PositiveSmallIntegerField(default=0,blank=True,null=True)
 
    min_units = models.PositiveSmallIntegerField(default=12,blank=True,null=True)
    max_units = models.PositiveSmallIntegerField(default=24,blank=True,null=True)

    class Meta:
        unique_together = ('student', 'semester')

    def __str__(self):
        return f"{self.semester}" #{self.student} -

        
class StudentCourse(models.Model):
    student_semester = models.ForeignKey(StudentSemester, on_delete=models.CASCADE)
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    #student = models.ForeignKey(User,on_delete=models.CASCADE)

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
"""

