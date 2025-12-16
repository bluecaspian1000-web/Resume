from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from courses.models import Course, CourseOffering
from Professor.models import Professor
from django.contrib.auth.models import User

class CourseOfferingSearchAPITest(APITestCase):
    def setUp(self):
        # ساخت یوزر و پروف‌ها
        self.user1 = User.objects.create_user(username="ali", password="123")
        self.user2 = User.objects.create_user(username="reza", password="123")

        self.prof1 = Professor.objects.create(user=self.user1, first_name="Ali", last_name="Ahmadi", professor_code="P001")
        self.prof2 = Professor.objects.create(user=self.user2, first_name="Reza", last_name="Karimi", professor_code="P002")

        # ساخت دوره‌ها
        self.course1 = Course.objects.create(name="Mathematics", code="MATH101", unit=3)
        self.course2 = Course.objects.create(name="Physics", code="PHYS101", unit=2)

        # ساخت CourseOffering
        self.offering1 = CourseOffering.objects.create(course=self.course1, professor=self.prof1, capacity=30, semester="Fall", group_code="A")
        self.offering2 = CourseOffering.objects.create(course=self.course2, professor=self.prof2, capacity=25, semester="Fall", group_code="B")

        # URL endpoint جست‌وجو (فرض شده)
        self.search_url = reverse("courseoffering-search")

    def test_search_by_course_name(self):
        response = self.client.get(self.search_url, {"course_name": "mathematics"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["course"]["name"], "Mathematics")

    def test_search_by_professor_name(self):
        response = self.client.get(self.search_url, {"professor_name": "reza"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["professor"]["first_name"], "Reza")
