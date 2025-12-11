
from django.urls import path
from .api import login, logout

urlpatterns = [
    path('api/login/', login, name='login'),
    path('api/logout/', logout, name='logout'),
]
