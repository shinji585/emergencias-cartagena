from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.repository.reporte import ReporteRepository
from app.schemas.reporte.public import ReportePublic
from app.schemas.enums import EstadoReporte, Severidad
from app.core.logging.logger import logger


class OperadorService:
    def __init__(self, db: Session):
        self.reporte_repo = ReporteRepository(db)

    def obtener_cola_priorizada(self) -> list[dict]:
        reportes_db = self.reporte_repo.get_cola_operador()
        ahora = datetime.now(timezone.utc)
        lista_priorizada = []

        severidad_pesos = {
            Severidad.GRAVE.value: 300,
            Severidad.MODERADO.value: 200,
            Severidad.LEVE.value: 100
        }

        for rep in reportes_db:
            created_at = rep.created_at
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)
            minutos_espera = max(0.0, (ahora - created_at).total_seconds() / 60.0)
            
            peso_base = severidad_pesos.get(rep.severidad, 100)
            score_prioridad = peso_base + (minutos_espera * 5.0)

            pub = ReportePublic.model_validate(rep).model_dump()
            pub["minutos_espera"] = round(minutos_espera, 1)
            pub["score_prioridad"] = round(score_prioridad, 1)
            lista_priorizada.append(pub)

        lista_priorizada.sort(key=lambda x: x["score_prioridad"], reverse=True)
        return lista_priorizada

    def actualizar_estado(self, reporte_id: str, nuevo_estado: EstadoReporte) -> ReportePublic | None:
        reporte = self.reporte_repo.get_by_id(reporte_id)
        if not reporte:
            return None

        actualizado = self.reporte_repo.update(reporte, {"estado": nuevo_estado.value})
        logger.info(f"Reporte {reporte_id} actualizado a estado {nuevo_estado.value}")
        return ReportePublic.model_validate(actualizado)

    def obtener_metricas(self) -> dict:
        todos = self.reporte_repo.get_all(limit=1000)
        totales = len(todos)
        por_estado = {e.value: 0 for e in EstadoReporte}
        por_organismo = {}

        for r in todos:
            por_estado[r.estado] = por_estado.get(r.estado, 0) + 1
            por_organismo[r.organismo] = por_organismo.get(r.organismo, 0) + 1

        return {
            "total_reportes": totales,
            "por_estado": por_estado,
            "por_organismo": por_organismo,
        }
