from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer


class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(groups__name='prof').order_by('first_name')
