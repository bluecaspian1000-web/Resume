from rest_framework.viewsets import  ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import *
from .serializers import * 

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseOfferingFilter
from students.models import *



class CourseOfferingViewSet(ModelViewSet):
    queryset = CourseOffering.objects.filter(semester__is_active=True).distinct()
    #permission_classes = [IsAuthenticated] 
    """
    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='student').exists():
            try:
                active_semester = StudentSemester.objects.filter(
                    student_id=user.id,
                    is_active=True
                ).latest('semester__year', 'semester__term')
            except StudentSemester.DoesNotExist:
                return CourseOffering.objects.none()
            
            return CourseOffering.objects.filter(semester=active_semester) #semester

        if user.groups.filter(name__in=['admin', 'prof']).exists():
            return CourseOffering.objects.all()
        
        return CourseOffering.objects.all()
    """
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseOfferingFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseOfferingReadSerializer
        return CourseOfferingWriteSerializer
    
    #lookup_field = 'code'          
    #lookup_url_kwarg = 'code'



class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer  
    #permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['day_of_week', 'time_slot', 'location']


class SemesterViewSet(ModelViewSet):
    queryset = Semester.objects.all().distinct()
    serializer_class = SemesterSerializer
    #permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['year','term','code']
    

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    #permission_classes = [IsAuthenticated] 

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseReadSerializer
        return CourseCreateSerializer
    
    #serializer_class = CourseSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['code', 'name', 'unit']
    
    @action(detail=False, methods=["post"], url_path="add-prerequisite")
    def add_prerequisite(self, request):

        serializer = PrerequisiteSerializer(
            data=request.data,
            context={"mode": "add"}
        )
        serializer.is_valid(raise_exception=True)

        course = serializer.validated_data["course"]
        prereq = serializer.validated_data["prereq"]

        course.prerequisites.add(prereq)

        return Response(
            {"message": "Prerequisite added"},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="remove-prerequisite")
    def remove_prerequisite(self, request):

        serializer = PrerequisiteSerializer(
            data=request.data,
            context={"mode": "remove"}
        )
        serializer.is_valid(raise_exception=True)

        course = serializer.validated_data["course"]
        prereq = serializer.validated_data["prereq"]

        course.prerequisites.remove(prereq)

        return Response(
            {"message": "Prerequisite removed"},
            status=status.HTTP_200_OK
        )
    
   
