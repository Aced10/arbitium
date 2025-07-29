from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import get_api_key
from app.core.exchanges import EXCHANGES
from app.services.arbitrage_service import calculate_opportunities
from app.core.notifications import send_telegram_message

router = APIRouter(
    prefix="/execute", tags=["Execute"],
    dependencies=[Depends(get_api_key)]
)

class ExecuteRequest(BaseModel):
    symbol: str
    buy_exchange: str
    sell_exchange: str
    amount: float  # cantidad en base currency, p.ej. USDT

@router.post("")
async def execute_trade(req: ExecuteRequest):
    # Validar exchanges
    if req.buy_exchange not in EXCHANGES or req.sell_exchange not in EXCHANGES:
        raise HTTPException(400, "Exchange inválido")

    buy_exch = EXCHANGES[req.buy_exchange]
    sell_exch = EXCHANGES[req.sell_exchange]

    # Crear orden de compra y venta (market)
    try:
        order_buy = buy_exch.create_market_order(req.symbol, 'buy', req.amount)
        order_sell = sell_exch.create_market_order(req.symbol, 'sell', req.amount)
    except Exception as e:
        raise HTTPException(500, f"Error ejecutando trade: {e}")

    # Enviar alerta Telegram
    profit = ((order_sell['price'] - order_buy['price']) / order_buy['price']) * 100
    message = (
        f"🤖 Arbitraje automático ejecutado!\n"
        f"{req.symbol}: compro en {req.buy_exchange} a {order_buy['price']}, "
        f"vendo en {req.sell_exchange} a {order_sell['price']}\n"
        f"Profit: {round(profit,3)}%"
    )
    await send_telegram_message(message)

    return {"buy_order": order_buy, "sell_order": order_sell, "profit_percent": round(profit,3)}