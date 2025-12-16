from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import *
from .serializers import * 

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
    

    #permission_classes = [IsAdminUser]



class StudentCourseViewSet(ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentCourseFilter
    #permission_classes = [IsAdminUser]