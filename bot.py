import logging
import os
import re
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, filters, MessageHandler

load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def normalize_phone_number(text: str) -> str | None:
    """
    Преобразует текст в номер телефона в формате +79ХХХХХХХХХ
    :param text: вводимый текст
    :return: преобразованный телефон или None
    """
    digits = re.sub(r'\D', '', text)

    if digits.startswith('8'):
        digits = f'7{digits[1:]}'

    if digits.startswith('7') and len(digits) == 11:
        return f'+{digits}'

    return None


async def handle_message(update: Update, context):
    phone_number = update.message.text

    logger.info(f'{phone_number=}')

    normalized_phone_number = normalize_phone_number(phone_number)

    if not normalized_phone_number:
        await update.message.reply_text(
            'Пожалуйста, введите российский номер телефона'
        )
    else:
        link = f'https://t.me/{normalized_phone_number}'

        await update.message.reply_text(link)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == '__main__':
    main()
