from django.db import models
from Student.models import Student


class Semester(models.Model):
    
    year = models.PositiveIntegerField(verbose_name="year")

    term = models.PositiveSmallIntegerField(
        verbose_name="term",
        help_text="1=First, 2=Second, 3=Summer"
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
