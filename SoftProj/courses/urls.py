from rest_framework.routers import DefaultRouter
from .views import CourseOfferingViewSet, CourseViewSet, SessionViewSet

#app_name = "courses"
router = DefaultRouter()

router.register(r'courseofferings', CourseOfferingViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'sessions', SessionViewSet)

urlpatterns = router.urls
