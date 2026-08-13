from pydantic import BaseModel, Field
from app.schemas.enums import Severidad, TipoEmergencia


class OrganismoNotificado(BaseModel):
    nombre: str = Field(..., description="Nombre del organismo")
    tipo: str = Field(..., description="Tipo de organismo (coordinacion_medica, policia_local, etc.)")
    telefono: str = Field(..., description="Teléfono de contacto")
    email: str | None = Field(default=None, description="Email institucional")
    accion: str = Field(..., description="Instrucción de despliegue generada por el agente")
    api_endpoint: str | None = Field(default=None, description="Endpoint de integración de despacho")


class PlanCandadoDetalle(BaseModel):
    activo: bool = Field(..., description="Indica si se activó el Plan Candado")
    radio_huida_km: float = Field(..., description="Radio de escape estimado en km")
    tiempo_transcurrido_minutos: int = Field(default=5, description="Minutos transcurridos")
    cai_responsable: str | None = Field(default=None, description="CAI asignado para el cierre")
    recomendacion_tactica: str = Field(..., description="Instrucción táctica de cerco policial")


class DespachoResponse(BaseModel):
    reporte_id: str = Field(..., description="ID del reporte de emergencia")
    tipo_emergencia: TipoEmergencia = Field(..., description="Tipo de emergencia")
    severidad: Severidad = Field(..., description="Severidad evaluada")
    resumen_ia: str | None = Field(default=None, description="Resumen analítico generado por la IA")
    cai_cercano: str | None = Field(default=None, description="CAI o estación policial más cercana")
    organismos_notificados: list[OrganismoNotificado] = Field(
        default_factory=list, description="Lista de organismos y unidades notificadas"
    )
    plan_candado: PlanCandadoDetalle | None = Field(
        default=None, description="Detalles del Plan Candado si es robo/inseguridad"
    )
    estado_despacho: str = Field(default="despachado", description="Estado de la alerta")
    mensaje: str = Field(..., description="Confirmación operativa del agente")
