import httpx
import json
from fastapi import HTTPException
from src.core.config import settings

async def fetch_all_ideas_service(filters: dict) -> list:
    if not settings.AEVO_URL_GET_IDEAS:
        raise HTTPException(status_code=500, detail="Ambiente AEVO_ENV não configurado.")
    
    if not settings.AEVO_TOKEN:
        raise HTTPException(status_code=500, detail="Token AEVO não configurado.")

    accumulated = []
    page = 1
    total_pages = 1 
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        while page <= total_pages:
            current_filters = filters.copy()
            current_filters["pagina"] = page 
            
            json_filters = json.dumps(current_filters)
            
            params = {
                "token": settings.AEVO_TOKEN,
                "filtros": json_filters
            }
            
            try:
                response = await client.get(settings.AEVO_URL_GET_IDEAS, params=params)
                
                if response.status_code != 200:
                    print(f"Erro na API Aevo (Pág {page}): {response.status_code} - {response.text}")
                
                response.raise_for_status()
                data = response.json()
                
                items = data.get("resultado", [])
                total_pages = data.get("numeroPaginas") or 1
                
                accumulated.extend(items)
                
                print(f"Página {page} de {total_pages} processada. Itens: {len(items)}.")
                page += 1
                
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code, 
                    detail=f"Falha na API externa: {e.response.text}"
                )
            except Exception as e:
                print(f"Erro crítico: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
                
    return accumulated