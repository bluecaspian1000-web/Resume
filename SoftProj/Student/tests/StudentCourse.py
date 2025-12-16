from django.test import TestCase
from courses.models import Course, CourseOffering
from Student.models import Student, StudentSemester, StudentCourse, Semester
from Professor.models import Professor
from django.contrib.auth.models import User

class StudentCourseModelTest(TestCase):
    def setUp(self):
        # ایجاد یوزر و دانشجو
        user_student = User.objects.create_user(username="ali_student", password="123")
        self.student = Student.objects.create(user=user_student, student_code="S101")

        # ایجاد یوزر و پروفسور
        user_prof = User.objects.create_user(username="prof_ahmadi", password="123")
        self.prof = Professor.objects.create(user=user_prof, professor_code="P101")

        # ایجاد یک Semester
        self.semester = Semester.objects.create(year=2025, term=1)

        # ایجاد StudentSemester
        self.student_sem = StudentSemester.objects.create(student=self.student, semester=self.semester)

        # ایجاد Course
        self.course = Course.objects.create(code="CSE101", name="Intro to CS")

        # ایجاد CourseOffering
        self.course_offering = CourseOffering.objects.create(
            course=self.course,         
            professor=self.prof,
            capacity=30,
            semester=str(self.semester),
            group_code="A"
        )

    def test_student_course_creation(self):
        sc = StudentCourse.objects.create(
            student_semester=self.student_sem,
            course_offering=self.course_offering,
            grade=18.5,
            status='enrolled'
        )
        self.assertEqual(sc.grade, 18.5)
        self.assertEqual(sc.status, 'enrolled')
        self.assertEqual(sc.student_semester, self.student_sem)
        self.assertEqual(sc.course_offering, self.course_offering)
