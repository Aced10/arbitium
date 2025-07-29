from app.core.db import db
import datetime

async def save_price_snapshot(prices: dict):
    await db.prices.insert_one({"timestamp": datetime.datetime.utcnow(), "prices": prices})

async def save_opportunities(opportunities: list):
    docs = [{**op, "timestamp": datetime.datetime.utcnow()} for op in opportunities]
    if docs:
        await db.opportunities.insert_many(docs)

async def save_trade(trade: dict):
    doc = {**trade, "timestamp": datetime.datetime.utcnow()}
    await db.trades.insert_one(doc)