import os
from telegram import Bot
from telegram.error import TelegramError
from app.core.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Inicializa el bot de Telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_telegram_message(message: str) -> bool:
    """
    Envía una alerta al chat configurado en TELEGRAM_CHAT_ID.
    """
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        return True
    except TelegramError as e:
        # Loguear o manejar error según convenga
        print(f"Error enviando Telegram: {e}")
        return False