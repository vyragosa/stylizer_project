from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import ImageUploadSerializer
from .image_stylizer import ImageStylizer
from tensorflow.keras.preprocessing.image import array_to_img
from drf_yasg.utils import swagger_auto_schema

class StylizeImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="2 изображения",
        request_body=ImageUploadSerializer,
        responses={200: 'JPEG image of the stylized content'}
    )
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            content_image = serializer.validated_data['content_image']
            style_image = serializer.validated_data['style_image']

            stylizer = ImageStylizer()
            stylized_image = stylizer.stylize_image(content_image, style_image)

            img = array_to_img(stylized_image)
            response = HttpResponse(content_type="image/jpeg")
            img.save(response, 'JPEG')

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
