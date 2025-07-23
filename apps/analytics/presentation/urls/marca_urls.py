"""
URLs específicas para marcas de ganado bovino
"""

from django.urls import path
from ..controllers.marca import (
    # CRUD básicos
    listar_marcas,
    obtener_marca,
    crear_marca,
    actualizar_marca,
    eliminar_marca,
    # Operaciones de estado
    aprobar_marca,
    rechazar_marca,
    # Consultas especializadas
    marcas_pendientes,
    marcas_por_procesar,
    marcas_procesadas_hoy,
    # Estadísticas
    estadisticas_por_raza,
    estadisticas_por_departamento,
    # Procesamiento masivo
    procesamiento_masivo,
)

app_name = "marca"

urlpatterns = [
    # ============================================================================
    # ENDPOINTS CRUD BÁSICOS
    # ============================================================================
    path("", listar_marcas, name="listar_marcas"),
    path("<int:marca_id>/", obtener_marca, name="obtener_marca"),
    path("crear/", crear_marca, name="crear_marca"),
    path("<int:marca_id>/actualizar/", actualizar_marca, name="actualizar_marca"),
    path("<int:marca_id>/eliminar/", eliminar_marca, name="eliminar_marca"),
    # ============================================================================
    # ENDPOINTS DE ESTADO
    # ============================================================================
    path("<int:marca_id>/aprobar/", aprobar_marca, name="aprobar_marca"),
    path("<int:marca_id>/rechazar/", rechazar_marca, name="rechazar_marca"),
    # ============================================================================
    # ENDPOINTS DE CONSULTA ESPECIALIZADA
    # ============================================================================
    path("pendientes/", marcas_pendientes, name="marcas_pendientes"),
    path("por-procesar/", marcas_por_procesar, name="marcas_por_procesar"),
    path("procesadas-hoy/", marcas_procesadas_hoy, name="marcas_procesadas_hoy"),
    # ============================================================================
    # ENDPOINTS DE ESTADÍSTICAS
    # ============================================================================
    path("estadisticas/por-raza/", estadisticas_por_raza, name="estadisticas_por_raza"),
    path(
        "estadisticas/por-departamento/",
        estadisticas_por_departamento,
        name="estadisticas_por_departamento",
    ),
    # ============================================================================
    # ENDPOINTS DE PROCESAMIENTO MASIVO
    # ============================================================================
    path("procesamiento-masivo/", procesamiento_masivo, name="procesamiento_masivo"),
]
