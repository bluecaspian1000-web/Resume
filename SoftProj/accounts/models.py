
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_professor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
"""