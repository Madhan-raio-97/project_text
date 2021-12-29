from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = tag
        fields = '__all__'

    def create(self, validated_data):
        tag.objects.create(title=validated_data['title'], created_by=self.context.get('request').user)
        return validated_data

    def update(self, instance, validated_data):
        if self.context.get('request').user.is_authenticated:
            instance.modified_by = self.context.get('request').user
        return super().update(instance, validated_data)


class TextSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)

    class Meta:
        model = text
        fields = ['title', 'text']

    def create(self, validated_data):
        obj, created = tag.objects.get_or_create(title=validated_data['tags'])
        if obj:
            text.objects.create(tag=obj, text=validated_data['text'], created_by=self.context.get('request').user)
        if created:
            text.objects.create(tag=obj, text=validated_data['text'], created_by=self.context.get('request').user)
        return validated_data

    def update(self, instance, validated_data):
        if self.context.get('request').user.is_authenticated:
            instance.modified_by = self.context.get('request').user
        return super().update(instance, validated_data)