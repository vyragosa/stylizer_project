import tensorflow as tf
import tensorflow_hub as hub
import tempfile
from tensorflow.keras.preprocessing.image import array_to_img

class ImageStylizer:
    def __init__(self, content_image_size=1024, style_image_size=512):
        self.content_image_size = content_image_size
        self.style_image_size = style_image_size    
        self.hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    def load_image(self, uploaded_file, image_size):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        img = tf.io.decode_image(tf.io.read_file(temp_file_path), channels=3, dtype=tf.float32)[tf.newaxis, ...]
        img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
        return img

    def stylize_image(self, content_image_file, style_image_file):
        content_image = self.load_image(content_image_file, image_size=(self.content_image_size, self.content_image_size))
        style_image = self.load_image(style_image_file, image_size=(self.style_image_size, self.style_image_size))

        style_image = tf.nn.avg_pool(style_image, ksize=[3, 3], strides=[1, 1], padding='SAME')
        stylized_image = self.hub_module(tf.constant(content_image), tf.constant(style_image))[0]
        stylized_image = tf.squeeze(stylized_image, axis=0)
        return array_to_img(stylized_image)
