from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = tag
        fields = '__all__'


class TextSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(max_length=255)

    class Meta:
        model = text
        fields = ['tags', 'text']

    def create(self, validated_data):
        obj, created = tag.objects.get_or_create(title=validated_data['tags'])
        if obj:
            text.objects.create(tag=obj, text=validated_data['text'])
            validated_data['tags'] = obj.id
        if created:
            text.objects.create(tag=obj, text=validated_data['text'])
            validated_data['tags'] = created.id
        return validated_data