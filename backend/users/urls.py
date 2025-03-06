from django.urls import path, include, re_path
from users.views import custom_confirm_email_view

urlpatterns = [
    re_path(
        r"^dj-rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        custom_confirm_email_view,
        name="account_confirm_email",
    ),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path(
        "dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")
    ),
]
