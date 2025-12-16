from django.db import models
from django.contrib.auth.models import User

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name="first name")
    last_name = models.CharField(max_length=100, verbose_name="last name")
    manager_code = models.CharField(max_length=20, unique=True, verbose_name="manager code")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "manager"
        verbose_name_plural = "managers"