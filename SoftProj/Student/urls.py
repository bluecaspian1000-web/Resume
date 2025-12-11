from django.urls import path
from .api import *

urlpatterns = [
    path('api/student/', student_list,name='student-list'),
    path('api/student/register/', student_register,name='student-register'),
]
