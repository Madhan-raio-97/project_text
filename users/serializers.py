from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email', allow_blank=False)
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = self.authenticate(email=email, password=password)

            if not user:
                raise serializers.ValidationError({'error': 'Unable to login with provided credentials.'}, code='authorization')

        return user


