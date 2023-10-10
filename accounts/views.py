from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer
from .serializers import UserRegistrationSerializer, UserSerializer
from .tokens import account_activation_token


class ActivateAccount(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Activate a user's account using a unique token.",
    )
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response("Account successfully activated", status=status.HTTP_200_OK)
        else:
            return Response(
                "Activation link is invalid", status=status.HTTP_400_BAD_REQUEST
            )


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        operation_description="Register a new user and send an account activation email.",
    )
    def perform_create(self, serializer):
        user = serializer.save()

        mail_subject = "Activate your marketplace account."
        message = render_to_string(
            "accounts/account_activation_email.html",
            {
                "user": user,
                "domain": "localhost:8000",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )

        send_mail(mail_subject, message, "thawatchai.cha@turbo.co.th", [user.email])


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile details.",
    )
    def get_object(self):
        return self.request.user
