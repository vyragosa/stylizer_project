import os
import requests
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '6639128192:AAEV_HHQKuIW_CZ-cA8Gie3pC6nidhb8xzA'
STYLIZE_URL = ''


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('2 изображения:')

def handle_images(update: Update, context: CallbackContext) -> None:
    if len(context.user_data.get('images', [])) < 2:
        photo = update.message.photo[-1]
        file = context.bot.getFile(photo.file_id)
        images = context.user_data.get('images', [])
        images.append(file.download_as_bytearray())
        context.user_data['images'] = images
        update.message.reply_text(f'Received image {len(images)}/2.')

        if len(images) == 2:
            stylize_images(update, context)
    else:
        update.message.reply_text('...')

def stylize_images(update: Update, context: CallbackContext) -> None:
    images = context.user_data['images']
    files = {
        'content_image': ('content.jpg', images[0], 'image/jpeg'),
        'style_image': ('style.jpg', images[1], 'image/jpeg')
    }

    response = requests.post(STYLIZE_URL, files=files)

    if response.status_code == 200 and response.headers['content-type'] == 'image/jpeg':
        with open('stylized_image.jpg', 'wb') as f:
            f.write(response.content)
        update.message.reply_photo(photo=open('stylized_image.jpg', 'rb'))
    else:
        update.message.reply_text('Не получилось')
    
    context.user_data['images'] = []

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_images))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()