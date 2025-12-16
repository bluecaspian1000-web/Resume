"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from Student.models import Semester
from courses.models import Course, CourseOffering
from courses.serializers import CourseOfferingSerializer
from django.contrib.auth.models import User
from Professor.models import Professor


class StudentSemesterCoursesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

       # 1. ساخت User
        user = User.objects.create_user(
            username="prof1",
            password="123456",
            first_name="Ali",
            last_name="Ahmadi"
        )

        # 2. ساخت Professor با User
        self.professor = Professor.objects.create(
            user=user,
            professor_code="P001",
            first_name=user.first_name,
            last_name=user.last_name
        )
        # ساخت درس‌ها
        self.course1 = Course.objects.create(name="Course 1", code="C001")
        self.course2 = Course.objects.create(name="Course 2", code="C002")

        # ساخت ترم نمونه
        self.semester = "20251"

        # ساخت CourseOffering
        self.offering1 = CourseOffering.objects.create(
            course=self.course1,
            professor=self.professor,
            semester=self.semester,
            group_code="A1",
            capacity=30
        )
        self.offering2 = CourseOffering.objects.create(
            course=self.course2,
            professor=self.professor,
            semester=self.semester,
            group_code="B1",
            capacity=30
        )

        self.url = "/api/student-semester/courses-in-semester/"

    def test_get_courses_in_semester_success(self):
        """دریافت موفق دروس ارائه شده در ترم"""
        response = self.client.get(self.url, {"semester_code": 20251})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # بررسی تعداد دروس برگردانده شده
        self.assertEqual(len(response.data), 2)

        # بررسی کد دروس
        codes = [c["course_code"] for c in response.data]
        self.assertIn("MATH101", codes)
        self.assertIn("PHY101", codes)

    def test_get_courses_in_semester_missing_code(self):
        """درخواست بدون ارسال کد ترم"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_get_courses_in_semester_not_found(self):
        """درخواست برای ترم موجود نیست"""
        response = self.client.get(self.url, {"semester_code": 99999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
"""