from pydantic import BaseModel
from typing import List
# Importamos objetos básicos compartilhados (Status e Info da Ideia)
from src.models.analytics_models import StatusDistribution, IdeaBasicInfo

class IndividualUserReport(BaseModel):
    """
    Data Transfer Object (DTO) para o relatório individual.
    """
    user_matricula: str
    user_name: str
    target_year: int
    
    # --- Visão de Criador (Ideias enviadas) ---
    created_count: int
    created_status_distribution: List[StatusDistribution]
    
    # --- Visão de Implantador (Ideias para executar) ---
    pending_implementation_count: int
    pending_implementation_list: List[IdeaBasicInfo]
    
    completed_implementation_count: int
    # Opcional: Lista das concluídas se quiser exibir no futuro
    # completed_implementation_list: List[IdeaBasicInfo] = []