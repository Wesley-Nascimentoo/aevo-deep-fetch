import httpx

aevo_get_ideas_v2_url = "https://seuambiente.aevoinnovate.net/webapi/api/ApiExterna/v2/GetIdeias"

def deepfetch(
    token: str,
    filters: dict,
    page: int = 1,
    accumulated: list = None
):
    """

    """

    if accumulated is None:
        accumulated = []
        
    if filters is None:
        filters = {}
    
    filters_with_page = {
        "page": page,
        **filters
    }
    
    params = {
        "token": token,
        "filtros": filters_with_page
    }
    
    res = httpx.get(aevo_get_ideas_v2_url, params=params)
    res.raise_for_status()
    data = res.json()
    
    items = data.get("resultado", [])
    total_pages = data.get("numeroPaginas", 1)
    currentPage = data.get("paginaAtual", page)
    
    accumulated.extend(items)
    
    if currentPage < total_pages:
        return deepfetch(
            token=token,
            filters= filters,
            page = currentPage + 1,
            accumulated= accumulated
        )
    
    return accumulated
    