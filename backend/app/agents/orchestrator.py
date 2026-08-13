import os
import unicodedata

import httpx

from app.core.logging.logger import logger
from app.schemas.enums import Severidad, TipoEmergencia


def _normalize_text(text: str) -> str:
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


class OrchestratorAgent:
    """
    Agente orquestador multimodal para análisis inteligente de emergencias.
    Implementa los 5 casos de uso del sistema de Cartagena:
    1. Accidentes de tránsito
    2. Desastres naturales/inundaciones
    3. Emergencias industriales (HAZMAT)
    4. Emergencias turísticas multilingües
    5. Robos e inseguridad ciudadana
    """

    # Palabras clave críticas normalizadas para cada caso de uso
    HAZMAT_KEYWORDS = {
        "quimic", "gas", "incendio", "fuego industrial", "toxic", "reactiv",
        "explosion", "derrame", "contaminacion", "vapor toxic", "sustancia peligrosa"
    }
    
    DISASTER_KEYWORDS = {
        "inundac", "inundad", "desbord", "lluvia", "anegad", "sumergid",
        "cano", "arroyo", "rio", "aluvion", "deslizamiento"
    }
    
    TRAFFIC_KEYWORDS = {
        "accidente", "choque", "colision", "vuelco", "derrapada", "transito",
        "carro", "coche", "moto", "auto"
    }

    # Mapeo de organismos por tipo de emergencia
    ORGANISMOS_PRIMARIOS = {
        TipoEmergencia.ACCIDENTE: ["CRUE", "Bomberos", "Policía"],
        TipoEmergencia.EMERGENCIA_MEDICA: ["CRUE", "Hospital", "Ambulancia"],
        TipoEmergencia.INCIDENTE_TRANSITO: ["DATT", "Policía", "CRUE"],
        TipoEmergencia.ROBO_INSEGURIDAD: ["CAI", "Policía", "Cuadrante"],
        TipoEmergencia.EMERGENCIA_INDUSTRIAL: ["Bomberos", "HAZMAT", "OAGRD"],
    }

    def __init__(self, ollama_url: str | None = None, model_name: str | None = None):
        self.ollama_url = ollama_url or os.getenv(
            "OLLAMA_URL", "http://localhost:11434"
        )
        self.model_name = model_name or os.getenv("OLLAMA_TEXT_MODEL", "llama3.2:3b")

    async def _call_llm(
        self, prompt: str, max_tokens: int = 256, temperature: float = 0.3
    ) -> str:
        """Llamada genérica al modelo Ollama local"""
        try:
            logger.info(f"🔗 Conectando a Ollama: {self.ollama_url}/api/generate (modelo: {self.model_name})")
            async with httpx.AsyncClient(timeout=300.0) as client:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "num_predict": max_tokens,
                    "temperature": temperature,
                }
                res = await client.post(f"{self.ollama_url}/api/generate", json=payload)
                logger.info(f"📡 Ollama respondió con status {res.status_code}")
                if res.status_code == 200:
                    data = res.json()
                    response_text = data.get("response", "").strip()
                    logger.info(f"✅ LLM response: {response_text[:100]}")
                    return response_text
                else:
                    logger.error(f"❌ Ollama error: {res.status_code} - {res.text}")
        except Exception as exc:
            logger.error(f"❌ LLM call failed: {type(exc).__name__}: {exc}")
        return ""

    def _detect_hazmat_risk(self, descripcion: str) -> bool:
        """Detecta si el reporte contiene riesgos HAZMAT"""
        norm_desc = _normalize_text(descripcion)
        return any(keyword in norm_desc for keyword in self.HAZMAT_KEYWORDS)

    def _detect_disaster_natural(self, descripcion: str) -> bool:
        """Detecta si es un desastre natural/inundación"""
        norm_desc = _normalize_text(descripcion)
        return any(keyword in norm_desc for keyword in self.DISASTER_KEYWORDS)

    def _is_location_insular(self, lat: float, lng: float) -> bool:
        """
        Detecta si la ubicación es en zona insular.
        Islas del Rosario: ~10.15°N, ~76.15°W
        Barú: ~10.17°N, ~75.78°W
        Tierra Bomba: ~10.18°N, ~75.85°W
        """
        return (10.0 <= lat <= 10.28) and (-76.5 <= lng <= -75.55)

    def _calculate_escape_radius_km(self, minutes_elapsed: int) -> float:
        """
        Calcula el radio de huida en km según el tiempo transcurrido.
        Basado en Plan Candado: velocidad promedio ~30 km/h en zonas urbanas
        """
        return (minutes_elapsed * 30.0) / 60.0

    async def generate_summary_and_grouping(
        self,
        tipo: TipoEmergencia,
        severidad: Severidad,
        lat: float,
        lng: float,
        existentes: list[dict],
        descripcion: str = "",
    ) -> dict[str, str | None]:
        """
        Genera resumen ejecutivo y detecta duplicados con lógica de casos de uso.
        Implementa deduplicación inteligente y enrutamiento.
        """
        resumen_fallback = (
            f"Reporte de {tipo.value.replace('_', ' ').title()} "
            f"con severidad {severidad.value.upper()} en lat: {lat:.4f}, lng: {lng:.4f}."
        )
        grupo_id = None
        organismo_primario = self.ORGANISMOS_PRIMARIOS.get(tipo, ["Centro de Control"])

        # === CASO 1: Detección de HAZMAT ===
        if self._detect_hazmat_risk(descripcion):
            logger.info("🚨 HAZMAT detectado - Elevando a CRÍTICA")
            severidad = Severidad.GRAVE
            organismo_primario = ["Bomberos HAZMAT", "OAGRD", "Brigadas Mamonal"]
            resumen_fallback += " ⚠️ RIESGO HAZMAT DETECTADO - MÁXIMA PRIORIDAD"

        # === CASO 2: Deduplicación espacial-temporal (Desastres) ===
        if self._detect_disaster_natural(descripcion):
            logger.info("🌊 Desastre natural detectado - Buscando duplicados en zona")
            # Radio de deduplicación mayor para desastres (afecta área más grande)
            radius_lat = 0.01  # ~1.1 km
            radius_lng = 0.01
            duplicados_count = 0

            for exp in existentes:
                dist_lat = abs(exp.get("ubicacion_lat", 0.0) - lat)
                dist_lng = abs(exp.get("ubicacion_lng", 0.0) - lng)
                if (
                    dist_lat < radius_lat
                    and dist_lng < radius_lng
                    and exp.get("tipo_emergencia") == tipo.value
                ):
                    if not grupo_id:
                        grupo_id = exp.get("grupo_incidente_id") or exp.get("id")
                    duplicados_count += 1

            if duplicados_count > 0:
                resumen_fallback = (
                    f"Incidente sectorial: {duplicados_count + 1} reportes en la misma zona. "
                    f"Tipo: {tipo.value}. Severidad: {severidad.value}. "
                    f"Enviando maquinaria de rescate coordinada."
                )

        # === CASO 3: Emergencias turísticas insulares (Traducción multilingüe) ===
        if self._is_location_insular(lat, lng):
            logger.info("🏝️ Emergencia insular detectada - Notificando Guardia Costera")
            organismo_primario = ["Guardia Costera", "CRUE", "Emergencias Marítimas"]
            resumen_fallback += " [ZONA INSULAR - Coordinación Marítima Requerida]"

        # === CASO 4: Deduplicación estándar (tránsito, robos) ===
        if not grupo_id:
            radius_lat = 0.005  # ~0.5 km
            radius_lng = 0.005
            for exp in existentes:
                dist_lat = abs(exp.get("ubicacion_lat", 0.0) - lat)
                dist_lng = abs(exp.get("ubicacion_lng", 0.0) - lng)
                if (
                    dist_lat < radius_lat
                    and dist_lng < radius_lng
                    and exp.get("tipo_emergencia") == tipo.value
                ):
                    grupo_id = exp.get("grupo_incidente_id") or exp.get("id")
                    resumen_fallback += f" (Duplicado probable: {grupo_id[:8]})"
                    break

        # Intenta generar resumen con LLM local
        try:
            llm_prompt = (
                f"Genera un resumen breve (1 línea) para operador de emergencias en Cartagena:\n"
                f"Tipo: {tipo.value}\n"
                f"Severidad: {severidad.value}\n"
                f"Organismos: {', '.join(organismo_primario)}\n"
                f"Descripción: {descripcion[:100] if descripcion else 'Sin descripción'}"
            )
            llm_response = await self._call_llm(llm_prompt, max_tokens=50)
            if llm_response and len(llm_response) > 5:
                resumen_fallback = llm_response
        except Exception as exc:
            logger.debug(f"LLM summary generation skipped ({exc})")

        return {
            "resumen_ia": resumen_fallback,
            "grupo_incidente_id": grupo_id,
            "organismos_primarios": organismo_primario,
            "severidad_ajustada": severidad.value,
        }

    async def analyze_robo_plan_candado(
        self, lat: float, lng: float, minutes_elapsed: int = 3
    ) -> dict:
        """
        CASO 5: Calcula Plan Candado para robo/inseguridad.
        Proyecta radio de huida y sugiere cierre de vías.
        """
        escape_radius_km = self._calculate_escape_radius_km(minutes_elapsed)
        
        # Aproximación: 1 grado ~ 111 km
        radius_deg = escape_radius_km / 111.0

        return {
            "punto_incidente": {"lat": lat, "lng": lng},
            "radio_huida_km": escape_radius_km,
            "radio_huida_deg": radius_deg,
            "tiempo_transcurrido_min": minutes_elapsed,
            "accion": f"Activar Plan Candado: cerrar vías en radio de {escape_radius_km:.1f} km",
        }

    async def translate_to_spanish(self, texto: str, idioma_origen: str = "en") -> str:
        """
        CASO 4: Traducción multilingüe para emergencias turísticas.
        Usa LLM local para traducir descripciones de síntomas/emergencias.
        """
        if idioma_origen.lower() == "es":
            return texto

        prompt = (
            f"Traduce al español (respuesta corta):\n"
            f"Idioma: {idioma_origen}\n"
            f"Texto: {texto}"
        )
        traduccion = await self._call_llm(prompt, max_tokens=100)
        return traduccion if traduccion else texto
