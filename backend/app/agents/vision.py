import json
import os

import httpx

from app.core.logging.logger import logger
from app.schemas.enums import Severidad, TipoEmergencia


class VisionAgent:
    """
    Agente de visión multimodal para análisis de imágenes en emergencias.
    Utiliza Gemma3:4b para análisis de imágenes.
    """

    def __init__(self, ollama_url: str | None = None, model_name: str | None = None):
        self.ollama_url = ollama_url or os.getenv(
            "OLLAMA_URL", "http://localhost:11434"
        )
        self.model_name = model_name or os.getenv("OLLAMA_VISION_MODEL", "gemma3:4b")

    async def analyze_image(
        self, tipo: TipoEmergencia, foto_url: str | None, descripcion: str = ""
    ) -> dict[str, str | float | bool]:
        """
        Analiza imagen de emergencia y retorna severidad, confianza y justificación.
        Fallback a análisis basado en reglas si la imagen no está disponible.
        """
        if not foto_url:
            logger.info("No photo provided, using rule-based analysis for type")
            return self._rule_based_analysis(tipo, descripcion)

        try:
            return await self._llm_image_analysis(tipo, foto_url, descripcion)
        except Exception as exc:
            logger.warning(f"LLM image analysis failed ({exc}), using rule-based fallback")
            return self._rule_based_analysis(tipo, descripcion)

    async def _llm_image_analysis(
        self, tipo: TipoEmergencia, foto_url: str, descripcion: str
    ) -> dict[str, str | float | bool]:
        """Análisis de imagen con modelo local Gemma3"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                prompt = (
                    f"Eres un experto en análisis de emergencias. "
                    f"Analiza esta imagen de una emergencia de tipo '{tipo.value.replace('_', ' ')}'.\n"
                    f"Contexto: {descripcion[:100] if descripcion else 'Sin descripción adicional'}\n"
                    f"Responde SOLO en JSON con estas llaves:\n"
                    f'{{"severidad": "leve|moderado|grave", "confianza": 0.0-1.0, "justificacion": "...", "coincide_tipo": true|false}}'
                )
                
                # Construir payload para Ollama con manejo de imágenes
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "num_predict": 150,
                    "temperature": 0.2,
                }

                # Si la imagen está en formato data:image o es URL larga, intentar incluirla
                if foto_url and (foto_url.startswith("data:image") or len(foto_url) > 100):
                    payload["images"] = [foto_url]

                response = await client.post(
                    f"{self.ollama_url}/api/generate", json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").strip()

                    # Intentar parsear JSON de la respuesta
                    try:
                        # Buscar JSON en la respuesta
                        json_start = response_text.find("{")
                        json_end = response_text.rfind("}") + 1
                        if json_start >= 0 and json_end > json_start:
                            json_str = response_text[json_start:json_end]
                            result = json.loads(json_str)
                            
                            # Validar campos
                            severidad = result.get("severidad", "moderado").lower()
                            if severidad not in ["leve", "moderado", "grave"]:
                                severidad = "moderado"
                            
                            confianza = float(result.get("confianza", 0.75))
                            confianza = max(0.0, min(1.0, confianza))

                            return {
                                "severidad": severidad,
                                "confianza": confianza,
                                "justificacion": str(result.get("justificacion", "Análisis de imagen completado")),
                                "coincide_tipo": bool(result.get("coincide_tipo", True)),
                            }
                    except json.JSONDecodeError:
                        logger.debug("Could not parse JSON from LLM response, using fallback")

        except Exception as exc:
            logger.warning(f"Image analysis timeout/error ({exc})")

        return self._rule_based_analysis(tipo, descripcion)

    def _rule_based_analysis(
        self, tipo: TipoEmergencia, descripcion: str = ""
    ) -> dict[str, str | float | bool]:
        """
        Análisis determinista basado en reglas cuando no hay imagen o LLM falla.
        Mapea severidad por tipo de emergencia.
        """
        severidad_map = {
            TipoEmergencia.ACCIDENTE: Severidad.GRAVE,
            TipoEmergencia.EMERGENCIA_MEDICA: Severidad.GRAVE,
            TipoEmergencia.EMERGENCIA_INDUSTRIAL: Severidad.GRAVE,
            TipoEmergencia.ROBO_INSEGURIDAD: Severidad.MODERADO,
            TipoEmergencia.INCIDENTE_TRANSITO: Severidad.LEVE,
        }

        # Ajuste por palabras clave en descripción
        lower_desc = (descripcion or "").lower()
        sev = severidad_map.get(tipo, Severidad.MODERADO)

        if any(w in lower_desc for w in ["grave", "crítico", "urgente", "muerto", "fallecido"]):
            sev = Severidad.GRAVE
        elif any(w in lower_desc for w in ["leve", "menor", "pequeño", "raspón"]):
            sev = Severidad.LEVE

        return {
            "severidad": sev.value,
            "confianza": 0.75,
            "justificacion": f"Análisis regla-basada para {tipo.value}: severidad {sev.value} por defecto de tipo.",
            "coincide_tipo": True,
        }
