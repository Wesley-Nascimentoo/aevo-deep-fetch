import requests
import json
from datetime import datetime
from typing import List
from pydantic import TypeAdapter

from src.config import Config
from src.models.idea_models import Idea

class IdeaService:
    """
    Service responsible for fetching Idea data from the external API.
    """

    def get_ideas_by_period(
        self, 
        start_date: datetime, 
        end_date: datetime, 
        page: int = 1, 
        accumulated_ideas: List[Idea] = None
    ) -> List[Idea]:
        
        if accumulated_ideas is None:
            accumulated_ideas = []

        try:
            date_fmt = "%Y-%m-%d %H:%M:%S"
            
            # --- CORRECTION IS HERE ---
            # We construct the filters dictionary including pagination inside it,
            # matching the "Example of filter" from the documentation.
            filters = {
                "DataCriacaoInicio": start_date.strftime(date_fmt),
                "DataCriacaoTermino": end_date.strftime(date_fmt),
                "itensPorPagina": 1000,  # Moved inside the JSON object
                "pagina": page           # Moved inside the JSON object
            }

            # Serialize without spaces to be safe
            filters_json = json.dumps(filters, separators=(',', ':'))

            # The 'params' sent to requests now mostly contains the token and the huge filter string
            params = {
                "token": Config.API_TOKEN,
                "filtros": filters_json
            }

            # Safety check for URL construction
            if "webapi" in Config.BASE_URL:
                 url = f"{Config.BASE_URL.rstrip('/')}/v2/GetIdeias"
            else:
                 url = f"{Config.BASE_URL.rstrip('/')}/webapi/api/ApiExterna/v2/GetIdeias"
            
            # Debug URL to confirm params are correct
            req_debug = requests.Request('GET', url, params=params).prepare()
            print(f"[IdeaService] Requesting URL: {req_debug.url}")

            response = requests.Session().send(req_debug)
            response.raise_for_status()
            
            data = response.json()

            # --- Extract Results ---
            raw_ideas_list = data.get("resultado", [])
            
            if raw_ideas_list:
                adapter = TypeAdapter(List[Idea])
                new_ideas = adapter.validate_python(raw_ideas_list)
                accumulated_ideas.extend(new_ideas)

            # --- Check Pagination ---
            # Even though we sent 1000, we check what the API returned just in case
            returned_items_per_page = data.get("itensPorPagina", 0) 
            total_pages = data.get("numeroPaginas", 1)
            current_page_api = data.get("paginaAtual", 1)

            print(f"[IdeaService] Page {current_page_api}/{total_pages} fetched. "
                  f"Items this page: {len(raw_ideas_list)} (Configured: {returned_items_per_page})")

            if current_page_api < total_pages:
                return self.get_ideas_by_period(
                    start_date, 
                    end_date, 
                    page + 1, 
                    accumulated_ideas
                )

            print(f"[IdeaService] Finished. Total ideas retrieved: {len(accumulated_ideas)}")
            return accumulated_ideas

        except Exception as e:
            print(f"[IdeaService] Error: {e}")
            raise

idea_service = IdeaService()