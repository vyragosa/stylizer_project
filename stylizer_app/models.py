from django.db import models

class StylizedImage(models.Model):
    content_image = models.ImageField(upload_to='content_images/')
    style_image = models.ImageField(upload_to='style_images/')
    stylized_image = models.ImageField(upload_to='stylized_images/')
    created_at = models.DateTimeField(auto_now_add=True)