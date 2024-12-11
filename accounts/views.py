from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import CustomUser
from .serializers import UserCreateSerializer
from .utils import send_activation_email


class AdminAddUserView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can access this endpoint

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)  # User is inactive initially
            send_activation_email(user)
            return Response(
                {"message": "User created successfully. Activation email sent."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(APIView):
    def post(self, request, uid, token):
        try:
            user = CustomUser.objects.get(pk=uid)
            token_generator = PasswordResetTokenGenerator()

            if not token_generator.check_token(user, token):
                return Response(
                    {"error": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Activate user and set password
            password = request.data.get("password")
            if not password:
                return Response(
                    {"error": "Password is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(password)
            user.is_active = True
            user.save()

            return Response(
                {"message": "Account activated successfully."},
                status=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid user ID."}, status=status.HTTP_404_NOT_FOUND
            )


class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password = request.data.get("password")
        password_confirm = request.data.get("password_confirm")

        if password == password_confirm:
            user.set_password(password)
            user.is_active = True
            user.save()
            return Response(
                {"message": "Password set successfully and account activated."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST
        )


class UserView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Retrieve all users."""
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new user."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update an existing user."""
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        """Delete a user."""
        try:
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return Response(
                {"message": "User deleted successfully."}, status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
