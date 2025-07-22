"""
Use Cases para el sistema de inteligencia de negocios ganadero
"""

# Use Cases de Marca
from .marca.crear_marca_use_case import CrearMarcaUseCase
from .marca.obtener_marca_use_case import ObtenerMarcaUseCase
from .marca.actualizar_marca_use_case import ActualizarMarcaUseCase
from .marca.eliminar_marca_use_case import EliminarMarcaUseCase
from .marca.listar_marcas_use_case import ListarMarcasUseCase
from .marca.cambiar_estado_marca_use_case import CambiarEstadoMarcaUseCase
from .marca.obtener_estadisticas_marcas_use_case import ObtenerEstadisticasMarcasUseCase

# Use Cases de Logo (mantener los existentes por ahora)
from .logo_use_cases import (
    GenerarLogoUseCase,
    ObtenerLogoUseCase,
    ListarLogosUseCase,
    ObtenerEstadisticasLogosUseCase,
)

# Use Cases de KPI (mantener los existentes por ahora)
from .kpi_use_cases import (
    CalcularKPIsUseCase,
    ObtenerKPIsUseCase,
    GenerarReporteKPIsUseCase,
)

# Use Cases de Dashboard (mantener los existentes por ahora)
from .dashboard_use_cases import (
    ObtenerDashboardDataUseCase,
    GenerarReporteDashboardUseCase,
)

# Use Cases de Historial (mantener los existentes por ahora)
from .historial_use_cases import (
    CrearHistorialUseCase,
    ObtenerHistorialUseCase,
    ListarHistorialMarcaUseCase,
    ObtenerActividadRecienteUseCase,
    ObtenerAuditoriaUsuarioUseCase,
    ObtenerPatronesCambioUseCase,
    ObtenerEficienciaEvaluadoresUseCase,
)

# Use Cases de Reporte (mantener los existentes por ahora)
from .reporte_use_cases import (
    GenerarReporteMensualUseCase,
    GenerarReporteAnualUseCase,
    GenerarReporteComparativoDepartamentosUseCase,
    GenerarReportePersonalizadoUseCase,
    ExportarReporteExcelUseCase,
    GenerarReporteProductorUseCase,
    GenerarReporteImpactoEconomicoUseCase,
    GenerarReporteInnovacionTecnologicaUseCase,
    GenerarReporteSostenibilidadUseCase,
)

__all__ = [
    # Marca Use Cases
    "CrearMarcaUseCase",
    "ObtenerMarcaUseCase",
    "ActualizarMarcaUseCase",
    "EliminarMarcaUseCase",
    "ListarMarcasUseCase",
    "CambiarEstadoMarcaUseCase",
    "ObtenerEstadisticasMarcasUseCase",
    # Logo Use Cases
    "GenerarLogoUseCase",
    "ObtenerLogoUseCase",
    "ListarLogosUseCase",
    "ObtenerEstadisticasLogosUseCase",
    # KPI Use Cases
    "CalcularKPIsUseCase",
    "ObtenerKPIsUseCase",
    "GenerarReporteKPIsUseCase",
    # Dashboard Use Cases
    "ObtenerDashboardDataUseCase",
    "GenerarReporteDashboardUseCase",
    # Historial Use Cases
    "CrearHistorialUseCase",
    "ObtenerHistorialUseCase",
    "ListarHistorialMarcaUseCase",
    "ObtenerActividadRecienteUseCase",
    "ObtenerAuditoriaUsuarioUseCase",
    "ObtenerPatronesCambioUseCase",
    "ObtenerEficienciaEvaluadoresUseCase",
    # Reporte Use Cases
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
