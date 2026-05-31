from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TravelPreferences(BaseModel):
    quantidade_viajantes: int = Field(default=1, description="Número de passageiros")
    quantidade_hospedes: int = Field(default=1, description="Número de hóspedes")
    quantidade_quartos: int = Field(default=1, description="Número de quartos")
    preferencia_voo: str = Field(default="melhor_custo_beneficio", description="Preferência de voo (ex: menor_preco, menor_duracao, melhor_custo_beneficio)")
    preferencia_hotel: str = Field(default="melhor_custo_beneficio", description="Preferência de hotel")
    categoria_hotel: Optional[str] = Field(default=None, description="Categoria do hotel (ex: 3 estrelas, 4 estrelas)")
    ritmo_roteiro: str = Field(default="moderado", description="Ritmo do roteiro (ex: leve, moderado, intenso)")
    interesses: List[str] = Field(default_factory=list, description="Lista de interesses (ex: historia, gastronomia, museus)")

class TravelRequest(BaseModel):
    cidade_destino: str = Field(..., description="Cidade de destino da viagem")
    data_saida: date = Field(..., description="Data de início da viagem (check-in)")
    data_retorno: date = Field(..., description="Data de retorno (check-out)")
    cidade_origem: Optional[str] = Field(default=None, description="Cidade de origem da viagem")
    preferencias: TravelPreferences = Field(default_factory=TravelPreferences, description="Preferências da viagem")

class ExecutionMetadata(BaseModel):
    idioma: str = Field(default="pt-BR")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class TravelContext(BaseModel):
    request_id: str
    cidade_destino: str
    data_saida: date
    data_retorno: date
    cidade_origem: Optional[str] = None
    quantidade_dias: int
    quantidade_noites: int
    preferencias: TravelPreferences
    execucao: ExecutionMetadata

class FlightOption(BaseModel):
    companhia: str
    origem: str
    destino: str
    data_ida: date
    data_volta: date
    preco_estimado: Optional[float] = None
    moeda: Optional[str] = "BRL"
    duracao_estimada: Optional[str] = None
    escalas: Optional[int] = 0
    link_consulta: Optional[str] = None
    observacoes: Optional[str] = "Preço e disponibilidade devem ser confirmados."
    score: Optional[float] = Field(default=0.0, description="Score calculado para ranking")

class HotelOption(BaseModel):
    nome: str
    bairro: Optional[str] = None
    categoria: Optional[str] = None
    preco_estimado_total: Optional[float] = None
    preco_estimado_diaria: Optional[float] = None
    moeda: Optional[str] = "BRL"
    avaliacao: Optional[str] = None
    destaques: List[str] = Field(default_factory=list)
    link_consulta: Optional[str] = None
    observacoes: Optional[str] = "Tarifa e disponibilidade devem ser confirmadas."
    score: Optional[float] = Field(default=0.0, description="Score calculado para ranking")

class TouristAttraction(BaseModel):
    nome: str
    categoria: str
    bairro: Optional[str] = None
    tempo_estimado_visita: Optional[str] = None
    prioridade: int
    observacoes: List[str] = Field(default_factory=list)
    score: Optional[float] = Field(default=0.0, description="Score calculado para ranking")

class DailyItinerary(BaseModel):
    dia: int
    data: date
    tema: str
    manha: List[str] = Field(default_factory=list)
    tarde: List[str] = Field(default_factory=list)
    noite: List[str] = Field(default_factory=list)
    observacoes: List[str] = Field(default_factory=list)

class AgentResult(BaseModel):
    agent_name: str
    status: str  # sucesso, parcial, erro
    data: Any
    fontes: List[str] = Field(default_factory=list)
    alertas: List[str] = Field(default_factory=list)
    erros: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class CostEstimation(BaseModel):
    passagens: Optional[float] = None
    hospedagem: Optional[float] = None
    passeios: Optional[float] = None
    total_estimado: Optional[float] = None
    moeda: str = "BRL"

class IntegratedPlan(BaseModel):
    estimativa_custos: CostEstimation
    recomendacao_geral: str

class TravelPlan(BaseModel):
    request_id: str
    status: str  # sucesso, parcial, erro
    resumo: Dict[str, Any]
    resultado: Dict[str, AgentResult]
    plano_integrado: IntegratedPlan
    alertas: List[str] = Field(default_factory=list)
    fontes: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
