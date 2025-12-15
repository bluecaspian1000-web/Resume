from rest_framework.viewsets import permissions , ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import *
from .serializers import * 

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend



class SemesterViewSet(ModelViewSet):
    queryset = Semester.objects.all().distinct()
    serializer_class = SemesterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['year','term','code']
