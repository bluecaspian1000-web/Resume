# Student/tests/test_student_semester.py
from django.test import TestCase
from django.contrib.auth.models import User

from Student.models import Student, StudentSemester
from semester.models import Semester

class StudentSemesterModelTest(TestCase):
    def setUp(self):
        # ایجاد یک کاربر و دانشجو
        self.user = User.objects.create_user(username="ali_student", password="123")
        self.student = Student.objects.create(user=self.user, student_code="S001", first_name="Ali", last_name="Ahmadi")
        
        # ایجاد یک Semester
        self.semester = Semester.objects.create(year=2025, term=1)
        
        # ایجاد StudentSemester
        self.student_semester = StudentSemester.objects.create(
            student=self.student,
            semester=self.semester,
            total_units=15,
            status='normal',
            min_units=12,
            max_units=24
        )

    def test_student_semester_creation(self):
        # بررسی اینکه آبجکت ساخته شده
        self.assertEqual(self.student_semester.student, self.student)
        self.assertEqual(self.student_semester.semester, self.semester)
        self.assertEqual(self.student_semester.total_units, 15)
        self.assertEqual(self.student_semester.status, 'normal')
        self.assertEqual(self.student_semester.min_units, 12)
        self.assertEqual(self.student_semester.max_units, 24)

    def test_student_semester_str(self):
        # بررسی خروجی __str__
        expected_str = f"{self.student} - {self.semester}"
        self.assertEqual(str(self.student_semester), expected_str)
