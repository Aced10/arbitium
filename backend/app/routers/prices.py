from fastapi import APIRouter, Depends
from app.core.security import get_api_key
from app.core.exchanges import fetch_prices

router = APIRouter(
    prefix="/prices", tags=["Prices"],
    dependencies=[Depends(get_api_key)]
)
@router.get("")
async def get_prices():
    return {"data": await fetch_prices()}