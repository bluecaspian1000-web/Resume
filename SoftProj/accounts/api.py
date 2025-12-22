from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

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
            # صادر کردن توکن JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # تعیین نقش بر اساس گروه‌ها و is_staff
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
