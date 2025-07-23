"""
Serializers de Clean Architecture para la aplicación de analytics
Trabajan con entidades de dominio, no con modelos Django
"""

from .marca_serializers import (
    MarcaGanadoBovinoSerializer,
    MarcaGanadoBovinoListSerializer,
    HistorialEstadoMarcaSerializer,
)

from .logo_serializers import (
    LogoMarcaBovinaSerializer,
    LogoMarcaBovinaListSerializer,
)

from .kpi_serializers import (
    KPIGanadoBovinoSerializer,
    KPIGanadoBovinoListSerializer,
)

from .dashboard_serializers import (
    DashboardDataSerializer,
    DashboardKPIBovinoSerializer,
    EstadisticasMensualesBovinoSerializer,
    EstadisticasPorRazaSerializer,
    EstadisticasPorDepartamentoSerializer,
    RendimientoModelosIASerializer,
)

from .historial_serializers import (
    HistorialEstadoMarcaSerializer as HistorialSerializer,
    HistorialEstadoMarcaListSerializer,
    ActividadRecienteSerializer,
    AuditoriaUsuarioSerializer,
    PatronesCambioSerializer,
    EficienciaEvaluadoresSerializer,
)

from .reporte_serializers import (
    ReporteDataSerializer,
    ReporteMensualSerializer,
    ReporteAnualSerializer,
    ReporteComparativoDepartamentosSerializer,
    ReportePersonalizadoSerializer,
    ReporteProductorSerializer,
    ReporteImpactoEconomicoSerializer,
    ReporteInnovacionTecnologicaSerializer,
    ReporteSostenibilidadSerializer,
    ExportacionReporteSerializer,
)

__all__ = [
    # Marca serializers
    "MarcaGanadoBovinoSerializer",
    "MarcaGanadoBovinoListSerializer",
    "HistorialEstadoMarcaSerializer",
    # Logo serializers
    "LogoMarcaBovinaSerializer",
    "LogoMarcaBovinaListSerializer",
    # KPI serializers
    "KPIGanadoBovinoSerializer",
    "KPIGanadoBovinoListSerializer",
    # Dashboard serializers
    "DashboardDataSerializer",
    "DashboardKPIBovinoSerializer",
    "EstadisticasMensualesBovinoSerializer",
    "EstadisticasPorRazaSerializer",
    "EstadisticasPorDepartamentoSerializer",
    "RendimientoModelosIASerializer",
    # Historial serializers
    "HistorialSerializer",
    "HistorialEstadoMarcaListSerializer",
    "ActividadRecienteSerializer",
    "AuditoriaUsuarioSerializer",
    "PatronesCambioSerializer",
    "EficienciaEvaluadoresSerializer",
    # Reporte serializers
    "ReporteDataSerializer",
    "ReporteMensualSerializer",
    "ReporteAnualSerializer",
    "ReporteComparativoDepartamentosSerializer",
    "ReportePersonalizadoSerializer",
    "ReporteProductorSerializer",
    "ReporteImpactoEconomicoSerializer",
    "ReporteInnovacionTecnologicaSerializer",
    "ReporteSostenibilidadSerializer",
    "ExportacionReporteSerializer",
]
