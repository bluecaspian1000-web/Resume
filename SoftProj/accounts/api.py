from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    groups = list(user.groups.values_list('name', flat=True))
    role = groups[0] if groups else None
    return Response({
        'id': user.id,
        'username': user.username,
        'role': role
    })


"""
@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"detail": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        
        if user.groups.filter(name='admin').exists():
            role = 'admin'
        elif user.groups.filter(name='prof').exists():
            role = 'prof'
        else:
            role = 'student'

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role,
        }, status=status.HTTP_200_OK)
    
    # اگر authenticate ناموفق بود
    return Response(
        {"detail": "Invalid credentials"},
        status=status.HTTP_401_UNAUTHORIZED
    )
"""
"""
@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"detail": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user:
          
            refresh = RefreshToken.for_user(user)
            #access_token = str(refresh.access_token)
     
            if user.groups.filter(name='admin').exists() :
                role = 'admin'
            elif user.groups.filter(name='prof').exists():
                role = 'prof'
            else:
                role = 'student'

      
    return Response({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "role":role,
    }, status=status.HTTP_200_OK)
"""


@api_view(['POST'])
def logout_api(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

    except Exception:
        return Response(
            {"detail": "Invalid or expired token"},
            status=status.HTTP_400_BAD_REQUEST
        )
