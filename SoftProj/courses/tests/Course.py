from django.test import TestCase
from django.core.exceptions import ValidationError
from courses.models import Course


class CourseModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name="Algorithms",
            code="CS101",
            unit=3
        )

    def test_course_creation(self):
        self.assertEqual(self.course.name, "Algorithms")
        self.assertEqual(self.course.code, "CS101")
        self.assertEqual(self.course.unit, 3)

    def test_course_str(self):
        self.assertEqual(str(self.course), "Algorithms (CS101)")

    def test_course_code_unique(self):
        with self.assertRaises(Exception):
            Course.objects.create(
                name="Advanced Algorithms",
                code="CS101",  # duplicate
                unit=3
            )

    def test_unit_min_validation(self):
        course = Course(
            name="Invalid Course",
            code="CS102",
            unit=0
        )
        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_unit_max_validation(self):
        course = Course(
            name="Invalid Course",
            code="CS103",
            unit=4
        )
        with self.assertRaises(ValidationError):
            course.full_clean()

    #  تست prerequisite
    def test_prerequisite_relationship(self):
        prereq = Course.objects.create(
            name="Programming Basics",
            code="CS100",
            unit=3
        )

        self.course.prerequisites.add(prereq)

        self.assertIn(prereq, self.course.prerequisites.all())
        self.assertIn(self.course, prereq.required_for.all())
