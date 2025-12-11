# courses/urls.py
from django.urls import path
from .api_views import *
from .prerequisites_management import *

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
    path("api/courses/<int:course_id>/prerequisite/add/", add_prerequisite_by_code),
    path("api/courses/<int:course_id>/prerequisite/remove/", remove_prerequisite_by_code),

    # search courses by name and prof-name and semester
    path('api/courses/search/', search_courses, name='search_courses'),
    path('api/courses/search/', search_courses_by_semester, name='search_courses-by-semester'),

    # search courses by semester
    path('api/courses/semester/<str:semester>/', list_courses_by_semester, name='list_courses_by_semester'),

]