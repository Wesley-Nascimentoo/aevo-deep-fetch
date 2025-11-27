from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import httpx
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()

AEVO_URL = "https://mondial.aevoinnovate.net/webapi/api/ApiExterna/v2/GetIdeias"

AEVO_TOKEN = os.getenv("AEVO_TOKEN_API")

async def fetch_all_ideas(token: str, filters: dict):
    accumulated = []
    page = 1
    total_pages = 1 
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        while page <= total_pages:
            current_filters = filters.copy()
            
            current_filters["pagina"] = page 
            
            json_filters = json.dumps(current_filters)
            
            params = {
                "token": token,
                "filtros": json_filters
            }
            
            try:
                response = await client.get(AEVO_URL, params=params)
                
                if response.status_code != 200:
                    print(f"Erro na API Aevo (Pág {page}): {response.status_code} - {response.text}")
                
                response.raise_for_status()
                
                data = response.json()
                
                items = data.get("resultado", [])
                
                total_pages = data.get("numeroPaginas") or 1
                
                accumulated.extend(items)
                
                print(f"Página {page} de {total_pages} processada. Itens nesta página: {len(items)}. Total acumulado: {len(accumulated)}")
                
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

@app.get("/")
async def get_ideas(
    DataCriacaoInicio: Optional[str] = Query(None),
    DataCriacaoTermino: Optional[str] = Query(None),
    DataAtualizacaoInicio: Optional[str] = Query(None),
    DataAtualizacaoTermino: Optional[str] = Query(None),
    EstadoId: Optional[int] = Query(None),
    DepartamentoId: Optional[int] = Query(None),
    TemaId: Optional[int] = Query(None),
    Titulo: Optional[str] = Query(None),
):
    if not AEVO_TOKEN:
        return {"erro": "Token da AEVO não configurado no .env"}

    raw_filters = {
        "DataCriacaoInicio": DataCriacaoInicio,
        "DataCriacaoTermino": DataCriacaoTermino,
        "DataAtualizacaoInicio": DataAtualizacaoInicio,
        "DataAtualizacaoTermino": DataAtualizacaoTermino,
        "EstadoId": EstadoId,
        "DepartamentoId": DepartamentoId,
        "TemaId": TemaId,
        "Titulo": Titulo,
        "itensPorPagina": 1000 
    }


    active_filters = {k: v for k, v in raw_filters.items() if v is not None}
    
    results = await fetch_all_ideas(
        token=AEVO_TOKEN,
        filters=active_filters
    )

    return {
        "total_ideas_fetched": len(results),
        "ideas": results
    }