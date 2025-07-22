# apps/analytics/domain/__init__.py
"""
Capa de dominio - Entidades y reglas de negocio
"""

# Enumeraciones
from .enums import (
    EstadoMarca,
    RazaBovino,
    PropositoGanado,
    Departamento,
    ModeloIA,
    CalidadLogo,
)

# Entidades principales
from .entities.marca_ganado_bovino import MarcaGanadoBovino
from .entities.logo_marca_bovina import LogoMarcaBovina
from .entities.kpi_ganado_bovino import KPIGanadoBovino
from .entities.historial_estado_marca import HistorialEstadoMarca

# Entidades agregadas
from .entities.dashboard_data import DashboardData
from .entities.reporte_data import ReporteData

# Interfaces de repositorios
from .repositories.marca_repository import MarcaGanadoBovinoRepository
from .repositories.logo_repository import LogoMarcaBovinaRepository
from .repositories.kpi_repository import KPIGanadoBovinoRepository
from .repositories.historial_repository import HistorialEstadoMarcaRepository
from .repositories.dashboard_repository import DashboardRepository
from .repositories.reporte_repository import ReporteRepository

__all__ = [
    # Enumeraciones
    "EstadoMarca",
    "RazaBovino",
    "PropositoGanado",
    "Departamento",
    "ModeloIA",
    "CalidadLogo",
    # Entidades principales
    "MarcaGanadoBovino",
    "LogoMarcaBovina",
    "KPIGanadoBovino",
    "HistorialEstadoMarca",
    # Entidades agregadas
    "DashboardData",
    "ReporteData",
    # Interfaces de repositorios
    "MarcaGanadoBovinoRepository",
    "LogoMarcaBovinaRepository",
    "KPIGanadoBovinoRepository",
    "HistorialEstadoMarcaRepository",
    "DashboardRepository",
    "ReporteRepository",
]
