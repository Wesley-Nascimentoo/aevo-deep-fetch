from typing import List, Set
from src.services.fetch_all_ideas_service import fetch_all_ideas_service
from src.services.fetch_user_per_dep_service import fetch_users_per_dep
import datetime

async def filter_ideas_to_implements_per_dep(department_id: int) -> int:
    current_year = datetime.date.today().year
    
    start = f"01-01-{current_year} 00:00:00"
    end = f"31-12-{current_year} 23:59:59"
    
    ideas = await fetch_all_ideas_service({
        "DataCriacaoInicio": start,
        "DataCriacaoTermino": end 
    })
    
    users_from_dep = await fetch_users_per_dep(department_id)

    target_ids: Set[str] = {
        str(user.Id).strip()
        for user in users_from_dep
        if getattr(user, "Id", None)
    }
    
    ideas_to_implements = []
    
    for idea in ideas:
        
        implementers = getattr(idea, "ResponsaveisImplantacao", []) or []
        
        has_dep_implementer = False
        
        for implementer in implementers:
            
            implementer_id = None
            
            if isinstance(implementer, dict):
                implementer_id = implementer.get("Id")
            elif hasattr(implementer, "Id"):
                implementer_id = implementer.Id
            
            if implementer_id and str(implementer_id).strip() in target_ids:
                has_dep_implementer = True
                break
        
        if has_dep_implementer:
            ideas_to_implements.append(idea)
            
    return ideas_to_implements