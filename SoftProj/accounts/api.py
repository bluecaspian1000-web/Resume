
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None : #and user.is_professor
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "username": user.username,
                "email": user.email
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    return Response({"detail": "Invalid credentials or not a professor"}, status=401)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()  

        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
