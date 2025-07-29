from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from app.core.config import API_KEY

API_KEY_HEADER_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Invalid or missing API Key")