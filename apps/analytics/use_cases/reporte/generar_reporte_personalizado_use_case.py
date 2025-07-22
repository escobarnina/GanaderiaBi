from typing import Optional, Dict, Any
from datetime import datetime

from apps.analytics.domain.entities.reporte_data import ReporteData
from apps.analytics.domain.repositories.reporte_repository import ReporteRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository


class GenerarReportePersonalizadoUseCase:
    """Use Case para generar reporte personalizado"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
        logo_repository: LogoMarcaBovinaRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository
        self.logo_repository = logo_repository

    def execute(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        tipo_reporte: str,
        filtros: Optional[Dict[str, Any]] = None,
    ) -> ReporteData:
        """
        Genera un reporte personalizado

        Args:
            fecha_inicio: Fecha de inicio del reporte
            fecha_fin: Fecha de fin del reporte
            tipo_reporte: Tipo de reporte a generar
            filtros: Filtros adicionales

        Returns:
            ReporteData: Reporte generado
        """
        if tipo_reporte == "logos":
            return self.reporte_repository.generar_reporte_logos(
                fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
            )
        elif tipo_reporte == "kpis":
            return self.reporte_repository.generar_reporte_kpis(
                fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
            )
        else:
            return self.reporte_repository.generar_reporte_consolidado(
                fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
            )
