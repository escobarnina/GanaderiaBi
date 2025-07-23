"""
Configuración del Admin de Django para la app analytics.
"""

from django.contrib import admin
from .infrastructure.models import (
    MarcaGanadoBovinoModel,
    LogoMarcaBovinaModel,
    KPIGanadoBovinoModel,
    HistorialEstadoMarcaModel,
    DashboardDataModel,
    ReporteDataModel,
)

# Los modelos se registran automáticamente desde presentation/admin/
# para evitar conflictos con los admins específicos
