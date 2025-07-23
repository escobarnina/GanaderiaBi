# apps/analytics/domain/enums.py
"""
Enumeraciones del dominio de Inteligencia de Negocios
Define los valores válidos para los campos del dominio
"""

from enum import Enum


class EstadoMarca(Enum):
    """Estados posibles de una marca de ganado bovino"""

    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"

    @classmethod
    def choices(cls):
        """Retorna las opciones para Django forms"""
        return [(member.value, member.value) for member in cls]


class RazaBovino(Enum):
    """Razas de ganado bovino"""

    CRIOLLO = "CRIOLLO"
    NELORE = "NELORE"
    BRAHMAN = "BRAHMAN"
    SANTA_GERTRUDIS = "SANTA_GERTRUDIS"
    CHAROLAIS = "CHAROLAIS"
    HOLSTEIN = "HOLSTEIN"
    SIMMENTAL = "SIMMENTAL"
    ANGUS = "ANGUS"
    HEREFORD = "HEREFORD"
    GUZERAT = "GUZERAT"
    MIXTO = "MIXTO"
    OTRO = "OTRO"

    @classmethod
    def choices(cls):
        """Retorna las opciones para Django forms"""
        return [(member.value, member.value) for member in cls]


class PropositoGanado(Enum):
    """Propósitos del ganado bovino"""

    CARNE = "CARNE"
    LECHE = "LECHE"
    DOBLE_PROPOSITO = "DOBLE_PROPOSITO"
    REPRODUCCION = "REPRODUCCION"

    @classmethod
    def choices(cls):
        """Retorna las opciones para Django forms"""
        return [(member.value, member.value) for member in cls]


class Departamento(Enum):
    """Departamentos de Bolivia"""

    LA_PAZ = "LA_PAZ"
    SANTA_CRUZ = "SANTA_CRUZ"
    COCHABAMBA = "COCHABAMBA"
    POTOSI = "POTOSI"
    ORURO = "ORURO"
    CHUQUISACA = "CHUQUISACA"
    TARIJA = "TARIJA"
    BENI = "BENI"
    PANDO = "PANDO"

    @classmethod
    def choices(cls):
        """Retorna las opciones para Django forms"""
        return [(member.value, member.value) for member in cls]


class ModeloIA(Enum):
    """Modelos de IA para generación de logos"""

    GPT_4 = "GPT-4"
    DALL_E_3 = "DALL-E-3"
    DALL_E_2 = "DALL-E-2"
    MIDJOURNEY = "MIDJOURNEY"
    STABLE_DIFFUSION = "STABLE_DIFFUSION"
    LEONARDO_AI = "LEONARDO_AI"

    @classmethod
    def choices(cls):
        """Retorna las opciones para Django forms"""
        return [(member.value, member.value) for member in cls]


class CalidadLogo(Enum):
    """Calidades de logos generados"""

    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

    @classmethod
    def choices(cls):
        """Retorna las opciones para Django forms"""
        return [(member.value, member.value) for member in cls]
