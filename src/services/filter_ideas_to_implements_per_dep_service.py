from typing import List, Set
from src.services.fetch_all_ideas_service import fetch_all_ideas_service
from src.services.fetch_user_per_dep_service import fetch_users_per_dep
import datetime

async def filter_ideas_to_implements_per_dep(department_id: int) -> int:
    current_year = datetime.date.today().year
    
    start = f"{current_year}-01-01 00:00:00"
    end = f"{current_year}-12-31 23:59:59"
    
    ideas = await fetch_all_ideas_service({
        "DataCriacaoInicio": start,
        "DataCriacaoTermino": end,
        "itensPorPagina": 1000
    })
    
    print(f"Ideias encontradas: {len(ideas)}")
    
    users_from_dep = await fetch_users_per_dep({
        "DepartamentoId": department_id,
        "itensPorPagina": 1000,
        "Ativo": 1
    })

    print(f"Usuários no departamento {department_id}: {len(users_from_dep)}")
    
    target_ids: Set[str] = set()
    for user in users_from_dep:
        uid = user.get("Id") if isinstance(user, dict) else getattr(user, "Id", None)
        if uid:
            target_ids.add(str(uid).strip().lower())
    
    ideas_to_implements = []
    
    for idea in ideas:
                
        implementers = []
        
        if isinstance(idea, dict):
            implementers = idea.get("ResponsaveisImplantacao") or []
        else:
            implementers = getattr(idea, "ResponsaveisImplantacao", []) or []
        
        has_dep_implementer = False
        
        for implementer in implementers:
                        
            implementer_id = None
            
            if isinstance(implementer, dict):
                implementer_id = implementer.get("Id")
            elif hasattr(implementer, "Id"):
                implementer_id = implementer.Id
            
            if implementer_id and str(implementer_id).strip().lower() in target_ids:
                has_dep_implementer = True
                print(f"Ideia {idea.get('Id') if isinstance(idea, dict) else getattr(idea, 'Id')} tem responsável do setor.")
                break
        
        if has_dep_implementer:
            ideas_to_implements.append(idea)
    
    print(f"Total de ideias filtradas: {len(ideas_to_implements)}")

    return ideas_to_implements