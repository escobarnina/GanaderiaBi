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
]
