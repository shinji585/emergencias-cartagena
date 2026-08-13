import os

import httpx

from app.core.logging.logger import logger
from app.schemas.enums import Severidad, TipoEmergencia


class OrchestratorAgent:
    def __init__(self, ollama_url: str | None = None, model_name: str | None = None):
        self.ollama_url = ollama_url or os.getenv(
            "OLLAMA_URL", "http://localhost:11434"
        )
        self.model_name = model_name or os.getenv("OLLAMA_TEXT_MODEL", "llama3.2")

    async def generate_summary_and_grouping(
        self,
        tipo: TipoEmergencia,
        severidad: Severidad,
        lat: float,
        lng: float,
        existentes: list[dict],
    ) -> dict[str, str | None]:
        resumen_fallback = (
            f"Reporte de {tipo.value.replace('_', ' ').title()} "
            f"con severidad {severidad.value.upper()} registrado en lat: {lat:.4f}, lng: {lng:.4f}."
        )
        grupo_id = None

        for exp in existentes:
            dist_lat = abs(exp.get("ubicacion_lat", 0.0) - lat)
            dist_lng = abs(exp.get("ubicacion_lng", 0.0) - lng)
            if (
                dist_lat < 0.005
                and dist_lng < 0.005
                and exp.get("tipo_emergencia") == tipo.value
            ):
                grupo_id = exp.get("grupo_incidente_id") or exp.get("id")
                resumen_fallback += f" (Posible duplicado del incidente {grupo_id[:8]})"
                break

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                prompt = (
                    f"Genera un resumen ejecutivo de 1 línea para el operador de emergencias en Cartagena. "
                    f"Tipo: {tipo.value}, Severidad: {severidad.value}, Ubicación: {lat}, {lng}."
                )
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                }
                res = await client.post(f"{self.ollama_url}/api/generate", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    resumen_ollama = data.get("response", "").strip()
                    if resumen_ollama:
                        resumen_fallback = resumen_ollama
        except Exception as exc:
            logger.info(
                f"Ollama text model offline or timeout ({exc}), using deterministic summary"
            )

        return {"resumen_ia": resumen_fallback, "grupo_incidente_id": grupo_id}
