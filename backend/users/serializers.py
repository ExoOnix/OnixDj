from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None  # Remove the username field
    email = serializers.EmailField(required=True)  # Add the email field

    def get_auth_user(self, username, password):
        # Since username is not used, replace it with email
        user = authenticate(email=username, password=password)
        return user

    def validate(self, attrs):
        # Override the validate method to use email instead of username
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = self.get_auth_user(email, password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')
                # Did we get back an active user?

                
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user, email=email)

        attrs['user'] = user
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered.")
        return email
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        return {
            'email': data.get('email'),
            'password1': data.get('password1'),
            'password2': data.get('password2'),
        }