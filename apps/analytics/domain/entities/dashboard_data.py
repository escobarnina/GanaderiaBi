# apps/analytics/domain/entities/dashboard_data.py
"""
Entidad de dominio para datos del dashboard
Agregación de datos para visualización
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class DashboardData:
    """
    Entidad de dominio para datos del dashboard
    Agregación de datos para visualización
    """

    kpis_principales: Dict[str, Any] = field(default_factory=dict)
    tendencias_mensuales: List[Dict[str, Any]] = field(default_factory=list)
    metricas_tiempo_real: Dict[str, Any] = field(default_factory=dict)
    resumen_ejecutivo: Dict[str, Any] = field(default_factory=dict)
