from pydantic import BaseModel, Field, TypeAdapter
from typing import Optional, List
from datetime import datetime

class DepartmentInfo(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Nome")
    manager_id: Optional[str] = Field(default=None, alias="GestorId")
    is_active: bool = Field(alias="Ativa")

class User(BaseModel):
    id: str = Field(alias="Id")
    
    full_name: str = Field(alias="Name")
    username: str = Field(alias="UserName") 
    email: str = Field(alias="Email")
    job_title: str = Field(alias="Cargo")
    
    department: DepartmentInfo = Field(alias="Departamento")
    
    company: str = Field(alias="Empresa")
    cost_center: str = Field(alias="CentroCusto")
    area: str = Field(alias="Area")
    division: str = Field(alias="Divisao")
    
    created_at: datetime = Field(alias="CriadoEm")
    accepted_at: Optional[datetime] = Field(default=None, alias="DataAceite")
    deleted_at: Optional[datetime] = Field(default=None, alias="ExcluidoEm")
    
    is_active: bool = Field(alias="Ativo")

    class Config:
        populate_by_name = True
