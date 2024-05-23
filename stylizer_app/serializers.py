from rest_framework import serializers
from .models import StylizedImage

class ImageUploadSerializer(serializers.Serializer):
    content_image = serializers.ImageField(required=False)
    style_image = serializers.ImageField(required=False)

    def validate(self, data):
        if not data.get('content_image') and not data.get('style_image'):
            raise serializers.ValidationError("At least one image must be provided.")
        return data

class StylizedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StylizedImage
        fields = '__all__'
