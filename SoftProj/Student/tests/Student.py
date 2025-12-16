from django.test import TestCase
from django.contrib.auth.models import User
from Student.models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        # اول User بساز
        self.user = User.objects.create_user(
            username="ali_student",
            password="123",
            first_name="Ali",
            last_name="Ahmadi"
        )
        # بعد Student بساز و User رو وصل کن
        self.student = Student.objects.create(
            user=self.user,
            student_code="S101",
            major="Computer Science",
            entry_year=2025,
            gender="male",
            national_id="1234567890"
        )

    def test_student_str(self):
        self.assertEqual(str(self.student), self.user.username)

    def test_student_fields(self):
        self.assertEqual(self.student.major, "Computer Science")
        self.assertEqual(self.student.entry_year, 2025)
        self.assertEqual(self.student.gender, "male")
        self.assertEqual(self.student.national_id, "1234567890")
