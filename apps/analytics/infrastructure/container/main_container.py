"""
Container principal para inyección de dependencias
Responsabilidad única: Orquestar containers específicos
"""

from apps.analytics.infrastructure.container.repositories_container import (
    RepositoriesContainer,
)
from apps.analytics.infrastructure.container.use_cases_container import (
    UseCasesContainer,
)


class MainContainer:
    """Container principal que orquesta todos los containers específicos"""

    def __init__(self):
        self.repositories_container = RepositoriesContainer()
        self.use_cases_container = UseCasesContainer(self.repositories_container)

    # Métodos para repositorios
    def get_marca_repository(self):
        return self.repositories_container.get_marca_repository()

    def get_logo_repository(self):
        return self.repositories_container.get_logo_repository()

    def get_kpi_repository(self):
        return self.repositories_container.get_kpi_repository()

    def get_historial_repository(self):
        return self.repositories_container.get_historial_repository()

    def get_dashboard_repository(self):
        return self.repositories_container.get_dashboard_repository()

    def get_reporte_repository(self):
        return self.repositories_container.get_reporte_repository()

    # Métodos para use cases de marca
    def get_crear_marca_use_case(self):
        return self.use_cases_container.get_crear_marca_use_case()

    def get_obtener_marca_use_case(self):
        return self.use_cases_container.get_obtener_marca_use_case()

    def get_actualizar_marca_use_case(self):
        return self.use_cases_container.get_actualizar_marca_use_case()

    def get_eliminar_marca_use_case(self):
        return self.use_cases_container.get_eliminar_marca_use_case()

    def get_listar_marcas_use_case(self):
        return self.use_cases_container.get_listar_marcas_use_case()

    def get_cambiar_estado_marca_use_case(self):
        return self.use_cases_container.get_cambiar_estado_marca_use_case()

    def get_obtener_estadisticas_marcas_use_case(self):
        return self.use_cases_container.get_obtener_estadisticas_marcas_use_case()

    # Métodos para use cases de logo
    def get_generar_logo_use_case(self):
        return self.use_cases_container.get_generar_logo_use_case()

    def get_obtener_logo_use_case(self):
        return self.use_cases_container.get_obtener_logo_use_case()

    def get_listar_logos_use_case(self):
        return self.use_cases_container.get_listar_logos_use_case()

    def get_obtener_estadisticas_logos_use_case(self):
        return self.use_cases_container.get_obtener_estadisticas_logos_use_case()

    def get_generar_prompt_logo_use_case(self):
        return self.use_cases_container.get_generar_prompt_logo_use_case()

    # Métodos para use cases de KPI
    def get_calcular_kpis_use_case(self):
        return self.use_cases_container.get_calcular_kpis_use_case()

    def get_obtener_kpis_use_case(self):
        return self.use_cases_container.get_obtener_kpis_use_case()

    def get_generar_reporte_kpis_use_case(self):
        return self.use_cases_container.get_generar_reporte_kpis_use_case()

    # Métodos para use cases de dashboard
    def get_obtener_dashboard_data_use_case(self):
        return self.use_cases_container.get_obtener_dashboard_data_use_case()

    def get_generar_reporte_dashboard_use_case(self):
        return self.use_cases_container.get_generar_reporte_dashboard_use_case()

    # Métodos para use cases de historial
    def get_crear_historial_use_case(self):
        return self.use_cases_container.get_crear_historial_use_case()

    def get_obtener_historial_use_case(self):
        return self.use_cases_container.get_obtener_historial_use_case()

    def get_listar_historial_marca_use_case(self):
        return self.use_cases_container.get_listar_historial_marca_use_case()

    def get_obtener_actividad_reciente_use_case(self):
        return self.use_cases_container.get_obtener_actividad_reciente_use_case()

    def get_obtener_auditoria_usuario_use_case(self):
        return self.use_cases_container.get_obtener_auditoria_usuario_use_case()

    def get_obtener_patrones_cambio_use_case(self):
        return self.use_cases_container.get_obtener_patrones_cambio_use_case()

    def get_obtener_eficiencia_evaluadores_use_case(self):
        return self.use_cases_container.get_obtener_eficiencia_evaluadores_use_case()

    # Métodos para use cases de reporte
    def get_generar_reporte_mensual_use_case(self):
        return self.use_cases_container.get_generar_reporte_mensual_use_case()

    def get_generar_reporte_anual_use_case(self):
        return self.use_cases_container.get_generar_reporte_anual_use_case()

    def get_generar_reporte_comparativo_departamentos_use_case(self):
        return (
            self.use_cases_container.get_generar_reporte_comparativo_departamentos_use_case()
        )

    def get_generar_reporte_personalizado_use_case(self):
        return self.use_cases_container.get_generar_reporte_personalizado_use_case()

    def get_exportar_reporte_excel_use_case(self):
        return self.use_cases_container.get_exportar_reporte_excel_use_case()

    def get_generar_reporte_productor_use_case(self):
        return self.use_cases_container.get_generar_reporte_productor_use_case()

    def get_generar_reporte_impacto_economico_use_case(self):
        return self.use_cases_container.get_generar_reporte_impacto_economico_use_case()

    def get_generar_reporte_innovacion_tecnologica_use_case(self):
        return (
            self.use_cases_container.get_generar_reporte_innovacion_tecnologica_use_case()
        )

    def get_generar_reporte_sostenibilidad_use_case(self):
        return self.use_cases_container.get_generar_reporte_sostenibilidad_use_case()

    # Métodos para use cases de data generation
    def get_generar_datos_mockaroo_use_case(self):
        return self.use_cases_container.get_generar_datos_mockaroo_use_case()

    def get_generar_descripcion_marca_use_case(self):
        return self.use_cases_container.get_generar_descripcion_marca_use_case()

    def get_generar_prompt_logo_use_case(self):
        return self.use_cases_container.get_generar_prompt_logo_use_case()

    # Métodos para use cases de analytics
    def get_calcular_tendencias_departamento_use_case(self):
        return self.use_cases_container.get_calcular_tendencias_departamento_use_case()


# Alias para mantener compatibilidad
Container = MainContainer
