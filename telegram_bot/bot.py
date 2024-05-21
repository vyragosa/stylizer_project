import logging
from io import BytesIO
import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

user_images = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! 🌟 Отправь мне два изображения: исходное и стиль, и я их стилизую! 🎨')

def handle_images(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    photo_file = update.message.photo[-1].get_file()

    photo_byte_array = BytesIO()
    photo_file.download(out=photo_byte_array)
    photo_byte_array.seek(0)

    if user_id in user_images:
        user_images[user_id]['style_image'] = photo_byte_array

        files = {
            'content_image': ('content_image.jpg', user_images[user_id]['content_image']),
            'style_image': ('style_image.jpg', user_images[user_id]['style_image'])
        }

        update.message.reply_text('Обрабатываю изображение, подожди немного...')
        response = requests.post('http://127.0.0.1:7777/stylize/', files=files)
        if response.status_code == 200:
            update.message.reply_photo(photo=BytesIO(response.content))
        else:
            update.message.reply_text('Не удалось стилизовать изображение. Попробуй снова. 😔')

        del user_images[user_id]
    else:
        user_images[user_id] = {'content_image': photo_byte_array}
        update.message.reply_text('Первое изображение получено. Теперь отправь изображение стиля.')


def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_images))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
