"""
Controllers de Clean Architecture para la aplicación de analytics
Implementan la lógica de presentación usando use cases
"""

# Importaciones básicas para evitar errores
try:
    from .marca import (
        listar_marcas,
        obtener_marca,
        crear_marca,
        actualizar_marca,
        eliminar_marca,
    )
except ImportError:
    # Placeholder functions si hay errores
    def listar_marcas(request):
        pass

    def obtener_marca(request, id):
        pass

    def crear_marca(request):
        pass

    def actualizar_marca(request, id):
        pass

    def eliminar_marca(request, id):
        pass


try:
    from .logo import (
        listar_logos,
        obtener_logo,
        generar_logo,
    )
except ImportError:

    def listar_logos(request):
        pass

    def obtener_logo(request, id):
        pass

    def generar_logo(request):
        pass


try:
    from .kpi import (
        listar_kpis,
        obtener_kpi,
        calcular_kpis,
    )
except ImportError:

    def listar_kpis(request):
        pass

    def obtener_kpi(request, id):
        pass

    def calcular_kpis(request):
        pass


try:
    from .dashboard import (
        kpis_principales,
        metricas_tiempo_real,
    )
except ImportError:

    def kpis_principales(request):
        pass

    def metricas_tiempo_real(request):
        pass


try:
    from .historial import (
        listar_historial,
        obtener_historial,
    )
except ImportError:

    def listar_historial(request):
        pass

    def obtener_historial(request, id):
        pass


try:
    from .reporte import (
        reporte_ejecutivo_mensual,
        reporte_anual,
    )
except ImportError:

    def reporte_ejecutivo_mensual(request):
        pass

    def reporte_anual(request):
        pass


__all__ = [
    # Marca Controllers
    "listar_marcas",
    "obtener_marca",
    "crear_marca",
    "actualizar_marca",
    "eliminar_marca",
    # Logo Controllers
    "listar_logos",
    "obtener_logo",
    "generar_logo",
    # KPI Controllers
    "listar_kpis",
    "obtener_kpi",
    "calcular_kpis",
    # Dashboard Controllers
    "kpis_principales",
    "metricas_tiempo_real",
    # Historial Controllers
    "listar_historial",
    "obtener_historial",
    # Reporte Controllers
    "reporte_ejecutivo_mensual",
    "reporte_anual",
]
