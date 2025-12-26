from rest_framework.routers import DefaultRouter
from .views import CourseOfferingViewSet, CourseViewSet, SessionViewSet, SemesterViewSet

#app_name = "courses"
router = DefaultRouter()

router.register(r'courseofferings', CourseOfferingViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'semesters', SemesterViewSet)


urlpatterns = router.urls
