from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import *
from .serializers import *
from courses.serializers import CourseOfferingSerializer 

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *




class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer  
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    #permission_classes = [IsAdminUser]


class StudentSemesterViewSet(ModelViewSet):
    queryset = StudentSemester.objects.all()
    serializer_class = StudentSemesterSerializer  
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentSemesterFilter

    # max-min student-units
    @action(detail=False, methods=['patch'], url_path='maxmin-units') 
    def update_units(self, request):
      
        student_code = request.data.get("student_code")
        semester_code = request.data.get("semester_code")

        if not student_code or not semester_code:
            return Response(
                {"error": "student_code and semester_code are required"},
                status=400
            )

        try:
            ss = StudentSemester.objects.select_related(
                'student', 'semester'
            ).get(
                student__student_code=student_code,
                semester__code=semester_code
            )
        except StudentSemester.DoesNotExist:
            return Response(
                {"error": "StudentSemester not found"},
                status=404
            )

        serializer = StudentSemesterUnitsSerializer(ss, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    

    @action(detail=False, methods=['get'], url_path='courses-in-semester')
    def courses_in_semester(self, request):
        """
        جست و جوی دروس ارائه شده در یک ترم توسط کد ترم
        ?semester_code=20251
        """
        semester_code = request.query_params.get('semester_code')
        if not semester_code:
            return Response({"error": "semester_code is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            semester = Semester.objects.get(code=semester_code)
        except Semester.DoesNotExist:
            return Response({"error": "Semester not found"}, status=status.HTTP_404_NOT_FOUND)

        offerings = CourseOffering.objects.filter(semester=semester)
        serializer = CourseOfferingSerializer(offerings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    #permission_classes = [IsAdminUser]



class StudentCourseViewSet(ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentCourseFilter
    #permission_classes = [IsAdminUser]