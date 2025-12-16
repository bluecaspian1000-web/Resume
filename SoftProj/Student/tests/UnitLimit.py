from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from Student.models import Student, Semester, StudentSemester
from django.contrib.auth.models import User

class StudentSemesterUnitsAPITest(TestCase):
    def setUp(self):
        # ساخت client
        self.client = APIClient()

        # ساخت user و student
        self.user = User.objects.create_user(username="ali_student", password="123456")
        self.student = Student.objects.create(
            user=self.user,
            student_code="S1001",
            major="CS",
            entry_year=2025
        )

        # ساخت ترم با code
        self.semester = Semester.objects.create(year=2025, term=1, code=20251)

        # ایجاد StudentSemester
        self.ss = StudentSemester.objects.create(
            student=self.student,
            semester=self.semester,
            min_units=12,
            max_units=24
        )

        # URL دقیق مطابق router و action
        self.url = "/student-semester/maxmin-units/"  # اگر prefix دارید: "/api/student-semester/maxmin-units/"

    def test_update_units_success(self):
        """تست تغییر موفقیت‌آمیز min و max units"""
        data = {
            "student_code": "S1001",
            "semester_code": 20251,
            "min_units": 10,
            "max_units": 20
        }
        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ss.refresh_from_db()
        self.assertEqual(self.ss.min_units, 10)
        self.assertEqual(self.ss.max_units, 20)
        self.assertIn("min_units", response.data)
        self.assertIn("max_units", response.data)

    def test_update_units_missing_params(self):
        """تست وقتی student_code یا semester_code ارسال نشده"""
        data = {"min_units": 10}
        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "student_code and semester_code are required")

    def test_update_units_not_found(self):
        """تست وقتی StudentSemester موجود نیست"""
        data = {
            "student_code": "S9999",
            "semester_code": 99999,
            "min_units": 10,
            "max_units": 20
        }
        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "StudentSemester not found")
