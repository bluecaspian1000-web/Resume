from rest_framework.viewsets import permissions , ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import *
from .serializers import * 

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseOfferingFilter



class CourseOfferingViewSet(ModelViewSet):
    queryset = CourseOffering.objects.all().distinct()
    serializer_class = CourseOfferingSerializer  
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseOfferingFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCourseOfferingSerializer
        return super().get_serializer_class()



class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer  
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['day_of_week', 'time_slot', 'location']
    permission_classes = [IsAdminUser]




class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
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
    
    permission_classes = [IsAdminUser]
