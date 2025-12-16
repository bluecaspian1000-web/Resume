"""
# Student/tests/test_studentsemester_units.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from Student.models import Student,Semester, StudentSemester
from django.contrib.auth.models import User
from Student.models import Student

class StudentSemesterUnitsAPITest(TestCase):
    def setUp(self):
      
        self.user = User.objects.create_user(
            username="ali_student",
            password="123456",
            first_name="Ali",
            last_name="Ahmadi"
        )

        self.student = Student.objects.create(
            user=self.user,
            student_code="S1001",
            major="CS",
            entry_year=2025
        )

        # ساخت ترم
        self.semester = Semester.objects.create(year=2025, term=1) #, code=20251

        # ایجاد StudentSemester
        self.ss = StudentSemester.objects.create(
            student=self.student,
            semester=self.semester,
            min_units=12,
            max_units=24
        )

        self.url = "/api/student-semester/maxmin-units/"

    def test_update_units_success(self):
        data = {"student_code": "S1001", "semester_code": 20251, "min_units": 10, "max_units": 20}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ss.refresh_from_db()
        self.assertEqual(self.ss.min_units, 10)
        self.assertEqual(self.ss.max_units, 20)

    def test_update_units_missing_params(self):
        data = {"min_units": 10}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_update_units_not_found(self):
        data = {"student_code": "S9999", "semester_code": 99999, "min_units": 10, "max_units": 20}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.data)
"""