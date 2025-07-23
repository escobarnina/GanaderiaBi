"""
Container para configuración de use cases
Responsabilidad única: Configurar e inyectar use cases
"""

from typing import Dict, Any

# Importar use cases de marca
from apps.analytics.use_cases.marca.crear_marca_use_case import CrearMarcaUseCase
from apps.analytics.use_cases.marca.obtener_marca_use_case import ObtenerMarcaUseCase
from apps.analytics.use_cases.marca.actualizar_marca_use_case import (
    ActualizarMarcaUseCase,
)
from apps.analytics.use_cases.marca.eliminar_marca_use_case import EliminarMarcaUseCase
from apps.analytics.use_cases.marca.listar_marcas_use_case import ListarMarcasUseCase
from apps.analytics.use_cases.marca.cambiar_estado_marca_use_case import (
    CambiarEstadoMarcaUseCase,
)
from apps.analytics.use_cases.marca.obtener_estadisticas_marcas_use_case import (
    ObtenerEstadisticasMarcasUseCase,
)

# Importar use cases de logo
from apps.analytics.use_cases.logo.generar_logo_use_case import GenerarLogoUseCase
from apps.analytics.use_cases.logo.obtener_logo_use_case import ObtenerLogoUseCase
from apps.analytics.use_cases.logo.listar_logos_use_case import ListarLogosUseCase
from apps.analytics.use_cases.logo.obtener_estadisticas_logos_use_case import (
    ObtenerEstadisticasLogosUseCase,
)
from apps.analytics.use_cases.data_generation.generar_prompt_logo_use_case import (
    GenerarPromptLogoUseCase,
)

# Importar use cases de data generation
from apps.analytics.use_cases.data_generation.generar_datos_mockaroo_use_case import (
    GenerarDatosMockarooUseCase,
)
from apps.analytics.use_cases.data_generation.generar_descripcion_marca_use_case import (
    GenerarDescripcionMarcaUseCase,
)

# Importar use cases de analytics
from apps.analytics.use_cases.analytics.calcular_tendencias_departamento_use_case import (
    CalcularTendenciasDepartamentoUseCase,
)

# Importar use cases de KPI
from apps.analytics.use_cases.kpi.calcular_kpis_use_case import CalcularKPIsUseCase
from apps.analytics.use_cases.kpi.obtener_kpis_use_case import ObtenerKPIsUseCase
from apps.analytics.use_cases.kpi.generar_reporte_kpis_use_case import (
    GenerarReporteKPIsUseCase,
)

# Importar use cases de dashboard
from apps.analytics.use_cases.dashboard.obtener_dashboard_data_use_case import (
    ObtenerDashboardDataUseCase,
)
from apps.analytics.use_cases.dashboard.generar_reporte_dashboard_use_case import (
    GenerarReporteDashboardUseCase,
)

# Importar use cases de historial
from apps.analytics.use_cases.historial.crear_historial_use_case import (
    CrearHistorialUseCase,
)
from apps.analytics.use_cases.historial.obtener_historial_use_case import (
    ObtenerHistorialUseCase,
)
from apps.analytics.use_cases.historial.listar_historial_marca_use_case import (
    ListarHistorialMarcaUseCase,
)
from apps.analytics.use_cases.historial.obtener_actividad_reciente_use_case import (
    ObtenerActividadRecienteUseCase,
)
from apps.analytics.use_cases.historial.obtener_auditoria_usuario_use_case import (
    ObtenerAuditoriaUsuarioUseCase,
)
from apps.analytics.use_cases.historial.obtener_patrones_cambio_use_case import (
    ObtenerPatronesCambioUseCase,
)
from apps.analytics.use_cases.historial.obtener_eficiencia_evaluadores_use_case import (
    ObtenerEficienciaEvaluadoresUseCase,
)

# Importar use cases de reporte
from apps.analytics.use_cases.reporte.generar_reporte_mensual_use_case import (
    GenerarReporteMensualUseCase,
)
from apps.analytics.use_cases.reporte.generar_reporte_anual_use_case import (
    GenerarReporteAnualUseCase,
)
from apps.analytics.use_cases.reporte.generar_reporte_comparativo_departamentos_use_case import (
    GenerarReporteComparativoDepartamentosUseCase,
)
from apps.analytics.use_cases.reporte.generar_reporte_personalizado_use_case import (
    GenerarReportePersonalizadoUseCase,
)
from apps.analytics.use_cases.reporte.exportar_reporte_excel_use_case import (
    ExportarReporteExcelUseCase,
)
from apps.analytics.use_cases.reporte.generar_reporte_productor_use_case import (
    GenerarReporteProductorUseCase,
)
from apps.analytics.use_cases.reporte.generar_reporte_impacto_economico_use_case import (
    GenerarReporteImpactoEconomicoUseCase,
)
from apps.analytics.use_cases.reporte.generar_reporte_innovacion_tecnologica_use_case import (
    GenerarReporteInnovacionTecnologicaUseCase,
)
from apps.analytics.use_cases.reporte.generar_reporte_sostenibilidad_use_case import (
    GenerarReporteSostenibilidadUseCase,
)


class UseCasesContainer:
    """Container específico para use cases"""

    def __init__(self, repositories_container):
        self.repositories_container = repositories_container
        self._use_cases: Dict[str, Any] = {}
        self._configure_use_cases()

    def _configure_use_cases(self):
        """Configura los use cases con inyección de dependencias"""
        # Obtener repositorios
        marca_repo = self.repositories_container.get_marca_repository()
        logo_repo = self.repositories_container.get_logo_repository()
        kpi_repo = self.repositories_container.get_kpi_repository()
        historial_repo = self.repositories_container.get_historial_repository()
        dashboard_repo = self.repositories_container.get_dashboard_repository()
        reporte_repo = self.repositories_container.get_reporte_repository()

        # Configurar use cases de marcas
        self._use_cases.update(
            {
                "crear_marca_use_case": CrearMarcaUseCase(marca_repo),
                "obtener_marca_use_case": ObtenerMarcaUseCase(marca_repo),
                "actualizar_marca_use_case": ActualizarMarcaUseCase(marca_repo),
                "eliminar_marca_use_case": EliminarMarcaUseCase(marca_repo),
                "listar_marcas_use_case": ListarMarcasUseCase(marca_repo),
                "cambiar_estado_marca_use_case": CambiarEstadoMarcaUseCase(marca_repo),
                "obtener_estadisticas_marcas_use_case": ObtenerEstadisticasMarcasUseCase(
                    marca_repo
                ),
            }
        )

        # Configurar use cases de logos
        self._use_cases.update(
            {
                "generar_logo_use_case": GenerarLogoUseCase(logo_repo),
                "obtener_logo_use_case": ObtenerLogoUseCase(logo_repo),
                "listar_logos_use_case": ListarLogosUseCase(logo_repo),
                "obtener_estadisticas_logos_use_case": ObtenerEstadisticasLogosUseCase(
                    logo_repo
                ),
                "generar_prompt_logo_use_case": GenerarPromptLogoUseCase(marca_repo),
            }
        )

        # Configurar use cases de KPIs
        self._use_cases.update(
            {
                "calcular_kpis_use_case": CalcularKPIsUseCase(
                    kpi_repo, marca_repo, logo_repo
                ),
                "obtener_kpis_use_case": ObtenerKPIsUseCase(kpi_repo),
                "generar_reporte_kpis_use_case": GenerarReporteKPIsUseCase(kpi_repo),
            }
        )

        # Configurar use cases de dashboard
        self._use_cases.update(
            {
                "obtener_dashboard_data_use_case": ObtenerDashboardDataUseCase(
                    dashboard_repo, marca_repo, kpi_repo, logo_repo
                ),
                "generar_reporte_dashboard_use_case": GenerarReporteDashboardUseCase(
                    dashboard_repo
                ),
            }
        )

        # Configurar use cases de historial
        self._use_cases.update(
            {
                "crear_historial_use_case": CrearHistorialUseCase(historial_repo),
                "obtener_historial_use_case": ObtenerHistorialUseCase(historial_repo),
                "listar_historial_marca_use_case": ListarHistorialMarcaUseCase(
                    historial_repo
                ),
                "obtener_actividad_reciente_use_case": ObtenerActividadRecienteUseCase(
                    historial_repo
                ),
                "obtener_auditoria_usuario_use_case": ObtenerAuditoriaUsuarioUseCase(
                    historial_repo
                ),
                "obtener_patrones_cambio_use_case": ObtenerPatronesCambioUseCase(
                    historial_repo
                ),
                "obtener_eficiencia_evaluadores_use_case": ObtenerEficienciaEvaluadoresUseCase(
                    historial_repo
                ),
            }
        )

        # Configurar use cases de reporte
        self._use_cases.update(
            {
                "generar_reporte_mensual_use_case": GenerarReporteMensualUseCase(
                    reporte_repo, marca_repo
                ),
                "generar_reporte_anual_use_case": GenerarReporteAnualUseCase(
                    reporte_repo, marca_repo
                ),
                "generar_reporte_comparativo_departamentos_use_case": GenerarReporteComparativoDepartamentosUseCase(
                    reporte_repo, marca_repo
                ),
                "generar_reporte_personalizado_use_case": GenerarReportePersonalizadoUseCase(
                    reporte_repo, marca_repo, kpi_repo, logo_repo
                ),
                "exportar_reporte_excel_use_case": ExportarReporteExcelUseCase(
                    reporte_repo, marca_repo
                ),
                "generar_reporte_productor_use_case": GenerarReporteProductorUseCase(
                    reporte_repo, marca_repo, historial_repo, logo_repo
                ),
                "generar_reporte_impacto_economico_use_case": GenerarReporteImpactoEconomicoUseCase(
                    reporte_repo, marca_repo, kpi_repo
                ),
                "generar_reporte_innovacion_tecnologica_use_case": GenerarReporteInnovacionTecnologicaUseCase(
                    reporte_repo, logo_repo, kpi_repo
                ),
                "generar_reporte_sostenibilidad_use_case": GenerarReporteSostenibilidadUseCase(
                    reporte_repo, marca_repo, kpi_repo
                ),
            }
        )

        # Configurar use cases de data generation
        self._use_cases.update(
            {
                "generar_datos_mockaroo_use_case": GenerarDatosMockarooUseCase(
                    marca_repo
                ),
                "generar_descripcion_marca_use_case": GenerarDescripcionMarcaUseCase(
                    marca_repo
                ),
            }
        )

        # Configurar use cases de analytics
        self._use_cases.update(
            {
                "calcular_tendencias_departamento_use_case": CalcularTendenciasDepartamentoUseCase(
                    marca_repo, kpi_repo
                ),
            }
        )

    def get_crear_marca_use_case(self) -> CrearMarcaUseCase:
        """Obtiene el use case para crear marcas"""
        return self._use_cases["crear_marca_use_case"]

    def get_obtener_marca_use_case(self) -> ObtenerMarcaUseCase:
        """Obtiene el use case para obtener marcas"""
        return self._use_cases["obtener_marca_use_case"]

    def get_actualizar_marca_use_case(self) -> ActualizarMarcaUseCase:
        """Obtiene el use case para actualizar marcas"""
        return self._use_cases["actualizar_marca_use_case"]

    def get_eliminar_marca_use_case(self) -> EliminarMarcaUseCase:
        """Obtiene el use case para eliminar marcas"""
        return self._use_cases["eliminar_marca_use_case"]

    def get_listar_marcas_use_case(self) -> ListarMarcasUseCase:
        """Obtiene el use case para listar marcas"""
        return self._use_cases["listar_marcas_use_case"]

    def get_cambiar_estado_marca_use_case(self) -> CambiarEstadoMarcaUseCase:
        """Obtiene el use case para cambiar estado de marcas"""
        return self._use_cases["cambiar_estado_marca_use_case"]

    def get_obtener_estadisticas_marcas_use_case(
        self,
    ) -> ObtenerEstadisticasMarcasUseCase:
        """Obtiene el use case para obtener estadísticas de marcas"""
        return self._use_cases["obtener_estadisticas_marcas_use_case"]

    def get_generar_logo_use_case(self) -> GenerarLogoUseCase:
        """Obtiene el use case para generar logos"""
        return self._use_cases["generar_logo_use_case"]

    def get_obtener_logo_use_case(self) -> ObtenerLogoUseCase:
        """Obtiene el use case para obtener logos"""
        return self._use_cases["obtener_logo_use_case"]

    def get_listar_logos_use_case(self) -> ListarLogosUseCase:
        """Obtiene el use case para listar logos"""
        return self._use_cases["listar_logos_use_case"]

    def get_obtener_estadisticas_logos_use_case(
        self,
    ) -> ObtenerEstadisticasLogosUseCase:
        """Obtiene el use case para obtener estadísticas de logos"""
        return self._use_cases["obtener_estadisticas_logos_use_case"]

    def get_generar_prompt_logo_use_case(self) -> GenerarPromptLogoUseCase:
        """Obtiene el use case para generar prompts de logo"""
        return self._use_cases["generar_prompt_logo_use_case"]

    def get_calcular_kpis_use_case(self) -> CalcularKPIsUseCase:
        """Obtiene el use case para calcular KPIs"""
        return self._use_cases["calcular_kpis_use_case"]

    def get_obtener_kpis_use_case(self) -> ObtenerKPIsUseCase:
        """Obtiene el use case para obtener KPIs"""
        return self._use_cases["obtener_kpis_use_case"]

    def get_generar_reporte_kpis_use_case(self) -> GenerarReporteKPIsUseCase:
        """Obtiene el use case para generar reporte de KPIs"""
        return self._use_cases["generar_reporte_kpis_use_case"]

    def get_obtener_dashboard_data_use_case(self) -> ObtenerDashboardDataUseCase:
        """Obtiene el use case para obtener datos del dashboard"""
        return self._use_cases["obtener_dashboard_data_use_case"]

    def get_generar_reporte_dashboard_use_case(self) -> GenerarReporteDashboardUseCase:
        """Obtiene el use case para generar reporte del dashboard"""
        return self._use_cases["generar_reporte_dashboard_use_case"]

    def get_crear_historial_use_case(self) -> CrearHistorialUseCase:
        """Obtiene el use case para crear historial"""
        return self._use_cases["crear_historial_use_case"]

    def get_obtener_historial_use_case(self) -> ObtenerHistorialUseCase:
        """Obtiene el use case para obtener historial"""
        return self._use_cases["obtener_historial_use_case"]

    def get_listar_historial_marca_use_case(self) -> ListarHistorialMarcaUseCase:
        """Obtiene el use case para listar historial de marca"""
        return self._use_cases["listar_historial_marca_use_case"]

    def get_obtener_actividad_reciente_use_case(
        self,
    ) -> ObtenerActividadRecienteUseCase:
        """Obtiene el use case para obtener actividad reciente"""
        return self._use_cases["obtener_actividad_reciente_use_case"]

    def get_obtener_auditoria_usuario_use_case(self) -> ObtenerAuditoriaUsuarioUseCase:
        """Obtiene el use case para obtener auditoría de usuario"""
        return self._use_cases["obtener_auditoria_usuario_use_case"]

    def get_obtener_patrones_cambio_use_case(self) -> ObtenerPatronesCambioUseCase:
        """Obtiene el use case para obtener patrones de cambio"""
        return self._use_cases["obtener_patrones_cambio_use_case"]

    def get_obtener_eficiencia_evaluadores_use_case(
        self,
    ) -> ObtenerEficienciaEvaluadoresUseCase:
        """Obtiene el use case para obtener eficiencia de evaluadores"""
        return self._use_cases["obtener_eficiencia_evaluadores_use_case"]

    def get_generar_reporte_mensual_use_case(self) -> GenerarReporteMensualUseCase:
        """Obtiene el use case para generar reporte mensual"""
        return self._use_cases["generar_reporte_mensual_use_case"]

    def get_generar_reporte_anual_use_case(self) -> GenerarReporteAnualUseCase:
        """Obtiene el use case para generar reporte anual"""
        return self._use_cases["generar_reporte_anual_use_case"]

    def get_generar_reporte_comparativo_departamentos_use_case(
        self,
    ) -> GenerarReporteComparativoDepartamentosUseCase:
        """Obtiene el use case para generar reporte comparativo de departamentos"""
        return self._use_cases["generar_reporte_comparativo_departamentos_use_case"]

    def get_generar_reporte_personalizado_use_case(
        self,
    ) -> GenerarReportePersonalizadoUseCase:
        """Obtiene el use case para generar reporte personalizado"""
        return self._use_cases["generar_reporte_personalizado_use_case"]

    def get_exportar_reporte_excel_use_case(self) -> ExportarReporteExcelUseCase:
        """Obtiene el use case para exportar reporte a Excel"""
        return self._use_cases["exportar_reporte_excel_use_case"]

    def get_generar_reporte_productor_use_case(self) -> GenerarReporteProductorUseCase:
        """Obtiene el use case para generar reporte de productor"""
        return self._use_cases["generar_reporte_productor_use_case"]

    def get_generar_reporte_impacto_economico_use_case(
        self,
    ) -> GenerarReporteImpactoEconomicoUseCase:
        """Obtiene el use case para generar reporte de impacto económico"""
        return self._use_cases["generar_reporte_impacto_economico_use_case"]

    def get_generar_reporte_innovacion_tecnologica_use_case(
        self,
    ) -> GenerarReporteInnovacionTecnologicaUseCase:
        """Obtiene el use case para generar reporte de innovación tecnológica"""
        return self._use_cases["generar_reporte_innovacion_tecnologica_use_case"]

    def get_generar_reporte_sostenibilidad_use_case(
        self,
    ) -> GenerarReporteSostenibilidadUseCase:
        """Obtiene el use case para generar reporte de sostenibilidad"""
        return self._use_cases["generar_reporte_sostenibilidad_use_case"]

    def get_generar_datos_mockaroo_use_case(self) -> GenerarDatosMockarooUseCase:
        """Obtiene el use case para generar datos con Mockaroo"""
        return self._use_cases["generar_datos_mockaroo_use_case"]

    def get_generar_descripcion_marca_use_case(self) -> GenerarDescripcionMarcaUseCase:
        """Obtiene el use case para generar descripción de marca"""
        return self._use_cases["generar_descripcion_marca_use_case"]

    def get_calcular_tendencias_departamento_use_case(
        self,
    ) -> CalcularTendenciasDepartamentoUseCase:
        """Obtiene el use case para calcular tendencias por departamento"""
        return self._use_cases["calcular_tendencias_departamento_use_case"]

    def get_all_use_cases(self) -> Dict[str, Any]:
        """Obtiene todos los use cases"""
        return self._use_cases.copy()
