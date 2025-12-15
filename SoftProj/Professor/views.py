from rest_framework.viewsets import permissions , ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from Professor.models import *
from Professor.serializers import * 

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProfessorFilter




class ProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer  
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfessorFilter
    permission_classes = [IsAdminUser]


    