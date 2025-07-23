"""
Container para configuración de repositorios
Responsabilidad única: Configurar e inyectar repositorios
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

from apps.analytics.infrastructure.repositories.marca_repository import (
    DjangoMarcaRepository,
)
from apps.analytics.infrastructure.repositories.logo_repository import (
    DjangoLogoRepository,
)
from apps.analytics.infrastructure.repositories.kpi_repository import (
    DjangoKpiRepository,
)
from apps.analytics.infrastructure.repositories.historial_repository import (
    DjangoHistorialRepository,
)
from apps.analytics.infrastructure.repositories.dashboard_repository import (
    DjangoDashboardRepository,
)
from apps.analytics.infrastructure.repositories.reporte_repository import (
    DjangoReporteRepository,
)


class RepositoriesContainer:
    """Container específico para repositorios"""

    def __init__(self):
        self._repositories: Dict[str, Any] = {}
        self._configure_repositories()

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
