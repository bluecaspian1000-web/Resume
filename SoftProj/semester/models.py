from django.db import models


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

