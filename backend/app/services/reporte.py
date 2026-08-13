from sqlalchemy.orm import Session

from app.agents.orchestrator import OrchestratorAgent
from app.agents.routing import RoutingAgent
from app.agents.vision import VisionAgent
from app.core.logging.logger import logger
from app.db.repository.clasificacion_ia import ClasificacionIARepository
from app.db.repository.reporte import ReporteRepository
from app.db.repository.usuario import UsuarioRepository
from app.schemas.clasificacion_ia.internal import ClasificacionIAInternal
from app.schemas.enums import EstadoReporte, Severidad, TipoEmergencia
from app.schemas.reporte.create import ReporteCreate
from app.schemas.reporte.despacho import (
    DespachoResponse,
    OrganismoNotificado,
    PlanCandadoDetalle,
)
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
        self.routing_agent = RoutingAgent()

    async def crear_reporte(self, payload: ReporteCreate) -> ReportePublic:
        """
        Crea un reporte de emergencia e integra análisis multimodal con los 5 casos de uso.
        
        Flujo:
        1. Validar y crear usuario si es necesario
        2. Análisis de visión (imagen)
        3. Análisis de orquestación (resumen, deduplicación, HAZMAT, etc)
        4. Enrutamiento a organismos correspondientes
        5. Persistencia en BD
        """
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

        # === 1. ANÁLISIS DE VISIÓN ===
        logger.info(f"📸 Analizando imagen para emergencia: {payload.tipo_emergencia.value}")
        analisis_vision = await self.vision_agent.analyze_image(
            tipo=payload.tipo_emergencia, 
            foto_url=payload.foto_url,
            descripcion=payload.descripcion or ""
        )
        severidad_enum = Severidad(analisis_vision["severidad"])

        # === 2. ANÁLISIS DE ORQUESTACIÓN (CASOS DE USO) ===
        logger.info("🧠 Orquestando reporte - Buscando duplicados y aplicando lógica de casos de uso")
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
            descripcion=payload.descripcion or ""
        )

        # Detectar características especiales de casos de uso
        descripcion_lower = (payload.descripcion or "").lower()
        is_hazmat = self.orchestrator_agent._detect_hazmat_risk(descripcion_lower)
        is_disaster = self.orchestrator_agent._detect_disaster_natural(descripcion_lower)
        is_insular = self.orchestrator_agent._is_location_insular(
            payload.ubicacion_lat, payload.ubicacion_lng
        )

        # === 3. ENRUTAMIENTO A ORGANISMOS ===
        logger.info("🚨 Enrutando emergencia a organismos correspondientes")
        organismos_destino = self.routing_agent.route_by_type(
            tipo=payload.tipo_emergencia,
            severidad=severidad_enum,
            is_hazmat=is_hazmat,
            is_insular=is_insular,
            is_disaster=is_disaster
        )

        # === 4. PERSISTENCIA EN BD ===
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
            f"✅ Reporte creado: ID={reporte_db.id} | "
            f"Severidad={severidad_enum.value} | "
            f"HAZMAT={is_hazmat} | Insular={is_insular} | "
            f"Organismos={len(organismos_destino)}"
        )

        # Log de organismos a notificar (en producción, enviar aquí)
        for org in organismos_destino:
            if org:
                logger.info(f"  📢 → {org.nombre} ({org.telefono})")

        return ReportePublic.model_validate(reporte_db)

    def obtener_reporte_por_id(self, reporte_id: str) -> ReportePublic | None:
        reporte = self.reporte_repo.get_by_id(reporte_id)
        if not reporte:
            return None
        return ReportePublic.model_validate(reporte)

    def generar_despacho(
        self, reporte_id: str, actualizar_estado: bool = False
    ) -> DespachoResponse | None:
        reporte = self.reporte_repo.get_by_id(reporte_id)
        if not reporte:
            return None

        # Detectar condiciones especiales
        descripcion_lower = (reporte.descripcion or "").lower()
        is_hazmat = self.orchestrator_agent._detect_hazmat_risk(descripcion_lower)
        is_disaster = self.orchestrator_agent._detect_disaster_natural(descripcion_lower)
        is_insular = self.orchestrator_agent._is_location_insular(
            reporte.ubicacion_lat, reporte.ubicacion_lng
        )

        # Enrutar organismos
        organismos_raw = self.routing_agent.route_by_type(
            tipo=reporte.tipo_emergencia,
            severidad=reporte.severidad,
            is_hazmat=is_hazmat,
            is_insular=is_insular,
            is_disaster=is_disaster,
        )

        organismos_notificados = [
            OrganismoNotificado(
                nombre=org.nombre,
                tipo=org.tipo,
                telefono=org.telefono,
                email=org.email,
                api_endpoint=org.api_endpoint,
                accion=f"Despachar unidad de {org.nombre} a coordenadas ({reporte.ubicacion_lat}, {reporte.ubicacion_lng})",
            )
            for org in organismos_raw
            if org is not None
        ]

        # Calcular CAI cercano si es en el casco urbano
        cai_cercano = self.routing_agent.get_cai_by_location(
            reporte.ubicacion_lat, reporte.ubicacion_lng
        )

        # Plan Candado si es robo/inseguridad
        plan_candado = None
        if reporte.tipo_emergencia == TipoEmergencia.ROBO_INSEGURIDAD:
            radio = self.orchestrator_agent._calculate_escape_radius_km(5)
            plan_candado = PlanCandadoDetalle(
                activo=True,
                radio_huida_km=radio,
                tiempo_transcurrido_minutos=5,
                cai_responsable=cai_cercano,
                recomendacion_tactica=f"Activar cerco policial en radio de {radio:.1f} km desde punto de incidente y cerrar vías perimetrales.",
            )

        if actualizar_estado:
            self.reporte_repo.update(reporte, {"estado": EstadoReporte.EN_ATENCION})

        return DespachoResponse(
            reporte_id=reporte.id,
            tipo_emergencia=reporte.tipo_emergencia,
            severidad=reporte.severidad,
            resumen_ia=reporte.resumen_ia,
            cai_cercano=cai_cercano,
            organismos_notificados=organismos_notificados,
            plan_candado=plan_candado,
            estado_despacho="notificado_exitosamente" if actualizar_estado else "calculado",
            mensaje=f"Alerta generada y canalizada a {len(organismos_notificados)} organismos competentes.",
        )

    def obtener_historial_usuario(self, usuario_id: str) -> list[ReportePublic]:
        reportes = self.reporte_repo.get_by_usuario(usuario_id)
        return [ReportePublic.model_validate(r) for r in reportes]
