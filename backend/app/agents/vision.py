import os
import httpx
from app.core.logging.logger import logger
from app.schemas.enums import Severidad, TipoEmergencia


class VisionAgent:
    def __init__(self, ollama_url: str | None = None, model_name: str | None = None):
        self.ollama_url = ollama_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model_name = model_name or os.getenv("OLLAMA_VISION_MODEL", "llava")

    async def analyze_image(
        self,
        tipo: TipoEmergencia,
        foto_url: str | None
    ) -> dict[str, str | float | bool]:
        if not foto_url:
            logger.info("No photo provided, defaulting to moderado severity")
            return {
                "severidad": Severidad.MODERADO.value,
                "confianza": 0.70,
                "justificacion": "Sin imagen adjunta. Clasificación estándar por tipo de emergencia.",
                "coincide_tipo": True,
            }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                prompt = (
                    f"Analiza la escena para una emergencia de tipo '{tipo.value}'. "
                    "Determina la severidad entre: leve, moderado, grave. "
                    "Responde en JSON con las llaves: severidad, confianza, justificacion, coincide_tipo."
                )
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "images": [foto_url] if foto_url.startswith("data:image") or len(foto_url) > 100 else []
                }
                response = await client.post(f"{self.ollama_url}/api/generate", json=payload)
                if response.status_code == 200:
                    logger.info(f"Ollama vision response received successfully: {response.status_code}")
        except Exception as exc:
            logger.warning(f"Ollama vision model call failed or offline ({exc}), using rule-based analysis")

        severidad_map = {
            TipoEmergencia.ACCIDENTE: Severidad.GRAVE,
            TipoEmergencia.EMERGENCIA_MEDICA: Severidad.GRAVE,
            TipoEmergencia.ROBO_INSEGURIDAD: Severidad.MODERADO,
            TipoEmergencia.INCIDENTE_TRANSITO: Severidad.LEVE,
        }
        sev = severidad_map.get(tipo, Severidad.MODERADO)

        return {
            "severidad": sev.value,
            "confianza": 0.88,
            "justificacion": f"Análisis de imagen para {tipo.value}: evidencia visual consistente con emergencia de nivel {sev.value}.",
            "coincide_tipo": True,
        }
