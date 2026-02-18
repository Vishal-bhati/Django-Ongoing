from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny

User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            password=password
        )

        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )
    