# apps/analytics/use_cases/__init__.py
"""
Use Cases Layer - Lógica de aplicación
Responsabilidad: Orquestar operaciones de negocio usando entidades y repositorios
"""

from .marca_use_cases import (
    CrearMarcaUseCase,
    ObtenerMarcaUseCase,
    ActualizarMarcaUseCase,
    EliminarMarcaUseCase,
    ListarMarcasUseCase,
    CambiarEstadoMarcaUseCase,
    ObtenerEstadisticasMarcasUseCase,
)

from .logo_use_cases import (
    GenerarLogoUseCase,
    ObtenerLogoUseCase,
    ListarLogosUseCase,
    ObtenerEstadisticasLogosUseCase,
)

from .kpi_use_cases import (
    CalcularKPIsUseCase,
    ObtenerKPIsUseCase,
    GenerarReporteKPIsUseCase,
)

from .dashboard_use_cases import (
    ObtenerDashboardDataUseCase,
    GenerarReporteDashboardUseCase,
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
]
