from pydantic import BaseModel, Field
from typing import Optional
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
    email: Optional[str] = Field(default=None, alias="Email") # Good practice to make Email optional too
    job_title: Optional[str] = Field(default=None, alias="Cargo") # Job title can sometimes be null
    
    department: DepartmentInfo = Field(alias="Departamento")
    
    company: Optional[str] = Field(default=None, alias="Empresa")
    
    # --- FIX IS HERE: Changed to Optional[str] ---
    cost_center: Optional[str] = Field(default=None, alias="CentroCusto") 
    
    area: Optional[str] = Field(default=None, alias="Area")
    division: Optional[str] = Field(default=None, alias="Divisao")
    
    created_at: datetime = Field(alias="CriadoEm")
    accepted_at: Optional[datetime] = Field(default=None, alias="DataAceite")
    deleted_at: Optional[datetime] = Field(default=None, alias="ExcluidoEm")
    
    is_active: bool = Field(alias="Ativo")

    class Config:
        populate_by_name = True