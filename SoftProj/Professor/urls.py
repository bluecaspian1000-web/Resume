from django.urls import path
from .api import *

urlpatterns = [
    path('api/professor/', professor_list,name='prof-list'),
    path('api/professor/register/', professor_register,name='professor-register')
]