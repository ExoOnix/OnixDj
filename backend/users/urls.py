from django.urls import path, include, re_path
from users.views import (
    custom_confirm_email_view,
    CustomVerifyEmailView,
    password_reset_confirm_redirect,
    GithubLogin,
)

urlpatterns = [
    path(
        "dj-rest-auth/password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
    re_path(
        r"^dj-rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        custom_confirm_email_view,
        name="account_confirm_email",
    ),
    path(
        "dj-rest-auth/registration/verify-email/",
        CustomVerifyEmailView.as_view(),
        name="custom_verify_email",
    ),
    path(
        "dj-rest-auth/registration/verify-email",
        CustomVerifyEmailView.as_view(),
        name="custom_verify_email",
    ),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path(
        "dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")
    ),
    path("dj-rest-auth/github/", GithubLogin.as_view(), name="github_login"),
]
