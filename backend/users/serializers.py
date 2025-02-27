from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

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

        attrs['user'] = user
        return attrs
