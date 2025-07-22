"""
Use Cases para gestión de reportes ejecutivos
"""

from .generar_reporte_mensual_use_case import GenerarReporteMensualUseCase
from .generar_reporte_anual_use_case import GenerarReporteAnualUseCase
from .generar_reporte_comparativo_departamentos_use_case import (
    GenerarReporteComparativoDepartamentosUseCase,
)
from .generar_reporte_personalizado_use_case import GenerarReportePersonalizadoUseCase
from .exportar_reporte_excel_use_case import ExportarReporteExcelUseCase
from .generar_reporte_productor_use_case import GenerarReporteProductorUseCase
from .generar_reporte_impacto_economico_use_case import (
    GenerarReporteImpactoEconomicoUseCase,
)
from .generar_reporte_innovacion_tecnologica_use_case import (
    GenerarReporteInnovacionTecnologicaUseCase,
)
from .generar_reporte_sostenibilidad_use_case import GenerarReporteSostenibilidadUseCase

__all__ = [
    "GenerarReporteMensualUseCase",
    "GenerarReporteAnualUseCase",
    "GenerarReporteComparativoDepartamentosUseCase",
    "GenerarReportePersonalizadoUseCase",
    "ExportarReporteExcelUseCase",
    "GenerarReporteProductorUseCase",
    "GenerarReporteImpactoEconomicoUseCase",
    "GenerarReporteInnovacionTecnologicaUseCase",
    "GenerarReporteSostenibilidadUseCase",
]
