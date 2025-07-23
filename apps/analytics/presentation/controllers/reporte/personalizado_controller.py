"""
Controller para reportes personalizados
Responsabilidad única: Reportes configurables y avanzados
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class ReportePersonalizadoController:
    """Controller para reportes personalizados"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de reportes personalizados
        self.generar_reporte_personalizado_use_case = (
            self.container.get_generar_reporte_personalizado_use_case()
        )
        self.exportar_reporte_excel_use_case = (
            self.container.get_exportar_reporte_excel_use_case()
        )


# ============================================================================
# ENDPOINTS DE REPORTES PERSONALIZADOS
# ============================================================================


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reporte_personalizado(request):
    """Genera reporte personalizado según parámetros"""
    try:
        controller = ReportePersonalizadoController()

        # Validar datos de entrada
        filtros = request.data.get("filtros", {})
        metricas = request.data.get("metricas", [])
        agrupaciones = request.data.get("agrupaciones", [])

        if not filtros or not metricas:
            return Response(
                {"error": "Filtros y métricas son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte personalizado
        reporte = controller.generar_reporte_personalizado_use_case.execute(
            {
                "filtros": filtros,
                "metricas": metricas,
                "agrupaciones": agrupaciones,
                "incluir_graficos": request.data.get("incluir_graficos", True),
                "incluir_resumen": request.data.get("incluir_resumen", True),
            }
        )

        return Response(
            {
                "mensaje": "Reporte personalizado generado exitosamente",
                "reporte": {
                    "datos_principales": reporte.datos_principales,
                    "resumen_estadistico": reporte.resumen_estadistico,
                    "analisis_departamental": reporte.analisis_departamental,
                    "analisis_razas": reporte.analisis_razas,
                    "graficos": reporte.graficos,
                    "insights": reporte.insights,
                },
                "configuracion": {
                    "filtros_aplicados": reporte.filtros_aplicados,
                    "metricas_incluidas": reporte.metricas_incluidas,
                    "agrupaciones_utilizadas": reporte.agrupaciones_utilizadas,
                },
                "metadata": {
                    "fecha_generacion": reporte.fecha_generacion,
                    "tiempo_procesamiento": reporte.tiempo_procesamiento,
                    "registros_procesados": reporte.registros_procesados,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte personalizado: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generar_reporte_personalizado_avanzado(request):
    """Genera reporte personalizado avanzado con análisis complejos"""
    try:
        controller = ReportePersonalizadoController()

        # Validar datos de entrada
        configuracion = request.data.get("configuracion", {})
        filtros_avanzados = request.data.get("filtros_avanzados", {})

        if not configuracion:
            return Response(
                {"error": "Configuración es requerida"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte avanzado
        reporte = controller.generar_reporte_personalizado_use_case.execute(
            {
                "tipo": "avanzado",
                "configuracion": configuracion,
                "filtros_avanzados": filtros_avanzados,
                "incluir_analisis_complejo": True,
                "incluir_limitaciones": True,
            }
        )

        return Response(
            {
                "mensaje": "Reporte personalizado avanzado generado exitosamente",
                "reporte": {
                    "datos_principales": reporte.datos_principales,
                    "resumen_estadistico": reporte.resumen_estadistico,
                    "analisis_departamental": reporte.analisis_departamental,
                    "analisis_razas": reporte.analisis_razas,
                    "analisis_temporal": reporte.analisis_temporal,
                    "insights_avanzados": reporte.insights_avanzados,
                },
                "configuracion": {
                    "configuracion_aplicada": reporte.configuracion_aplicada,
                    "filtros_avanzados": reporte.filtros_avanzados,
                    "limitaciones_metodologicas": reporte.limitaciones_metodologicas,
                },
                "metadata": {
                    "fecha_generacion": reporte.fecha_generacion,
                    "tiempo_procesamiento": reporte.tiempo_procesamiento,
                    "registros_procesados": reporte.registros_procesados,
                    "complejidad_analisis": reporte.complejidad_analisis,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte personalizado avanzado: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exportar_excel(request):
    """Exporta reporte a formato Excel"""
    try:
        controller = ReportePersonalizadoController()

        # Obtener parámetros
        reporte_id = request.query_params.get("reporte_id")
        formato = request.query_params.get("formato", "excel")

        if not reporte_id:
            return Response(
                {"error": "Parámetro reporte_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para exportar
        exportacion = controller.exportar_reporte_excel_use_case.execute(
            {
                "reporte_id": reporte_id,
                "formato": formato,
                "incluir_graficos": request.query_params.get(
                    "incluir_graficos", "true"
                ).lower()
                == "true",
            }
        )

        return Response(
            {
                "mensaje": f"Reporte exportado exitosamente en formato {formato.upper()}",
                "archivo": {
                    "nombre": exportacion.nombre_archivo,
                    "tamaño_bytes": exportacion.tamaño_bytes,
                    "formato": exportacion.formato,
                    "url_descarga": exportacion.url_descarga,
                },
                "metadata": {
                    "fecha_exportacion": exportacion.fecha_exportacion,
                    "tiempo_procesamiento": exportacion.tiempo_procesamiento,
                    "hojas_incluidas": exportacion.hojas_incluidas,
                },
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al exportar reporte: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
