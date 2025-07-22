# apps/analytics/domain/entities/kpi_ganado_bovino.py
"""
Entidad de dominio para KPIs del sector ganadero bovino
Representa un snapshot de indicadores clave
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class KPIGanadoBovino:
    """
    Entidad de dominio para KPIs del sector ganadero bovino
    Representa un snapshot de indicadores clave
    """

    fecha: date

    # KPIs principales
    marcas_registradas_mes: int = 0
    tiempo_promedio_procesamiento: float = 0.0
    porcentaje_aprobacion: float = 0.0
    ingresos_mes: Decimal = Decimal("0")

    # KPIs específicos para bovinos
    total_cabezas_registradas: int = 0
    promedio_cabezas_por_marca: float = 0.0

    # Distribución por propósito
    marcas_carne: int = 0
    marcas_leche: int = 0
    marcas_doble_proposito: int = 0
    marcas_reproduccion: int = 0

    # Distribución por departamentos
    marcas_santa_cruz: int = 0
    marcas_beni: int = 0
    marcas_la_paz: int = 0
    marcas_otros_departamentos: int = 0

    # KPIs de logos
    tasa_exito_logos: float = 0.0
    total_logos_generados: int = 0
    tiempo_promedio_generacion_logos: float = 0.0

    # ID para persistencia (opcional)
    id: Optional[int] = None

    def __post_init__(self):
        """Validaciones de dominio"""
        if self.porcentaje_aprobacion < 0 or self.porcentaje_aprobacion > 100:
            raise ValueError("El porcentaje de aprobación debe estar entre 0 y 100")

        if self.tasa_exito_logos < 0 or self.tasa_exito_logos > 100:
            raise ValueError("La tasa de éxito de logos debe estar entre 0 y 100")

        if self.ingresos_mes < 0:
            raise ValueError("Los ingresos no pueden ser negativos")
