"""
Container de inyección de dependencias para la capa de infraestructura
Responsabilidad única: Configurar y proporcionar implementaciones de repositorios y use cases
"""

from typing import Dict, Any

from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository
from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)
from apps.analytics.domain.repositories.dashboard_repository import DashboardRepository
from apps.analytics.domain.repositories.reporte_repository import ReporteRepository

from .repositories.marca_repository import DjangoMarcaRepository
from .repositories.logo_repository import DjangoLogoRepository
from .repositories.kpi_repository import DjangoKpiRepository
from .repositories.historial_repository import DjangoHistorialRepository
from .repositories.dashboard_repository import DjangoDashboardRepository
from .repositories.reporte_repository import DjangoReporteRepository

# Importar use cases
from apps.analytics.use_cases.marca_use_cases import (
    CrearMarcaUseCase,
    ObtenerMarcaUseCase,
    ActualizarMarcaUseCase,
    EliminarMarcaUseCase,
    ListarMarcasUseCase,
    CambiarEstadoMarcaUseCase,
    ObtenerEstadisticasMarcasUseCase,
)
from apps.analytics.use_cases.logo_use_cases import (
    GenerarLogoUseCase,
    ObtenerLogoUseCase,
    ListarLogosUseCase,
    ObtenerEstadisticasLogosUseCase,
)
from apps.analytics.use_cases.kpi_use_cases import (
    CalcularKPIsUseCase,
    ObtenerKPIsUseCase,
    GenerarReporteKPIsUseCase,
)
from apps.analytics.use_cases.dashboard_use_cases import (
    ObtenerDashboardDataUseCase,
    GenerarReporteDashboardUseCase,
)


class Container:
    """Container de inyección de dependencias"""

    def __init__(self):
        """Inicializa el container con las implementaciones de repositorios y use cases"""
        self._repositories: Dict[str, Any] = {}
        self._use_cases: Dict[str, Any] = {}
        self._configure_repositories()
        self._configure_use_cases()

    def _configure_repositories(self):
        """Configura las implementaciones de repositorios"""
        self._repositories = {
            "marca_repository": DjangoMarcaRepository(),
            "logo_repository": DjangoLogoRepository(),
            "kpi_repository": DjangoKpiRepository(),
            "historial_repository": DjangoHistorialRepository(),
            "dashboard_repository": DjangoDashboardRepository(),
            "reporte_repository": DjangoReporteRepository(),
        }

    def _configure_use_cases(self):
        """Configura los use cases con inyección de dependencias"""
        # Obtener repositorios
        marca_repo = self._repositories["marca_repository"]
        logo_repo = self._repositories["logo_repository"]
        kpi_repo = self._repositories["kpi_repository"]
        dashboard_repo = self._repositories["dashboard_repository"]

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

    # Métodos para repositorios
    def get_marca_repository(self) -> MarcaGanadoBovinoRepository:
        """Obtiene el repositorio de marcas"""
        return self._repositories["marca_repository"]

    def get_logo_repository(self) -> LogoMarcaBovinaRepository:
        """Obtiene el repositorio de logos"""
        return self._repositories["logo_repository"]

    def get_kpi_repository(self) -> KPIGanadoBovinoRepository:
        """Obtiene el repositorio de KPIs"""
        return self._repositories["kpi_repository"]

    def get_historial_repository(self) -> HistorialEstadoMarcaRepository:
        """Obtiene el repositorio de historial"""
        return self._repositories["historial_repository"]

    def get_dashboard_repository(self) -> DashboardRepository:
        """Obtiene el repositorio de dashboard"""
        return self._repositories["dashboard_repository"]

    def get_reporte_repository(self) -> ReporteRepository:
        """Obtiene el repositorio de reportes"""
        return self._repositories["reporte_repository"]

    def get_all_repositories(self) -> Dict[str, Any]:
        """Obtiene todos los repositorios"""
        return self._repositories.copy()

    # Métodos para use cases
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
        """Obtiene el use case para estadísticas de marcas"""
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
        """Obtiene el use case para estadísticas de logos"""
        return self._use_cases["obtener_estadisticas_logos_use_case"]

    def get_calcular_kpis_use_case(self) -> CalcularKPIsUseCase:
        """Obtiene el use case para calcular KPIs"""
        return self._use_cases["calcular_kpis_use_case"]

    def get_obtener_kpis_use_case(self) -> ObtenerKPIsUseCase:
        """Obtiene el use case para obtener KPIs"""
        return self._use_cases["obtener_kpis_use_case"]

    def get_generar_reporte_kpis_use_case(self) -> GenerarReporteKPIsUseCase:
        """Obtiene el use case para generar reportes de KPIs"""
        return self._use_cases["generar_reporte_kpis_use_case"]

    def get_obtener_dashboard_data_use_case(self) -> ObtenerDashboardDataUseCase:
        """Obtiene el use case para datos del dashboard"""
        return self._use_cases["obtener_dashboard_data_use_case"]

    def get_generar_reporte_dashboard_use_case(self) -> GenerarReporteDashboardUseCase:
        """Obtiene el use case para generar reportes del dashboard"""
        return self._use_cases["generar_reporte_dashboard_use_case"]

    def get_all_use_cases(self) -> Dict[str, Any]:
        """Obtiene todos los use cases"""
        return self._use_cases.copy()


# Instancia global del container
container = Container()


def get_container() -> Container:
    """Obtiene la instancia global del container"""
    return container


# Funciones helper para repositorios
def get_marca_repository() -> MarcaGanadoBovinoRepository:
    """Obtiene el repositorio de marcas desde el container global"""
    return container.get_marca_repository()


def get_logo_repository() -> LogoMarcaBovinaRepository:
    """Obtiene el repositorio de logos desde el container global"""
    return container.get_logo_repository()


def get_kpi_repository() -> KPIGanadoBovinoRepository:
    """Obtiene el repositorio de KPIs desde el container global"""
    return container.get_kpi_repository()


def get_historial_repository() -> HistorialEstadoMarcaRepository:
    """Obtiene el repositorio de historial desde el container global"""
    return container.get_historial_repository()


def get_dashboard_repository() -> DashboardRepository:
    """Obtiene el repositorio de dashboard desde el container global"""
    return container.get_dashboard_repository()


def get_reporte_repository() -> ReporteRepository:
    """Obtiene el repositorio de reportes desde el container global"""
    return container.get_reporte_repository()


# Funciones helper para use cases
def get_crear_marca_use_case() -> CrearMarcaUseCase:
    """Obtiene el use case para crear marcas desde el container global"""
    return container.get_crear_marca_use_case()


def get_obtener_marca_use_case() -> ObtenerMarcaUseCase:
    """Obtiene el use case para obtener marcas desde el container global"""
    return container.get_obtener_marca_use_case()


def get_actualizar_marca_use_case() -> ActualizarMarcaUseCase:
    """Obtiene el use case para actualizar marcas desde el container global"""
    return container.get_actualizar_marca_use_case()


def get_eliminar_marca_use_case() -> EliminarMarcaUseCase:
    """Obtiene el use case para eliminar marcas desde el container global"""
    return container.get_eliminar_marca_use_case()


def get_listar_marcas_use_case() -> ListarMarcasUseCase:
    """Obtiene el use case para listar marcas desde el container global"""
    return container.get_listar_marcas_use_case()


def get_cambiar_estado_marca_use_case() -> CambiarEstadoMarcaUseCase:
    """Obtiene el use case para cambiar estado de marcas desde el container global"""
    return container.get_cambiar_estado_marca_use_case()


def get_obtener_estadisticas_marcas_use_case() -> ObtenerEstadisticasMarcasUseCase:
    """Obtiene el use case para estadísticas de marcas desde el container global"""
    return container.get_obtener_estadisticas_marcas_use_case()


def get_generar_logo_use_case() -> GenerarLogoUseCase:
    """Obtiene el use case para generar logos desde el container global"""
    return container.get_generar_logo_use_case()


def get_obtener_logo_use_case() -> ObtenerLogoUseCase:
    """Obtiene el use case para obtener logos desde el container global"""
    return container.get_obtener_logo_use_case()


def get_listar_logos_use_case() -> ListarLogosUseCase:
    """Obtiene el use case para listar logos desde el container global"""
    return container.get_listar_logos_use_case()


def get_obtener_estadisticas_logos_use_case() -> ObtenerEstadisticasLogosUseCase:
    """Obtiene el use case para estadísticas de logos desde el container global"""
    return container.get_obtener_estadisticas_logos_use_case()


def get_calcular_kpis_use_case() -> CalcularKPIsUseCase:
    """Obtiene el use case para calcular KPIs desde el container global"""
    return container.get_calcular_kpis_use_case()


def get_obtener_kpis_use_case() -> ObtenerKPIsUseCase:
    """Obtiene el use case para obtener KPIs desde el container global"""
    return container.get_obtener_kpis_use_case()


def get_generar_reporte_kpis_use_case() -> GenerarReporteKPIsUseCase:
    """Obtiene el use case para generar reportes de KPIs desde el container global"""
    return container.get_generar_reporte_kpis_use_case()


def get_obtener_dashboard_data_use_case() -> ObtenerDashboardDataUseCase:
    """Obtiene el use case para datos del dashboard desde el container global"""
    return container.get_obtener_dashboard_data_use_case()


def get_generar_reporte_dashboard_use_case() -> GenerarReporteDashboardUseCase:
    """Obtiene el use case para generar reportes del dashboard desde el container global"""
    return container.get_generar_reporte_dashboard_use_case()
