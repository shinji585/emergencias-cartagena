from enum import Enum


class TipoEmergencia(str, Enum):
    ACCIDENTE = "accidente"
    ROBO_INSEGURIDAD = "robo_inseguridad"
    EMERGENCIA_MEDICA = "emergencia_medica"
    INCIDENTE_TRANSITO = "incidente_transito"


class Severidad(str, Enum):
    LEVE = "leve"
    MODERADO = "moderado"
    GRAVE = "grave"


class EstadoReporte(str, Enum):
    PENDIENTE = "pendiente"
    EN_ATENCION = "en_atencion"
    RESUELTO = "resuelto"
    DESCARTADO = "descartado"


class Organismo(str, Enum):
    POLICIA = "policia"
    TRANSITO = "transito"
    AMBULANCIA = "ambulancia"
