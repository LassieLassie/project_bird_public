from telegram_bot.model import ClassPredictor
import torch
from telegram_bot.config import reply_texts
import numpy as np
from PIL import Image
from io import BytesIO


token = '865496874:AAEnuxZDDJNAgAFNB25zDbagy-8JO1h-vRA'
model = ClassPredictor()


def send_prediction_on_photo(bot, update):
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    image_stream = BytesIO()
    image_file.download(out=image_stream)

    class_ = model.predict(image_stream)
    # теперь отправим результат
    update.message.reply_text(str(class_))
    print("Sent Answer to user, predicted: {}".format(class_))


if __name__ == '__main__':
    from telegram.ext import Updater, MessageHandler, Filters
    import logging

    # Включим самый базовый логгинг, чтобы видеть сообщения об ошибках
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    # используем прокси, так как без него у меня ничего не работало(
    updater = Updater(token=token)
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, send_prediction_on_photo))
    updater.start_polling()
