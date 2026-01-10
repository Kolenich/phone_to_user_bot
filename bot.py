import re

from telegram import Update
from telegram.ext import ApplicationBuilder, filters, MessageHandler

TOKEN = '8315940582:AAG61eOqCLEDD4zz8SmL9fJ-Qp-rHCVQtto'


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


async def handle_message(update: Update, *args, **kwargs):
    phone_number = normalize_phone_number(update.message.text)

    if not phone_number:
        await update.message.reply_text(
            'Пожалуйста, введите российский номер телефона'
        )

    link = f'https://t.me/{phone_number}'

    await update.message.reply_text(link)


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
