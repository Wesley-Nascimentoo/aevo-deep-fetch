from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- MODELOS EXISTENTES (Mantidos) ---
class IdeaStatusSummary(BaseModel):
    title: str
    status: str

class UserRankingEntry(BaseModel):
    user_name: str
    total_ideas: int
    ideas_summary: List[IdeaStatusSummary] = Field(default_factory=list)

class StatusDistribution(BaseModel):
    status_title: str
    count: int
    percentage: float

class TimelineMetric(BaseModel):
    period: str
    sent_to_implementation_count: int = 0
    sent_for_validation_count: int = 0
    validated_implementation_count: int = 0

class DepartmentAnalytics(BaseModel):
    total_ideas_analyzed: int
    user_ranking: List[UserRankingEntry]
    status_distribution: List[StatusDistribution]
    monthly_timeline: List[TimelineMetric]
    weekly_timeline: List[TimelineMetric]

# --- NOVOS MODELOS PARA O RANKING DE CRIAÇÃO ---

class IdeaBasicInfo(BaseModel):
    id: int
    title: str
    status: str

class UserCreationStats(BaseModel):
    user_id: str
    user_name: str
    total_sent: int
    has_submitted_idea: bool
    
    # Metas Individuais
    hit_plr_target: bool
    hit_dept_individual_target: bool
    
    ideas: List[IdeaBasicInfo] = Field(default_factory=list)

class TimelineComparison(BaseModel):
    period: str
    total_sent: int
    target: int
    hit_target: bool

class CreationAnalytics(BaseModel):
    target_year: int
    
    # Ranking Individual
    user_ranking: List[UserCreationStats]
    
    # Resumo Coletivo (Departamento)
    monthly_timeline: List[TimelineComparison]
    weekly_timeline: List[TimelineComparison]