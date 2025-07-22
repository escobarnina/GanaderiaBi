# apps/analytics/domain/repositories/reporte_repository.py
"""
Interfaz para repositorio de reportes
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import date

from ..entities.reporte_data import ReporteData


class ReporteRepository(ABC):
    """Interfaz para repositorio de reportes"""

    @abstractmethod
    def generar_reporte_ejecutivo_mensual(self, mes: int, anio: int) -> ReporteData:
        """Genera reporte ejecutivo mensual"""
        pass

    @abstractmethod
    def generar_reporte_anual(self, anio: int) -> ReporteData:
        """Genera reporte anual"""
        pass

    @abstractmethod
    def generar_reporte_comparativo_departamentos(
        self, fecha_inicio: date, fecha_fin: date
    ) -> ReporteData:
        """Genera reporte comparativo entre departamentos"""
        pass

    @abstractmethod
    def generar_reporte_personalizado(self, filtros: Dict[str, Any]) -> ReporteData:
        """Genera reporte personalizado según filtros"""
        pass
