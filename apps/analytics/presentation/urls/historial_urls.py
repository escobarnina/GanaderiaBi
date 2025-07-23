"""
URLs específicas para Historial de ganado bovino
"""

from django.urls import path
from ..controllers.historial import (
    # CRUD básico
    listar_historial,
    obtener_historial,
    historial_por_marca,
    # Actividad
    actividad_reciente,
    auditoria_usuario,
    # Patrones
    patrones_cambio_estado,
    analisis_flujos_estado,
    # Eficiencia
    eficiencia_evaluadores,
    evaluador_detalle,
    comparativa_evaluadores,
)

app_name = "historial"

urlpatterns = [
    # ============================================================================
    # ENDPOINTS CRUD BÁSICOS
    # ============================================================================
    path("", listar_historial, name="listar_historial"),
    path("<int:historial_id>/", obtener_historial, name="obtener_historial"),
    path("marca/<int:marca_id>/", historial_por_marca, name="historial_por_marca"),
    # ============================================================================
    # ENDPOINTS DE ACTIVIDAD
    # ============================================================================
    path("actividad-reciente/", actividad_reciente, name="actividad_reciente"),
    path("auditoria-usuario/", auditoria_usuario, name="auditoria_usuario"),
    # ============================================================================
    # ENDPOINTS DE PATRONES
    # ============================================================================
    path("patrones-cambio/", patrones_cambio_estado, name="patrones_cambio_estado"),
    path("analisis-flujos/", analisis_flujos_estado, name="analisis_flujos_estado"),
    # ============================================================================
    # ENDPOINTS DE EFICIENCIA
    # ============================================================================
    path(
        "eficiencia-evaluadores/", eficiencia_evaluadores, name="eficiencia_evaluadores"
    ),
    path("evaluador/<str:evaluador_id>/", evaluador_detalle, name="evaluador_detalle"),
    path(
        "comparativa-evaluadores/",
        comparativa_evaluadores,
        name="comparativa_evaluadores",
    ),
]
