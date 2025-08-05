import os
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Lista de variables obligatorias
REQUIRED_VARS = [
    "API_KEY",
    "BINANCE_API_KEY",
    "BINANCE_SECRET",
    "KRAKEN_API_KEY",
    "KRAKEN_SECRET",
    "KUCOIN_API_KEY",
    "KUCOIN_SECRET",
    "KUCOIN_PASSWORD",
    "MONGODB_URI",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "SCHEDULER_INTERVAL",
]

missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing:
    raise RuntimeError(f"Faltan variables de entorno requeridas: {', '.join(missing)}")

# Configuración de símbolos y umbral de beneficio
SYMBOLS = os.getenv("SYMBOLS", "BTC/USDT,ETH/USDT,SOL/USDT").split(",")
try:
    MIN_PROFIT = float(os.getenv("MIN_PROFIT", "0.3"))
except ValueError:
    raise RuntimeError("MIN_PROFIT debe ser un número válido")

# Claves y tokens
API_KEY = os.getenv("API_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_SECRET = os.getenv("KRAKEN_SECRET")
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_SECRET = os.getenv("KUCOIN_SECRET")
KUCOIN_PASSWORD = os.getenv("KUCOIN_PASSWORD")

MONGODB_URI = os.getenv("MONGODB_URI")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# backend/app/core/security.py
import os
import logging
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from app.core.config import API_KEY

# Verificar presencia de API_KEY
if not API_KEY:
    raise RuntimeError("Falta variable de entorno: API_KEY")

# Permitir personalizar nombre de la cabecera via env
API_KEY_HEADER_NAME = os.getenv("API_KEY_HEADER_NAME", "X-API-KEY")
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    logging.warning(f"Acceso denegado: clave inválida '{{api_key}}'")
    raise HTTPException(status_code=403, detail="API Key inválida o ausente")
