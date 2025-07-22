from typing import List, Optional
from datetime import date

from apps.analytics.domain.entities.kpi_ganado_bovino import KPIGanadoBovino
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository


class ObtenerKPIsUseCase:
    """Use Case para obtener KPIs existentes"""

    def __init__(self, kpi_repository: KPIGanadoBovinoRepository):
        self.kpi_repository = kpi_repository

    def execute(
        self,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        limit: int = 100,
    ) -> List[KPIGanadoBovino]:
        """
        Obtiene KPIs en un rango de fechas

        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
            limit: Límite de resultados

        Returns:
            List[KPIGanadoBovino]: Lista de KPIs
        """
        return self.kpi_repository.listar_por_fechas(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, limit=limit
        )
