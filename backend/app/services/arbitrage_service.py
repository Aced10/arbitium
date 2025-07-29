from app.core.exchanges import fetch_prices, EXCHANGES
from app.core.config import SYMBOLS, MIN_PROFIT
from app.services.persistence_service import save_price_snapshot, save_opportunities
# from app.ml.predictor import predict_opportunity

async def calculate_opportunities(min_profit: float = MIN_PROFIT):
    prices = await fetch_prices()
    await save_price_snapshot(prices)

    opportunities = []
    for symbol in SYMBOLS:
        for buy_ex in EXCHANGES:
            for sell_ex in EXCHANGES:
                if buy_ex == sell_ex:
                    continue
                buy_price = prices[buy_ex].get(symbol)
                sell_price = prices[sell_ex].get(symbol)
                if not isinstance(buy_price, float) or not isinstance(sell_price, float):
                    continue
                profit = ((sell_price - buy_price) / buy_price) * 100
                if profit <= min_profit:
                    continue
                # success_prob = predict_opportunity(buy_price, sell_price, profit)
                op = {
                    "symbol": symbol,
                    "buy_exchange": buy_ex,
                    "sell_exchange": sell_ex,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "profit_percent": round(profit, 3),
                    # "success_prob": round(success_prob, 3),
                    "success_prob": round(0.4, 3),
                }
                opportunities.append(op)

    await save_opportunities(opportunities)
    return opportunities