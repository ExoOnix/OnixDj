from django.http import HttpResponseRedirect
import requests
from django.conf import settings

def custom_confirm_email_view(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )