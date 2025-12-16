from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from courses.models import Course, CourseOffering, Session
from Professor.models import Professor
from accounts.models import User

class CourseOfferingAPITest(APITestCase):

    def setUp(self):
        # ساخت یوزر و استاد
        self.user = User.objects.create_user(username="prof1", password="testpass")
        self.professor = Professor.objects.create(user=self.user, professor_code="P001", first_name="John", last_name="Doe")
        
        # ساخت دوره
        self.course = Course.objects.create(name="Math", code="MATH101", unit=3)
        
        # ساخت session
        self.session1 = Session.objects.create(day_of_week="Saturday", time_slot="8-10", location="Room 101")
        self.session2 = Session.objects.create(day_of_week="Sunday", time_slot="10-12", location="Room 102")
        
        # URL اندپوینت ایجاد course offering
        self.url = reverse("courseoffering-list")  # اگر از DefaultRouter استفاده می‌کنی

    def test_create_course_offering(self):
        payload = {
            "course": self.course.id,
            "capacity": 30,
            "professor": self.professor.id,
            "sessions": [
                {"day_of_week": "Saturday", "time_slot": "8-10", "location": "Room 101"},
                {"day_of_week": "Sunday", "time_slot": "10-12", "location": "Room 102"}
            ],
            "semester": "1403-1",
            "group_code": "A1"
        }

        response = self.client.post(self.url, payload, format="json")
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseOffering.objects.count(), 1)
        self.assertEqual(CourseOffering.objects.first().course, self.course)
        self.assertEqual(CourseOffering.objects.first().sessions.count(), 2)
