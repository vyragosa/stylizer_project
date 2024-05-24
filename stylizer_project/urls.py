from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from stylizer_app.views import StylizeImageView, StylizeWithDefaultStyleView, StylizeWithDefaultImagesView, StylizeWithDefaultContentView

schema_view = get_schema_view(
   openapi.Info(
      title="Image Stylizer API",
      default_version='v1',
      description="API for image stylization",
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stylize/', StylizeImageView.as_view(), name='stylize_image'),
    path('default-style/', StylizeWithDefaultStyleView.as_view(), name='stylize_with_default_style'),
    path('default-images/', StylizeWithDefaultImagesView.as_view(), name='stylize_with_default_images'),
    path('default-content/', StylizeWithDefaultContentView.as_view(), name='stylize_with_default_content'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]
