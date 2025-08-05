import logging
from ccxt.async_support import PermissionDenied, AuthenticationError
from app.core.exchanges import EXCHANGES
from app.services.persistence_service import save_trade
from app.core.notifications import send_telegram_message


async def execute_trade_logic(symbol: str, buy_exchange: str, sell_exchange: str, amount: float) -> dict:
    """
    Ejecuta una operación de mercado de arbitraje entre dos exchanges.
    Maneja excepciones de permisos y autenticación.
    """
    buy_exch = EXCHANGES[buy_exchange]
    sell_exch = EXCHANGES[sell_exchange]

    # Opcional: verificar permisos básicos usando fetch_balance
    try:
        await buy_exch.fetch_balance()
        await sell_exch.fetch_balance()
    except (PermissionDenied, AuthenticationError) as e:
        logging.error(f"Permisos insuficientes en exchanges {buy_exchange}/{sell_exchange}: {e}")
        raise RuntimeError(f"Permisos insuficientes: {e}")
    except Exception as e:
        logging.warning(f"Advertencia verificación de permisos: {e}")

    # Intentar ejecutar órdenes de mercado
    try:
        order_buy = await buy_exch.create_market_order(symbol, 'buy', amount)
        order_sell = await sell_exch.create_market_order(symbol, 'sell', amount)
    except (PermissionDenied, AuthenticationError) as e:
        logging.error(f"Error de autorización en trade {symbol}@{buy_exchange}->{sell_exchange}: {e}")
        raise RuntimeError(f"Error de autorización: {e}")
    except Exception as e:
        logging.error(f"Error ejecutando trade {symbol}@{buy_exchange}->{sell_exchange}: {e}")
        raise

    # Calcular porcentaje de beneficio
    profit_percent = ((order_sell['price'] - order_buy['price']) / order_buy['price']) * 100
    trade = {
        "symbol": symbol,
        "buy_exchange": buy_exchange,
        "sell_exchange": sell_exchange,
        "buy_order": order_buy,
        "sell_order": order_sell,
        "profit_percent": round(profit_percent, 3),
    }

    # Guardar trade y enviar notificación
    await save_trade(trade)
    message = (
        f"🤖 AutoTrade: {symbol} | Buy @{order_buy['price']} ({buy_exchange}) | "
        f"Sell @{order_sell['price']} ({sell_exchange}) | Profit: {round(profit_percent, 3)}%"
    )
    await send_telegram_message(message)
    return trade