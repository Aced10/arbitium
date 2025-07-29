import ccxt
from app.core.config import (
    BINANCE_API_KEY, BINANCE_SECRET,
    KRAKEN_API_KEY, KRAKEN_SECRET,
    KUCOIN_API_KEY, KUCOIN_SECRET,
    SYMBOLS,
)


EXCHANGES = {
    "binance": ccxt.binance(),
    "kraken": ccxt.kraken(),
    "kucoin": ccxt.kucoin(),
}

async def fetch_prices():
    """
    Obtiene el precio 'last' de cada símbolo en cada exchange.
    """
    results = {}
    for name, exchange in EXCHANGES.items():
        results[name] = {}
        for symbol in SYMBOLS:
            try:
                ticker = exchange.fetch_ticker(symbol)
                results[name][symbol] = ticker['last']
            except Exception:
                results[name][symbol] = None
    return results