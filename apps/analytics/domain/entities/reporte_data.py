# apps/analytics/domain/entities/reporte_data.py
"""
Entidad de dominio para datos de reportes
Estructura para generación de reportes
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ReporteData:
    """
    Entidad de dominio para datos de reportes
    Estructura para generación de reportes
    """

    periodo: str
    tipo_reporte: str
    datos: Dict[str, Any] = field(default_factory=dict)
    filtros: Dict[str, Any] = field(default_factory=dict)
    formato: str = "json"
