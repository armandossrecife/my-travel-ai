"""API request and response schemas."""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class PlanRequest(BaseModel):
    cidade_destino: str = Field(..., description="Cidade de destino")
    data_saida: date = Field(..., description="Data de início (YYYY-MM-DD)")
    data_retorno: date = Field(..., description="Data de retorno (YYYY-MM-DD)")
    cidade_origem: Optional[str] = Field(
        default=None, description="Cidade de origem (opcional)"
    )
    quantidade_viajantes: int = Field(
        default=1, ge=1, description="Número de viajantes"
    )
    preferencia_voo: str = Field(default="melhor_custo_beneficio")
    preferencia_hotel: str = Field(default="melhor_custo_beneficio")
    categoria_hotel: Optional[str] = Field(default=None)
    ritmo_roteiro: str = Field(default="moderado")
    interesses: List[str] = Field(default_factory=list)

