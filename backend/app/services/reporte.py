from sqlalchemy.orm import Session

from app.agents.orchestrator import OrchestratorAgent
from app.agents.vision import VisionAgent
from app.core.logging.logger import logger
from app.db.repository.clasificacion_ia import ClasificacionIARepository
from app.db.repository.reporte import ReporteRepository
from app.db.repository.usuario import UsuarioRepository
from app.schemas.clasificacion_ia.internal import ClasificacionIAInternal
from app.schemas.enums import EstadoReporte, Severidad
from app.schemas.reporte.create import ReporteCreate
from app.schemas.reporte.internal import ReporteInternal
from app.schemas.reporte.public import ReportePublic
from app.schemas.usuario.internal import UsuarioInternal


class ReporteService:
    def __init__(self, db: Session):
        self.reporte_repo = ReporteRepository(db)
        self.ia_repo = ClasificacionIARepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.vision_agent = VisionAgent()
        self.orchestrator_agent = OrchestratorAgent()

    async def crear_reporte(self, payload: ReporteCreate) -> ReportePublic:
        usuario_id = payload.usuario_id
        
        # Si usuario_id es string vacío, tratarlo como None
        if usuario_id == "":
            usuario_id = None
        
        if not usuario_id and payload.usuario_telefono:
            user = self.usuario_repo.get_by_telefono(payload.usuario_telefono)
            if not user:
                nuevo_user = UsuarioInternal(
                    nombre=payload.usuario_nombre or "Ciudadano Anónimo",
                    telefono=payload.usuario_telefono,
                )
                user = self.usuario_repo.create(nuevo_user.model_dump())
            usuario_id = user.id

        if not usuario_id:
            nuevo_user = UsuarioInternal(
                nombre="Ciudadano Anónimo", telefono="0000000000"
            )
            user = self.usuario_repo.create(nuevo_user.model_dump())
            usuario_id = user.id

        analisis_vision = await self.vision_agent.analyze_image(
            tipo=payload.tipo_emergencia, foto_url=payload.foto_url
        )
        severidad_enum = Severidad(analisis_vision["severidad"])

        reportes_previos = [
            {
                "id": r.id,
                "ubicacion_lat": r.ubicacion_lat,
                "ubicacion_lng": r.ubicacion_lng,
                "tipo_emergencia": r.tipo_emergencia,
                "grupo_incidente_id": r.grupo_incidente_id,
            }
            for r in self.reporte_repo.get_cola_operador()
        ]

        orquestacion = await self.orchestrator_agent.generate_summary_and_grouping(
            tipo=payload.tipo_emergencia,
            severidad=severidad_enum,
            lat=payload.ubicacion_lat,
            lng=payload.ubicacion_lng,
            existentes=reportes_previos,
        )

        internal_reporte = ReporteInternal(
            tipo_emergencia=payload.tipo_emergencia,
            ubicacion_lat=payload.ubicacion_lat,
            ubicacion_lng=payload.ubicacion_lng,
            foto_url=payload.foto_url,
            organismo=payload.organismo,
            usuario_id=usuario_id,
            severidad=severidad_enum,
            estado=EstadoReporte.PENDIENTE,
            resumen_ia=orquestacion["resumen_ia"],
            grupo_incidente_id=orquestacion["grupo_incidente_id"],
        )

        reporte_db = self.reporte_repo.create(internal_reporte.model_dump())

        internal_ia = ClasificacionIAInternal(
            reporte_id=reporte_db.id,
            severidad=severidad_enum,
            confianza=float(analisis_vision["confianza"]),
            justificacion=str(analisis_vision["justificacion"]),
            coincide_tipo=bool(analisis_vision["coincide_tipo"]),
        )
        self.ia_repo.create(internal_ia.model_dump())

        logger.info(
            f"Reporte creado exitosamente ID={reporte_db.id} Severidad={severidad_enum.value}"
        )
        return ReportePublic.model_validate(reporte_db)

    def obtener_historial_usuario(self, usuario_id: str) -> list[ReportePublic]:
        reportes = self.reporte_repo.get_by_usuario(usuario_id)
        return [ReportePublic.model_validate(r) for r in reportes]
