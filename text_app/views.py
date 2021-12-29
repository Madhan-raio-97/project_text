from django.shortcuts import render
from .serializer import TagSerializer, TextSerializer
from .models import *
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


class TagView(ModelViewSet):
    queryset = tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset()
        data = []
        for obj in queryset:
            data.append(obj.tag_list())
        if data:
            data.append({'total count': len(queryset)})
            return Response(data)
        return Response('No records')

    def retrieve(self, request, *args, **kwargs):
        response = list()
        for data in self.get_object().texts.all():
            response.append(
                {
                    'tags': self.get_object().title,
                    'text': data.text,
                    'created at': data.created_at,
                    'last modified': data.modified_at
                }
            )

        if response:
            response.append({'total count': len(response)})
            return Response(response)
        return Response('No records')

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TextView(ModelViewSet):
    queryset = text.objects.all()
    serializer_class = TextSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset()
        data = []
        for obj in queryset:
            data.append(obj.text_list())
        if data:
            data.append({'total count': len(queryset)})
            return Response(data)
        return Response('No records')

    def retrieve(self, request, *args, **kwargs):

        return Response(self.get_object().text_list())

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.retrieve(request, *args, **kwargs)
