from rest_framework import serializers

class StylizedImageStylizerSerializer(serializers.Serializer):
    content_image = serializers.ImageField(required=True, help_text="Изображение контента")
    style_image = serializers.ImageField(required=True, help_text="Изображение стиля")

class StylizedImageDefaultSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, help_text="Изображение стиля, либо контента")
