from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Support Models (Nested Objects) ---

class Creator(BaseModel):
    name: Optional[str] = Field(default=None, alias="Name")
    email: Optional[str] = Field(default=None, alias="Email")
    username: Optional[str] = Field(default=None, alias="Username")
    department_id: Optional[int] = Field(default=None, alias="DepartamentoId")
    is_active: Optional[bool] = Field(default=None, alias="Ativo")

class Implementer(BaseModel):
    """
    Model for 'ResponsaveisImplantacao'.
    Based on the snippet provided earlier.
    """
    idea_id: Optional[int] = Field(default=None, alias="IdeiaId")
    user_id: Optional[str] = Field(default=None, alias="Id")
    name: Optional[str] = Field(default=None, alias="Name")

class Campaign(BaseModel):
    id: int = Field(alias="Id")
    name: Optional[str] = Field(default=None, alias="Nome")
    title: Optional[str] = Field(default=None, alias="Titulo")
    start_date: Optional[datetime] = Field(default=None, alias="DataInicio")

class Department(BaseModel):
    id: int = Field(alias="Id")
    name: Optional[str] = Field(default=None, alias="Nome")
    is_active: Optional[bool] = Field(default=None, alias="Ativo")
    manager_id: Optional[str] = Field(default=None, alias="GestorId")
    manager_name: Optional[str] = Field(default=None, alias="Gestor")

class Theme(BaseModel):
    id: int = Field(alias="Id")
    name: Optional[str] = Field(default=None, alias="Nome")
    is_active: Optional[bool] = Field(default=None, alias="Ativo")
    manager_id: Optional[str] = Field(default=None, alias="GestorId")
    manager_name: Optional[str] = Field(default=None, alias="Gestor")
    sub_theme: Optional[Dict[str, Any]] = Field(default=None, alias="SubTema")

class Collaborator(BaseModel):
    id: Optional[str] = Field(default=None, alias="Id")
    name: Optional[str] = Field(default=None, alias="Nome")
    username: Optional[str] = Field(default=None, alias="UserName")
    email: Optional[str] = Field(default=None, alias="Email")
    is_active: Optional[bool] = Field(default=None, alias="Ativo")
    department: Optional[str] = Field(default=None, alias="Departamento")
    manager: Optional[str] = Field(default=None, alias="Gestor")

class AdditionalField(BaseModel):
    id: int = Field(alias="Id")
    idea_id: int = Field(alias="IdeiaId")
    label: Optional[str] = Field(default=None, alias="Label")
    value: Optional[str] = Field(default=None, alias="Valor")

class ClassificationCriteria(BaseModel):
    idea_id: int = Field(alias="IdeiaId")
    criteria_id: int = Field(alias="CriterioClassificacaoId")
    title: Optional[str] = Field(default=None, alias="CriterioClassificacaoTitulo")
    value: Optional[str] = Field(default=None, alias="CriterioClassificacaoValor")
    points: Optional[int] = Field(default=0, alias="CriterioClassificacaoPontos")

class Attachment(BaseModel):
    name: Optional[str] = Field(default=None, alias="Nome")
    url: Optional[str] = Field(default=None, alias="URL")

class Stage(BaseModel):
    """
    Stage model refactored based on real API JSON response.
    Includes labels, observations and flow/state IDs.
    """
    flow_id: Optional[int] = Field(default=None, alias="FluxoId")
    state_id: Optional[int] = Field(default=None, alias="EstadoId")
    idea_id: Optional[int] = Field(default=None, alias="IdeiaId")
    
    # Dates
    start_date: Optional[datetime] = Field(default=None, alias="DataEntrada")
    end_date: Optional[datetime] = Field(default=None, alias="DataSaida")
    
    days_in_stage: Optional[int] = Field(default=None, alias="DiasNaEtapa")
    
    # Labels (Multi-language support in API)
    label_pt: Optional[str] = Field(default=None, alias="LabelPt")
    label_en: Optional[str] = Field(default=None, alias="LabelEn")
    label_es: Optional[str] = Field(default=None, alias="LabelEs")
    
    observation: Optional[str] = Field(default=None, alias="Observacao")

# --- Main Model ---

class Idea(BaseModel):
    id: int = Field(alias="Id")
    
    # Status Info
    current_stage_name: Optional[str] = Field(default=None, alias="Estado")
    current_stage_id: int = Field(alias="EstadoId")
    
    # Dates
    updated_at: datetime = Field(alias="DataAtualizacao")
    created_at: datetime = Field(alias="CriadoEm")
    
    # Content
    title: Optional[str] = Field(default=None, alias="Titulo")
    description: Optional[str] = Field(default=None, alias="Descricao")
    benefit: Optional[str] = Field(default=None, alias="Beneficio")
    
    # Metrics
    return_value: Optional[float] = Field(default=0.0, alias="ValorRetorno")
    completion_percentage: Optional[float] = Field(default=0.0, alias="PercentualConcluido")
    
    # Creator info
    creator_id: Optional[str] = Field(default=None, alias="ElaboradorId")
    external_id: Optional[str] = Field(default=None, alias="IdExterno")

    # Nested Objects
    creator: Optional[Creator] = Field(default=None, alias="Elaborador")
    campaign: Optional[Campaign] = Field(default=None, alias="Campanha")
    department: Optional[Department] = Field(default=None, alias="Departamento")
    theme: Optional[Theme] = Field(default=None, alias="Tema")
    
    # Lists
    collaborators: List[Collaborator] = Field(default_factory=list, alias="Colaboradores")
    implementers: List[Implementer] = Field(default_factory=list, alias="ResponsaveisImplantacao")
    
    additional_fields: List[AdditionalField] = Field(default_factory=list, alias="CamposAdicionais")
    classification_criteria: List[ClassificationCriteria] = Field(default_factory=list, alias="CriteriosClassificacaoItens")
    attachments: List[Attachment] = Field(default_factory=list, alias="AnexosIdeia")
    stages: List[Stage] = Field(default_factory=list, alias="Etapas")

    class Config:
        populate_by_name = True
        extra = "ignore" # Ignora campos extras que não mapeamos para não dar erro