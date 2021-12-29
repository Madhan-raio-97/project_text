from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import TagView, TextView

router = routers.DefaultRouter()
router.register(r'tags', TagView)
router.register(r'shorttext', TextView)

urlpatterns = [
    path('', include(router.urls)),
]
