from django.urls import path

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter
router.register(r'students',views.StudentViewSet)
router.register(r'student-course',views.StudentCourseViewSet)
router.register(r'student-semester',views.StudentSemesterViewSet)



urlpatterns = []
