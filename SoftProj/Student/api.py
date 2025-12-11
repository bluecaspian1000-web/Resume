from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from .models import Student
from rest_framework import status
from .serializers import  StudentSerializer
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def student_list(request):
    students = Student.objects.all()
    data = [{"id": p.id, "name": str(p)} for p in students]
    return Response(data)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def student_register(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        student = serializer.save()
        refresh = RefreshToken.for_user(student)
        return Response({
            "prof": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
