"""
Controller para reportes ejecutivos
Responsabilidad única: Reportes para alta dirección
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class ReporteEjecutivoController:
    """Controller para reportes ejecutivos"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de reportes ejecutivos
        self.generar_reporte_mensual_use_case = (
            self.container.get_generar_reporte_mensual_use_case()
        )
        self.generar_reporte_anual_use_case = (
            self.container.get_generar_reporte_anual_use_case()
        )


# ============================================================================
# ENDPOINTS DE REPORTES EJECUTIVOS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporte_ejecutivo_mensual(request):
    """Reporte ejecutivo mensual para alta dirección"""
    try:
        controller = ReporteEjecutivoController()

        # Obtener parámetros
        mes = int(request.query_params.get("mes", 0))
        año = int(request.query_params.get("año", 0))

        if not mes or not año:
            return Response(
                {"error": "Parámetros mes y año son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte mensual
        reporte = controller.generar_reporte_mensual_use_case.execute(
            {
                "mes": mes,
                "año": año,
                "incluir_alertas": True,
                "incluir_recomendaciones": True,
            }
        )

        return Response(
            {
                "periodo": f"{mes}/{año}",
                "fecha_generacion": reporte.fecha_generacion,
                "resumen_ejecutivo": {
                    "total_marcas": reporte.total_marcas,
                    "total_cabezas": reporte.total_cabezas,
                    "ingresos_totales": reporte.ingresos_totales,
                    "tasa_aprobacion": reporte.tasa_aprobacion,
                    "crecimiento_vs_mes_anterior": reporte.crecimiento_vs_mes_anterior,
                },
                "metricas_calidad": reporte.metricas_calidad,
                "departamento_lider": reporte.departamento_lider,
                "comparacion_interanual": reporte.comparacion_interanual,
                "eficiencia_mensual": reporte.eficiencia_mensual,
                "proyecciones": reporte.proyecciones,
                "conclusiones": reporte.conclusiones,
                "recomendaciones_estrategicas": reporte.recomendaciones_estrategicas,
                "alertas_ejecutivas": reporte.alertas_ejecutivas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte ejecutivo mensual: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporte_anual(request):
    """Reporte ejecutivo anual para alta dirección"""
    try:
        controller = ReporteEjecutivoController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        if not año:
            return Response(
                {"error": "Parámetro año es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte anual
        reporte = controller.generar_reporte_anual_use_case.execute(
            {"año": año, "incluir_analisis": True, "incluir_proyecciones": True}
        )

        return Response(
            {
                "año": año,
                "fecha_generacion": reporte.fecha_generacion,
                "resumen_anual": {
                    "total_marcas": reporte.total_marcas,
                    "total_cabezas": reporte.total_cabezas,
                    "ingresos_totales": reporte.ingresos_totales,
                    "crecimiento_anual": reporte.crecimiento_anual,
                    "eficiencia_promedio": reporte.eficiencia_promedio,
                },
                "analisis_mensual": reporte.analisis_mensual,
                "comparacion_interanual": reporte.comparacion_interanual,
                "eficiencia_anual": reporte.eficiencia_anual,
                "proyecciones_anuales": reporte.proyecciones_anuales,
                "conclusiones_anuales": reporte.conclusiones_anuales,
                "recomendaciones_estrategicas": reporte.recomendaciones_estrategicas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte ejecutivo anual: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
