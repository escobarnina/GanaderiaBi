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

# Use Cases de Dashboard
from .dashboard.obtener_dashboard_data_use_case import ObtenerDashboardDataUseCase
from .dashboard.generar_reporte_dashboard_use_case import GenerarReporteDashboardUseCase

# Use Cases de Logo
from .logo.generar_logo_use_case import GenerarLogoUseCase
from .logo.obtener_logo_use_case import ObtenerLogoUseCase
from .logo.listar_logos_use_case import ListarLogosUseCase
from .logo.obtener_estadisticas_logos_use_case import ObtenerEstadisticasLogosUseCase

# Use Cases de KPI
from .kpi.calcular_kpis_use_case import CalcularKPIsUseCase
from .kpi.obtener_kpis_use_case import ObtenerKPIsUseCase
from .kpi.generar_reporte_kpis_use_case import GenerarReporteKPIsUseCase

# Use Cases de Historial
from .historial.crear_historial_use_case import CrearHistorialUseCase
from .historial.obtener_historial_use_case import ObtenerHistorialUseCase
from .historial.listar_historial_marca_use_case import ListarHistorialMarcaUseCase
from .historial.obtener_actividad_reciente_use_case import (
    ObtenerActividadRecienteUseCase,
)
from .historial.obtener_auditoria_usuario_use_case import ObtenerAuditoriaUsuarioUseCase
from .historial.obtener_patrones_cambio_use_case import ObtenerPatronesCambioUseCase
from .historial.obtener_eficiencia_evaluadores_use_case import (
    ObtenerEficienciaEvaluadoresUseCase,
)

# Use Cases de Reporte
from .reporte.generar_reporte_mensual_use_case import GenerarReporteMensualUseCase
from .reporte.generar_reporte_anual_use_case import GenerarReporteAnualUseCase
from .reporte.generar_reporte_comparativo_departamentos_use_case import (
    GenerarReporteComparativoDepartamentosUseCase,
)
from .reporte.generar_reporte_personalizado_use_case import (
    GenerarReportePersonalizadoUseCase,
)
from .reporte.exportar_reporte_excel_use_case import ExportarReporteExcelUseCase
from .reporte.generar_reporte_productor_use_case import GenerarReporteProductorUseCase
from .reporte.generar_reporte_impacto_economico_use_case import (
    GenerarReporteImpactoEconomicoUseCase,
)
from .reporte.generar_reporte_innovacion_tecnologica_use_case import (
    GenerarReporteInnovacionTecnologicaUseCase,
)
from .reporte.generar_reporte_sostenibilidad_use_case import (
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
    # Dashboard Use Cases
    "ObtenerDashboardDataUseCase",
    "GenerarReporteDashboardUseCase",
    # Logo Use Cases
    "GenerarLogoUseCase",
    "ObtenerLogoUseCase",
    "ListarLogosUseCase",
    "ObtenerEstadisticasLogosUseCase",
    # KPI Use Cases
    "CalcularKPIsUseCase",
    "ObtenerKPIsUseCase",
    "GenerarReporteKPIsUseCase",
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
