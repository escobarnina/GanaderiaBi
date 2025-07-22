# apps/analytics/domain/repositories/dashboard_repository.py
"""
Interfaz para repositorio de datos del dashboard
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class DashboardRepository(ABC):
    """Interfaz para repositorio de datos del dashboard"""

    @abstractmethod
    def get_kpis_principales(self) -> Dict[str, Any]:
        """Obtiene KPIs principales para el dashboard"""
        pass

    @abstractmethod
    def get_tendencias_mensuales(self, meses: int = 12) -> List[Dict[str, Any]]:
        """Obtiene tendencias mensuales"""
        pass

    @abstractmethod
    def get_metricas_tiempo_real(self) -> Dict[str, Any]:
        """Obtiene métricas en tiempo real"""
        pass

    @abstractmethod
    def get_resumen_ejecutivo(self) -> Dict[str, Any]:
        """Obtiene resumen ejecutivo"""
        pass
