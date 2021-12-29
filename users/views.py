from django.shortcuts import render
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from .serializers import LoginSerializer
from dj_rest_auth.views import sensitive_post_parameters_m


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_response(self):
        token = self.user.token
        response = Response(
            {
                'token': token
            }
        )
        cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
        cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
        cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
        cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')

        if cookie_name:
            expiration = (datetime.utcnow() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            response.set_cookie(
                cookie_name,
                token,
                expires=expiration,
                secure=cookie_secure,
                httponly=cookie_httponly,
                samesite=cookie_samesite
            )
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.user = serializer.validated_data

        return self.get_response()