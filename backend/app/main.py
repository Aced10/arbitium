from fastapi import FastAPI
from app.routers import prices, opportunities, execute
from app.core.scheduler import start_scheduler

app = FastAPI()

app.include_router(prices.router)
app.include_router(opportunities.router)
app.include_router(execute.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the backend application!"}

@app.on_event("startup")
async def on_startup():
    start_scheduler()