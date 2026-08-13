"""
Agente de enrutamiento inteligente para mapear emergencias a organismos.
Implementa la lógica de despacho para los 5 casos de uso del sistema.
"""
from dataclasses import dataclass

from app.core.logging.logger import logger
from app.schemas.enums import Severidad, TipoEmergencia


@dataclass
class OrganismoContacto:
    """Datos de contacto de un organismo de emergencia"""
    nombre: str
    tipo: str
    telefono: str
    email: str | None = None
    api_endpoint: str | None = None
    zona_cobertura: str | None = None


class RoutingAgent:
    """
    Agente que mapea emergencias a organismos correspondientes.
    Gestiona directorios de contactos y lógica de enrutamiento por caso de uso.
    """

    # CASO 1: Accidentes de Tránsito
    ORGANISMOS_TRAFICO = {
        "CRUE": OrganismoContacto(
            nombre="Centro Regulador de Urgencias y Emergencias",
            tipo="coordinacion_medica",
            telefono="(+57 5) 6600 123",
            email="crue@cartagena.gov.co",
            zona_cobertura="Cartagena y zona metropolitana"
        ),
        "DATT": OrganismoContacto(
            nombre="Dirección de Tránsito de Cartagena",
            tipo="gestion_trafico",
            telefono="(+57 5) 6690 500",
            email="datt@cartagena.gov.co",
            zona_cobertura="Vías principales"
        ),
        "Ambulancia": OrganismoContacto(
            nombre="Servicio de Ambulancias Medicalizadas",
            tipo="ambulancia",
            telefono="123",
            zona_cobertura="Cartagena"
        ),
    }

    # CASO 2: Desastres Naturales
    ORGANISMOS_DESASTRES = {
        "Bomberos": OrganismoContacto(
            nombre="Cuerpo Oficial de Bomberos de Cartagena",
            tipo="rescate",
            telefono="119",
            email="bomberos@cartagena.gov.co",
            zona_cobertura="Cartagena"
        ),
        "OAGRD": OrganismoContacto(
            nombre="Oficina Asesora para la Gestión del Riesgo de Desastres",
            tipo="gestion_riesgo",
            telefono="(+57 5) 6600 500",
            email="oagrd@cartagena.gov.co",
            zona_cobertura="Cartagena"
        ),
        "Defensa Civil": OrganismoContacto(
            nombre="Defensa Civil de Cartagena",
            tipo="defensa_civil",
            telefono="122",
            zona_cobertura="Cartagena"
        ),
    }

    # CASO 3: Emergencias Industriales (HAZMAT)
    ORGANISMOS_HAZMAT = {
        "Bomberos_HAZMAT": OrganismoContacto(
            nombre="Brigada HAZMAT - Bomberos Cartagena",
            tipo="hazmat",
            telefono="119",
            email="hazmat@bomberos.cartagena.gov.co",
            zona_cobertura="Mamonal, Zona Industrial"
        ),
        "OAGRD_HAZMAT": OrganismoContacto(
            nombre="OAGRD - Respuesta Química",
            tipo="hazmat_coordinacion",
            telefono="(+57 5) 6600 500",
            zona_cobertura="Cartagena"
        ),
    }

    # CASO 4: Emergencias Turísticas Insulares
    ORGANISMOS_INSULARES = {
        "Guardia_Costera": OrganismoContacto(
            nombre="Guardia Costera - Armada Nacional de Colombia",
            tipo="rescate_maritimo",
            telefono="(+57 5) 6656 800",
            email="guardiacostera@armada.mil.co",
            api_endpoint="https://api.guardiacostera.mil.co/emergencias",
            zona_cobertura="Islas del Rosario, Barú, aguas territoriales"
        ),
        "CRUE": OrganismoContacto(
            nombre="CRUE - Coordinación en tierra",
            tipo="coordinacion_medica",
            telefono="(+57 5) 6600 123",
            zona_cobertura="Muelle de desembarque"
        ),
    }

    # CASO 5: Robos e Inseguridad
    ORGANISMOS_POLICIA = {
        "CAI": OrganismoContacto(
            nombre="Centro de Atención Inmediata - Policía Nacional",
            tipo="policia_local",
            telefono="112 / (Varía por zona)",
            zona_cobertura="Por cuadrante"
        ),
        "PLAN_CANDADO": OrganismoContacto(
            nombre="Central de Coordinación - Plan Candado",
            tipo="coordinacion_policial",
            telefono="(+57 5) 6600 999",
            api_endpoint="https://api.policia.cartagena.gov.co/candado",
            zona_cobertura="Cartagena"
        ),
    }

    def __init__(self):
        self.directorios = {
            TipoEmergencia.ACCIDENTE: self.ORGANISMOS_TRAFICO,
            TipoEmergencia.INCIDENTE_TRANSITO: self.ORGANISMOS_TRAFICO,
            TipoEmergencia.EMERGENCIA_MEDICA: self.ORGANISMOS_DESASTRES,
            TipoEmergencia.EMERGENCIA_INDUSTRIAL: self.ORGANISMOS_HAZMAT,
            TipoEmergencia.ROBO_INSEGURIDAD: self.ORGANISMOS_POLICIA,
        }

    def route_by_type(
        self,
        tipo: TipoEmergencia,
        severidad: Severidad,
        is_hazmat: bool = False,
        is_insular: bool = False,
        is_disaster: bool = False,
    ) -> list[OrganismoContacto]:
        """
        Retorna lista de organismos a notificar en orden de prioridad.
        Implementa lógica de routing para los 5 casos de uso.
        """
        organismos = []

        # HAZMAT: Máxima prioridad
        if is_hazmat:
            logger.info("🚨 HAZMAT routing: activando brigadas especiales")
            return [
                self.ORGANISMOS_HAZMAT.get("Bomberos_HAZMAT"),
                self.ORGANISMOS_HAZMAT.get("OAGRD_HAZMAT"),
            ]

        # Zona insular: Guardia Costera primaria
        if is_insular:
            logger.info("🏝️ Insular routing: Guardia Costera")
            return [
                self.ORGANISMOS_INSULARES.get("Guardia_Costera"),
                self.ORGANISMOS_INSULARES.get("CRUE"),
            ]

        # Desastres naturales: Bomberos + Defensa Civil
        if is_disaster:
            logger.info("🌊 Disaster routing: Bomberos + OAGRD")
            return [
                self.ORGANISMOS_DESASTRES.get("Bomberos"),
                self.ORGANISMOS_DESASTRES.get("OAGRD"),
                self.ORGANISMOS_DESASTRES.get("Defensa Civil"),
            ]

        # Enrutamiento por tipo genérico
        directorio = self.directorios.get(tipo, {})
        for organismo in directorio.values():
            if organismo:
                organismos.append(organismo)

        return organismos

    def get_cai_by_location(self, lat: float, lng: float) -> str | None:
        """
        Mapea coordenadas a CAI más cercano (simulado).
        En producción, usar base de datos geoespacial.
        """
        # Aproximación: dividir Cartagena en cuadrantes
        # Centro histórico: ~10.3815°N, 75.5097°W
        
        if 10.35 <= lat <= 10.42 and -75.52 <= lng <= -75.46:
            return "CAI Centro Histórico"
        elif 10.38 <= lat <= 10.45 and -75.46 <= lng <= -75.40:
            return "CAI Bocagrande"
        elif 10.25 <= lat <= 10.35 and -75.55 <= lng <= -75.45:
            return "CAI Castillogrande"
        elif 10.30 <= lat <= 10.38 and -75.60 <= lng <= -75.52:
            return "CAI Getsemaní"
        else:
            return "CAI Zona Periférica"

    def format_alert_for_organismo(
        self,
        organismo: OrganismoContacto,
        tipo: TipoEmergencia,
        severidad: Severidad,
        lat: float,
        lng: float,
        resumen: str,
    ) -> dict:
        """
        Formatea alerta según el formato esperado por cada organismo.
        En producción, adaptar según APIs específicas.
        """
        return {
            "organismo": organismo.nombre,
            "tipo_organismo": organismo.tipo,
            "telefono": organismo.telefono,
            "email": organismo.email,
            "timestamp": None,  # Será establecido en el router
            "emergencia": {
                "tipo": tipo.value,
                "severidad": severidad.value,
                "ubicacion": {"lat": lat, "lng": lng},
                "resumen": resumen,
            },
            "accion": f"Notificar a {organismo.nombre}",
        }
