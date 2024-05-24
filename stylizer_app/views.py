from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import StylizedImageStylizerSerializer, StylizedImageDefaultSerializer
from .services.image_stylizer import ImageStylizer
from drf_yasg.utils import swagger_auto_schema

class StylizeImageBaseView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    stylizer = ImageStylizer()

    def handle_stylization(self, content_image_file=None, style_image_file=None, use_default_style=False, use_default_images=False, use_default_content=False):
        try:
            if use_default_images:
                stylized_image = self.stylizer.stylize_with_default_images()
            elif use_default_content:
                stylized_image = self.stylizer.stylize_with_default_content(style_image_file)
            elif use_default_style:
                stylized_image = self.stylizer.stylize_with_default_style(content_image_file)
            else:
                stylized_image = self.stylizer.stylize_image(content_image_file, style_image_file)

            response = HttpResponse(content_type="image/jpeg")
            stylized_image.save(response, 'JPEG')
            return response
        except IOError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StylizeImageView(StylizeImageBaseView):
    @swagger_auto_schema(
        operation_description="Apply style transfer using provided content and style images",
        request_body=StylizedImageStylizerSerializer,
        responses={
            200: 'JPEG image of the stylized content',
            400: 'Bad Request - The submitted data was invalid.',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = StylizedImageStylizerSerializer(data=request.data)
        if serializer.is_valid():
            content_image = serializer.validated_data.get('content_image')
            style_image = serializer.validated_data.get('style_image')
            return self.handle_stylization(content_image, style_image)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StylizeWithDefaultStyleView(StylizeImageBaseView):
    @swagger_auto_schema(
        operation_description="Apply style transfer using provided content image and default style image",
        request_body=StylizedImageDefaultSerializer,
        responses={
            200: 'JPEG image of the stylized content',
            400: 'Bad Request - The submitted data was invalid.',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = StylizedImageDefaultSerializer(data=request.data)
        if serializer.is_valid():
            content_image = serializer.validated_data.get('image')
            return self.handle_stylization(content_image, use_default_style=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StylizeWithDefaultImagesView(StylizeImageBaseView):
    @swagger_auto_schema(
        operation_description="Apply style transfer using default content and style images",
        responses={
            200: 'JPEG image of the stylized content',
            400: 'Bad Request - The request could not be understood or was missing required parameters.',
        }
    )
    def get(self, request, *args, **kwargs):
        return self.handle_stylization(use_default_images=True)

class StylizeWithDefaultContentView(StylizeImageBaseView):
    @swagger_auto_schema(
        operation_description="Apply style transfer using default content image and provided style image",
        request_body=StylizedImageDefaultSerializer,
        responses={
            200: 'JPEG image of the stylized content',
            400: 'Bad Request - The submitted data was invalid.',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = StylizedImageDefaultSerializer(data=request.data)
        if serializer.is_valid():
            style_image = serializer.validated_data.get('image')
            return self.handle_stylization(style_image_file=style_image, use_default_content=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
