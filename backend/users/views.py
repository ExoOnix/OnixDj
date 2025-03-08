from django.http import HttpResponseRedirect
from django.conf import settings
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.utils import jwt_encode
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login as django_login
from rest_framework.decorators import api_view


def custom_confirm_email_view(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
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

        # Prepare the response data
        response_data = {
            "user": str(user),
            "access": str(access_token),
            "refresh": str(refresh_token),
        }

        # Optionally, set the refresh token as an HTTP-only cookie
        response = Response(response_data, status=status.HTTP_200_OK)
        return response


@api_view(["GET"])
def hello_view(request):
    return Response("Hello, world!", content_type="text/plain")
