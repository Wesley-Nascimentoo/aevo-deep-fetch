from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


AEVO_URL = f"https://{os.getenv("AEVO_ENV")}.aevoinnovate.net/webapi/api/ApiExterna/v2/GetIdeias"

AEVO_TOKEN = os.getenv("AEVO_TOKEN_API")



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