from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    content_image = serializers.ImageField()
    style_image = serializers.ImageField()