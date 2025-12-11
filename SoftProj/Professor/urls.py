from django.urls import path
from .api import *

urlpatterns = [
    path('api/professor/', professor_list,name='prof-list'),
    #path('api/Professor/create/', professor_create),
    #path('api/register_Prof/', professor_register, name='professor-register'),
    path('api/professor/register/', professor_register,name='professor-register')
]