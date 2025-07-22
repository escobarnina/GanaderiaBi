# apps/analytics/domain/repositories/kpi_repository.py
"""
Interfaz para repositorio de KPIs de ganado bovino
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from ..entities.kpi_ganado_bovino import KPIGanadoBovino


class KPIGanadoBovinoRepository(ABC):
    """Interfaz para repositorio de KPIs de ganado bovino"""

    @abstractmethod
    def get_by_fecha(self, fecha: date) -> Optional[KPIGanadoBovino]:
        """Obtiene KPIs por fecha"""
        pass

    @abstractmethod
    def get_latest(self) -> Optional[KPIGanadoBovino]:
        """Obtiene los KPIs más recientes"""
        pass

    @abstractmethod
    def list_by_periodo(
        self, fecha_inicio: date, fecha_fin: date
    ) -> List[KPIGanadoBovino]:
        """Lista KPIs por período"""
        pass

    @abstractmethod
    def save(self, kpi: KPIGanadoBovino) -> KPIGanadoBovino:
        """Guarda KPIs (crear o actualizar)"""
        pass

    @abstractmethod
    def delete(self, kpi_id: int) -> bool:
        """Elimina KPIs por ID"""
        pass

    @abstractmethod
    def calcular_kpis_actuales(self) -> KPIGanadoBovino:
        """Calcula KPIs actuales basado en datos en tiempo real"""
        pass
