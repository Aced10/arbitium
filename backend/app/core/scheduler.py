import os
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.arbitrage_service import calculate_opportunities
from app.services.execute_service import execute_trade_logic

# Umbral de probabilidad para ejecución automática
AUTO_EXECUTE_THRESHOLD = float(os.getenv("AUTO_EXECUTE_THRESHOLD", "0.7"))
# Proporción del capital a usar en cada trade (0.0 - 1.0)
EXECUTE_CAPITAL_RATIO = float(os.getenv("EXECUTE_CAPITAL_RATIO", "0.5"))

scheduler = AsyncIOScheduler()

async def periodic_task():
    """
    Tarea periódica que calcula oportunidades y ejecuta trades con alta probabilidad.
    """
    try:
        ops = await calculate_opportunities()
        logging.info(f"Found {len(ops)} opportunities")
    except Exception as exc:
        logging.error(f"Error calculating opportunities: {exc}")
        return

    for op in ops:
        if op.get('success_prob', 0) >= AUTO_EXECUTE_THRESHOLD:
            # Calcular monto a operar (por ejemplo: ratio * buy_price)
            amount = op['buy_price'] * EXECUTE_CAPITAL_RATIO
            try:
                trade = await execute_trade_logic(
                    symbol=op['symbol'],
                    buy_exchange=op['buy_exchange'],
                    sell_exchange=op['sell_exchange'],
                    amount=amount,
                )
                logging.info(f"Executed auto trade: {trade}")
            except Exception as e:
                logging.error(
                    f"Auto trade error for {op['symbol']} on {op['buy_exchange']}->{op['sell_exchange']}: {e}"
                )


def start_scheduler():
    """
    Inicia el scheduler para ejecutar periodic_task cada X segundos.
    """
    interval_seconds = int(os.getenv("SCHEDULER_INTERVAL", "10"))
    scheduler.add_job(
        periodic_task,
        'interval',
        seconds=interval_seconds,
        replace_existing=True
    )
    scheduler.start()
