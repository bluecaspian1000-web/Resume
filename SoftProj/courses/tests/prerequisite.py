# courses/tests/test_prerequisites.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from courses.models import Course

class PrerequisiteAPITest(APITestCase):

    def setUp(self):
        self.course1 = Course.objects.create(
            name="Algorithms",
            code="C101",
            unit=3
        )
        self.course2 = Course.objects.create(
            name="Data Structures",
            code="C102",
            unit=3
        )

        self.url = reverse("course-detail", args=[self.course1.id])

    def test_add_and_remove_prerequisite(self):

        #  add prerequisite
        response = self.client.patch(
            self.url,
            {"prerequisites": ["C102"]},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course1.refresh_from_db()
        self.assertIn(self.course2, self.course1.prerequisites.all())

        #  remove prerequisite
        response = self.client.patch(
            self.url,
            {"prerequisites": []},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course1.refresh_from_db()
        self.assertNotIn(self.course2, self.course1.prerequisites.all())
