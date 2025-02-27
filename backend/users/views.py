from django.http import JsonResponse
import requests

def custom_confirm_email_view(request, key):
    base_url = request.build_absolute_uri('/api/')[:-1]
    api_url = f"{base_url}/dj-rest-auth/registration/verify-email/"

    response = requests.post(api_url, json={"key": key})

    if response.status_code == 200:
        return JsonResponse({"message": "Email verified successfully."})
    return JsonResponse({"error": "Invalid or expired key."}, status=400)
