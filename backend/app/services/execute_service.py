from app.core.exchanges import EXCHANGES
from app.services.persistence_service import save_trade
from app.core.notifications import send_telegram_message

async def execute_trade_logic(symbol: str, buy_exchange: str, sell_exchange: str, amount: float) -> dict:
    buy_exch = EXCHANGES[buy_exchange]
    sell_exch = EXCHANGES[sell_exchange]

    order_buy = buy_exch.create_market_order(symbol, 'buy', amount)
    order_sell = sell_exch.create_market_order(symbol, 'sell', amount)

    profit_percent = ((order_sell['price'] - order_buy['price']) / order_buy['price']) * 100
    trade = {
        "symbol": symbol,
        "buy_exchange": buy_exchange,
        "sell_exchange": sell_exchange,
        "buy_order": order_buy,
        "sell_order": order_sell,
        "profit_percent": round(profit_percent, 3),
    }

    await save_trade(trade)
    message = (
        f"🤖 AutoTrade: {symbol} | "
        f"Compra en {buy_exchange} a {order_buy['price']} | "
        f"Venta en {sell_exchange} a {order_sell['price']} | "
        f"Profit: {round(profit_percent,3)}%"
    )
    await send_telegram_message(message)
    return trade