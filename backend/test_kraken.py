import asyncio
import ccxt.async_support as ccxt

async def main():
    ex = ccxt.kraken({
        

        "apiKey": "3dsveppuRYPA9SgwCeEi2frF9xu/28tMHwX9rsbnuN791aX8OIAK/sMA",
        # "apiKey": "OJjzMyAYCT7ccIV7yKu3MrJ7Dtli4YhuGHCxS1F/aGB3z1R1X+hirkcP",
        "secret": "ARlIk3InAXcWLxLFcQKkJ+om/xCX25RxmKZCHWjMDCBbp6TbjF6dBVPxxGMWdNrS3XoLia4wrx4RzcHG5XRYGA=="
        # "secret": "W/ciytRBzA+YBBVyYjATXJJldbzatmUvpEFL4o2lx/TCoRNwkLUOERDC93I2pXi+oTAO0yZY/v8IMD7JUcBizg=="
    })
    try:
        # bal = await ex.create_market_order('SOL/USDT', 'buy', 1)
        bal = await ex.fetch_balance()
        print("✅ Balance OK:", bal)
    except Exception as e:
        print("❌ Error en fetch_balance():", e)
    finally:
        await ex.close()

asyncio.run(main())
