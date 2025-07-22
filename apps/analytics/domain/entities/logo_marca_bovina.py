# apps/analytics/domain/entities/logo_marca_bovina.py
"""
Entidad de dominio para logo generado por IA
Representa un logo generado para una marca bovina
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..enums import ModeloIA, CalidadLogo


@dataclass
class LogoMarcaBovina:
    """
    Entidad de dominio para logo generado por IA
    Representa un logo generado para una marca bovina
    """

    marca_id: int
    url_logo: str
    fecha_generacion: datetime
    exito: bool = True
    tiempo_generacion_segundos: int = 0
    modelo_ia_usado: ModeloIA = ModeloIA.DALL_E_3
    prompt_usado: Optional[str] = None
    calidad_logo: CalidadLogo = CalidadLogo.MEDIA

    # ID para persistencia (opcional)
    id: Optional[int] = None

    def __post_init__(self):
        """Validaciones de dominio"""
        if self.tiempo_generacion_segundos < 0:
            raise ValueError("El tiempo de generación no puede ser negativo")

        if not self.url_logo:
            raise ValueError("La URL del logo es requerida")
