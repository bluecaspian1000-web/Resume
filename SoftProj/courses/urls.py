# courses/urls.py
from django.urls import path
from .api_views import *

urlpatterns = [
    # CRUD
    path('api/courses/', get_courses),
    path('api/courses/<int:id>/', get_course),
    path('api/courses/create/', create_course),
    path('api/courses/<int:id>/update/', update_course),
    path('api/courses/<int:id>/delete/', delete_course),

    # Prerequisites management
    path('api/courses/<int:course_id>/prerequisite/add/<prereq_id>/',add_prerequisite),
    path('api/courses/<int:course_id>/prerequisite/remove/<prereq_id>/',remove_prerequisite),
    path("courses/<int:course_id>/prerequisite/add/", add_prerequisite_by_code),
    path("courses/<int:course_id>/prerequisite/remove/", remove_prerequisite_by_code),

]