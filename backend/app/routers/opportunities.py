from fastapi import APIRouter
from app.services.arbitrage_service import calculate_opportunities

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])

@router.get("")
async def get_opportunities():
    return {"opportunities": await calculate_opportunities()}