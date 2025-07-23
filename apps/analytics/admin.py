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
from .presentation.admin import (
    MarcaGanadoBovinoAdmin,
    LogoMarcaBovinaAdmin,
    KPIGanadoBovinoAdmin,
    HistorialEstadoMarcaAdmin,
    DashboardDataAdmin,
    ReporteDataAdmin,
)

# Registrar los modelos con sus respectivos admins
admin.site.register(MarcaGanadoBovinoModel, MarcaGanadoBovinoAdmin)
admin.site.register(LogoMarcaBovinaModel, LogoMarcaBovinaAdmin)
admin.site.register(KPIGanadoBovinoModel, KPIGanadoBovinoAdmin)
admin.site.register(HistorialEstadoMarcaModel, HistorialEstadoMarcaAdmin)
admin.site.register(DashboardDataModel, DashboardDataAdmin)
admin.site.register(ReporteDataModel, ReporteDataAdmin)
