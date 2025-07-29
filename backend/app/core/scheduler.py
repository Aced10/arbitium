from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.arbitrage_service import calculate_opportunities
from app.services.persistence_service import save_trade
from app.core.notifications import send_telegram_message
from app.services.execute_service import execute_trade_logic
from app.core.config import MIN_PROFIT

# Umbral de probabilidad para ejecución automática
AUTO_EXECUTE_THRESHOLD = 0.8

scheduler = AsyncIOScheduler()

async def periodic_task():
    # Recolecta oportunidades y almacena en DB
    ops = await calculate_opportunities()
    # Para cada oportunidad con alta probabilidad, ejecuta el trade
    print(f"Found {len(ops)} opportunities")
    for op in ops:
        if op['success_prob'] >= AUTO_EXECUTE_THRESHOLD:
            trade = await execute_trade_logic(
                symbol=op['symbol'],
                buy_exchange=op['buy_exchange'],
                sell_exchange=op['sell_exchange'],
                amount=op['calculate_amount'](op['buy_price'])  # función que convierte monto
            )
            # Guarda trade en DB
            await save_trade(trade)
            # Envía alerta
            msg = (
                f"🤖 AutoTrade: {trade['symbol']} | "
                f"Buy @{trade['buy_order']['price']} ({trade['buy_exchange']}) | "
                f"Sell @{trade['sell_order']['price']} ({trade['sell_exchange']}) | "
                f"Profit: {round(trade['profit_percent'],3)}%"
            )
            await send_telegram_message(msg)

def start_scheduler():
    # Ejecutar cada 10 segundos, usando la función async directamente
    scheduler.add_job(periodic_task, 'interval', seconds=10)
    scheduler.start()