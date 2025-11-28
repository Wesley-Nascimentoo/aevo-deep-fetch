from fastapi import APIRouter, Query
from src.services.filter_ideas_to_implements_per_dep_service import filter_ideas_to_implements_per_dep

router = APIRouter()

@router.get("/") 
async def get_ideas_to_implements(
    DepartamentoId: int = Query(None),

):
    results = await filter_ideas_to_implements_per_dep(DepartamentoId)

    return {
        "total_ideas_fetched": len(results),
        "ideas": results
    }