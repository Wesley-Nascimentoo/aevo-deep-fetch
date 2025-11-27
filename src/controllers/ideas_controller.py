from fastapi import APIRouter, Query
from typing import Optional
from src.services.fetch_all_ideas_service import fetch_all_ideas_service

router = APIRouter()

@router.get("/") 
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
    
    results = await fetch_all_ideas_service(filters=active_filters)

    return {
        "total_ideas_fetched": len(results),
        "ideas": results
    }