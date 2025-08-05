import asyncio
import ccxt.async_support as ccxt
from app.core.config import (
    BINANCE_API_KEY, BINANCE_SECRET,
    KRAKEN_API_KEY, KRAKEN_SECRET,
    KUCOIN_API_KEY, KUCOIN_SECRET,KUCOIN_PASSWORD, 
    SYMBOLS,
)

EXCHANGES = {
    "binance": ccxt.binance({
        "apiKey": BINANCE_API_KEY,
        "secret": BINANCE_SECRET,
    }),
    "kraken": ccxt.kraken({
        "apiKey": KRAKEN_API_KEY,
        "secret": KRAKEN_SECRET,
    }),
    "kucoin": ccxt.kucoin({
        "apiKey": KUCOIN_API_KEY,
        "secret": KUCOIN_SECRET,
        "password": KUCOIN_PASSWORD,
    }),
}

async def fetch_prices():
    tasks = {
        name: [asyncio.create_task(ex.fetch_ticker(symbol)) for symbol in SYMBOLS]
        for name, ex in EXCHANGES.items()
    }

    results = {name: {} for name in EXCHANGES}
    for name, symbol_tasks in tasks.items():
        for symbol, task in zip(SYMBOLS, symbol_tasks):
            try:
                ticker = await task
                results[name][symbol] = ticker['last']
            except Exception:
                results[name][symbol] = None

    await asyncio.gather(*(ex.close() for ex in EXCHANGES.values()))
    return results