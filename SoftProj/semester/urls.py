
from django.urls import path
from .api import *

urlpatterns = [
    path('api/student-semesters/set-units/', student_semester_maxmin_units,name='student_semester_maxmin_units'),
]
