import logging
from io import BytesIO
import os
import requests
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')

user_images = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! 🌟 Отправь мне два изображения: исходное и стиль, и я их стилизую! 🎨')

# Обработчик команды /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Доступные команды:\n'
        '/start - Запустить бота\n'
        '/help - Показать это сообщение\n'
        '/stylize - Стилизовать, используя предоставленные изображения содержимого и стиля\n'
        '/default_style - Стилизовать, используя предоставленное изображение содержимого и изображение стиля по умолчанию\n'
        '/default_images - Стилизовать, используя изображения содержимого и стиля по умолчанию\n'
        '/default_content - Стилизовать, используя изображение содержимого по умолчанию и предоставленное изображение стиля\n'
        '/reset - Сбросить изображения'
    )

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
        response = requests.post(BACKEND_URL + '/stylize/', files=files)
        if response.status_code == 200:
            update.message.reply_photo(photo=BytesIO(response.content))
        else:
            update.message.reply_text('Не удалось стилизовать изображение. Попробуй снова. 😔')

        del user_images[user_id]
    else:
        user_images[user_id] = {'content_image': photo_byte_array}
        update.message.reply_text('Первое изображение получено. Теперь отправь изображение стиля.')

def reset(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_images:
        del user_images[user_id]
    update.message.reply_text('Изображения сброшены. Отправьте изображения для стилизации заново.')

def stylize(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_images or 'content_image' not in user_images[user_id] or 'style_image' not in user_images[user_id]:
        update.message.reply_text('Пожалуйста, отправьте два изображения для стилизации.')
        return

    files = {
        'content_image': ('content_image.jpg', user_images[user_id]['content_image']),
        'style_image': ('style_image.jpg', user_images[user_id]['style_image'])
    }

    response = requests.post(BACKEND_URL + '/stylize/', files=files)
    if response.status_code == 200:
        stylized_image = BytesIO(response.content)
        update.message.reply_photo(photo=InputFile(stylized_image, filename='stylized.jpg'))
    else:
        update.message.reply_text('Не удалось стилизовать изображение. Попробуй снова. 😔')

def default_style(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_images or 'content_image' not in user_images[user_id]:
        update.message.reply_text('Пожалуйста, отправьте изображение для стилизации.')
        return

    files = {
        'content_image': ('content_image.jpg', user_images[user_id]['content_image'])
    }

    response = requests.post(BACKEND_URL + '/default-style/', files=files)
    if response.status_code == 200:
        stylized_image = BytesIO(response.content)
        update.message.reply_photo(photo=InputFile(stylized_image, filename='stylized.jpg'))
    else:
        update.message.reply_text('Не удалось стилизовать изображение. Попробуй снова. 😔')

def default_images(update: Update, context: CallbackContext) -> None:
    response = requests.get(BACKEND_URL + '/default-images/')
    if response.status_code == 200:
        stylized_image = BytesIO(response.content)
        update.message.reply_photo(photo=InputFile(stylized_image, filename='stylized.jpg'))
    else:
        update.message.reply_text('Не удалось стилизовать изображение. Попробуй снова. 😔')

def default_content(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_images or 'style_image' not in user_images[user_id]:
        update.message.reply_text('Пожалуйста, отправьте изображение для стилизации.')
        return

    files = {
        'style_image': ('style_image.jpg', user_images[user_id]['style_image'])
    }

    response = requests.post(BACKEND_URL + '/default-content/', files=files)
    if response.status_code == 200:
        stylized_image = BytesIO(response.content)
        update.message.reply_photo(photo=InputFile(stylized_image, filename='stylized.jpg'))
    else:
        update.message.reply_text('Не удалось стилизовать изображение. Попробуй снова. 😔')

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("stylize", stylize))
    dispatcher.add_handler(CommandHandler("default_style", default_style))
    dispatcher.add_handler(CommandHandler("default_images", default_images))
    dispatcher.add_handler(CommandHandler("default_content", default_content))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_images))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()