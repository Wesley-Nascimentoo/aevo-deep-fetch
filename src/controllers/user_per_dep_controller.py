from fastapi import APIRouter, Query
from src.services.fetch_user_per_dep_service import fetch_users_per_dep

router = APIRouter()

@router.get("/") 
async def get_users_per_dep(
    DepartamentoId: int = Query(None),

):
    raw_filters = {
        "Ativo": 1,
        "DepartamentoId": DepartamentoId,
        "itensPorPagina": 1000 
    }

    active_filters = {k: v for k, v in raw_filters.items() if v is not None}
    
    results = await fetch_users_per_dep(filters=active_filters)

    return {
        "total_users_fetched": len(results),
        "users": results
    }