from django.db import models
from accounts.models import User

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor_profile")
    first_name = models.CharField(max_length=100, verbose_name="first name")
    last_name = models.CharField(max_length=100, verbose_name="last name")
    professor_code = models.CharField(max_length=20, unique=True, verbose_name="professor code")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "professor"
        verbose_name_plural = "professors"