from django.http import HttpResponseRedirect
from django.conf import settings
from dj_rest_auth.registration.views import VerifyEmailView, SocialLoginView
from dj_rest_auth.utils import jwt_encode
from .serializers import CustomUserDetailsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login as django_login
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.SITE_HOST
    client_class = OAuth2Client


def custom_confirm_email_view(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


class CustomVerifyEmailView(VerifyEmailView):
    def post(self, request, *args, **kwargs):
        # Deserialize the incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]

        # Retrieve the confirmation object
        confirmation = self.get_object()
        confirmation.confirm(self.request)

        # Generate JWT tokens for the user
        user = confirmation.email_address.user

        django_login(request, user)

        access_token, refresh_token = jwt_encode(user)

        user_data = CustomUserDetailsSerializer(user).data

        # Prepare the response data
        response_data = {
            "user": user_data,
            "access": str(access_token),
            "refresh": str(refresh_token),
        }

        # Optionally, set the refresh token as an HTTP-only cookie
        response = Response(response_data, status=status.HTTP_200_OK)
        return response
