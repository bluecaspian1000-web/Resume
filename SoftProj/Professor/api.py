from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from .models import Professor
from rest_framework import status
from .serializers import  ProfessorSerializer
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def professor_list(request):
    professors = Professor.objects.all()
    data = [{"id": p.id, "name": str(p)} for p in professors]
    return Response(data)

"""
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def professor_register(request):
    serializer = ProfessorRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def professor_register(request):
    serializer = ProfessorSerializer(data=request.data)
    if serializer.is_valid():
        prof = serializer.save()
        refresh = RefreshToken.for_user(prof)
        return Response({
            "prof": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
