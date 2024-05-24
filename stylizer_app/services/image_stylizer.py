import tensorflow as tf
import tensorflow_hub as hub
import tempfile
from tensorflow.keras.preprocessing.image import array_to_img
import os

class ImageStylizer:
    def __init__(self, content_image_size=1024, style_image_size=512, default_images=None):
        self.default_content_image_size = content_image_size
        self.default_style_image_size = style_image_size
        self.content_image_size = content_image_size
        self.style_image_size = style_image_size    
        self.hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
        self.default_images = default_images or {
            'content': r'stylizer_app/Images/Golden_Gate_Bridge_from_Battery_Spencer.jpg',
            'style': r'stylizer_app/Images/The_Great_Wave_off_Kanagawa.jpg',
        }

    def load_image(self, uploaded_file, image_size):
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            img = tf.io.decode_image(tf.io.read_file(temp_file_path), channels=3, dtype=tf.float32)[tf.newaxis, ...]
            img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
            return img
        except Exception as e:
            raise IOError(f"Error loading image")
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def load_image_from_path(self, image_path, image_size):
        try:
            img = tf.io.decode_image(tf.io.read_file(image_path), channels=3, dtype=tf.float32)[tf.newaxis, ...]
            img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
            return img
        except Exception as e:
            raise IOError(f"Error loading image from path")

    def stylize_images(self, content_image, style_image):
        try:
            style_image = tf.nn.avg_pool(style_image, ksize=[3, 3], strides=[1, 1], padding='SAME')
            stylized_image = self.hub_module(tf.constant(content_image), tf.constant(style_image))[0]
            stylized_image = tf.squeeze(stylized_image, axis=0)
            # array_to_img(stylized_image).show()
            return array_to_img(stylized_image)
        except Exception as e:
            raise RuntimeError(f"Error during image stylization")

    def stylize_image(self, content_image_file, style_image_file):
        content_image = self.load_image(content_image_file, image_size=(self.content_image_size, self.content_image_size))
        style_image = self.load_image(style_image_file, image_size=(self.style_image_size, self.style_image_size))
        return self.stylize_images(content_image, style_image)

    def stylize_with_default_style(self, content_image_file):
        content_image = self.load_image(content_image_file, image_size=(self.content_image_size, self.content_image_size))
        style_image = self.load_image_from_path(self.default_images['style'], image_size=(self.style_image_size, self.style_image_size))
        return self.stylize_images(content_image, style_image)

    def stylize_with_default_images(self):
        content_image = self.load_image_from_path(self.default_images['content'], image_size=(self.content_image_size, self.content_image_size))
        style_image = self.load_image_from_path(self.default_images['style'], image_size=(self.style_image_size, self.style_image_size))
        return self.stylize_images(content_image, style_image)

    def stylize_with_default_content(self, style_image_file):
        content_image = self.load_image_from_path(self.default_images['content'], image_size=(self.content_image_size, self.content_image_size))
        style_image = self.load_image(style_image_file, image_size=(self.style_image_size, self.style_image_size))
        return self.stylize_images(content_image, style_image)


if __name__ == "__main__":
    stylizer = ImageStylizer()

    content_image_path = '../Images/Golden_Gate_Bridge_from_Battery_Spencer.jpg'
    style_image_path = '../Images/Golden_Gate_Bridge_from_Battery_Spencer.jpg'

    with open(content_image_path, 'rb') as content_file, open(style_image_path, 'rb') as style_file:
        stylized_image = stylizer.stylize_image(content_file, style_file)
        stylized_image.show()

    with open(content_image_path, 'rb') as content_file:
        stylized_image = stylizer.stylize_with_default_style(content_file)
        stylized_image.show()

    stylized_image = stylizer.stylize_with_default_images()
    stylized_image.show()

    with open(style_image_path, 'rb') as style_file:
        stylized_image = stylizer.stylize_with_default_content(style_file)
        stylized_image.show()