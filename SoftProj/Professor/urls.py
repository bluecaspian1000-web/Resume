from django.urls import path
#from .api import *

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter
router.register(r'Professor',views.ProfessorViewSet)

urlpatterns = [
    #path('api/professor/', professor_list,name='prof-list'),
    #path('api/professor/register/', professor_register,name='professor-register')
]