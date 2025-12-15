# courses/urls.py
from django.urls import path

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter
router.register(r'courses',views.CourseViewSet)
router.register(r'course-offering',views.CourseOfferingViewSet)
router.register(r'sessions',views.SessionViewSet)



urlpatterns = [ ]