"""
Controllers de Clean Architecture para la aplicación de analytics
Implementan la lógica de presentación usando use cases
"""

from .marca import (
    listar_marcas,
    obtener_marca,
    crear_marca,
    actualizar_marca,
    eliminar_marca,
    aprobar_marca,
    rechazar_marca,
    marcas_pendientes,
    marcas_por_procesar,
    marcas_procesadas_hoy,
    estadisticas_por_raza,
    estadisticas_por_departamento,
    procesamiento_masivo,
)

from .logo import (
    listar_logos,
    obtener_logo,
    generar_logo,
    logos_pendientes,
    logos_fallidos,
    logos_por_calidad,
    evaluar_calidad_masiva,
    rendimiento_modelos_ia,
    analisis_prompts,
    regenerar_logo,
    generar_logos_masivo,
)

from .kpi import (
    listar_kpis,
    obtener_kpi,
    calcular_kpis,
    ultimos_12_meses,
    kpis_actuales,
    comparativa_trimestral,
    analisis_estacional,
)

from .dashboard import (
    kpis_principales,
    metricas_tiempo_real,
    tendencias_mensuales,
    analisis_tendencias,
    resumen_ejecutivo,
    generar_reporte_ejecutivo,
    metricas_eficiencia_regional,
)
from .historial_controller import HistorialController
from .reporte_controller import ReporteController

__all__ = [
    # Marca Controllers
    "listar_marcas",
    "obtener_marca",
    "crear_marca",
    "actualizar_marca",
    "eliminar_marca",
    "aprobar_marca",
    "rechazar_marca",
    "marcas_pendientes",
    "marcas_por_procesar",
    "marcas_procesadas_hoy",
    "estadisticas_por_raza",
    "estadisticas_por_departamento",
    "procesamiento_masivo",
    # Logo Controllers
    "listar_logos",
    "obtener_logo",
    "generar_logo",
    "logos_pendientes",
    "logos_fallidos",
    "logos_por_calidad",
    "evaluar_calidad_masiva",
    "rendimiento_modelos_ia",
    "analisis_prompts",
    "regenerar_logo",
    "generar_logos_masivo",
    # KPI Controllers
    "listar_kpis",
    "obtener_kpi",
    "calcular_kpis",
    "ultimos_12_meses",
    "kpis_actuales",
    "comparativa_trimestral",
    "analisis_estacional",
    # Dashboard Controllers
    "kpis_principales",
    "metricas_tiempo_real",
    "tendencias_mensuales",
    "analisis_tendencias",
    "resumen_ejecutivo",
    "generar_reporte_ejecutivo",
    "metricas_eficiencia_regional",
    # Otros Controllers (pendientes)
    "HistorialController",
    "ReporteController",
]
