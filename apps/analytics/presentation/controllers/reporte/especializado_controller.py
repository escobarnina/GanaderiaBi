"""
Controller para reportes especializados
Responsabilidad única: Reportes específicos por dominio
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class ReporteEspecializadoController:
    """Controller para reportes especializados"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de reportes especializados
        self.generar_reporte_productor_use_case = (
            self.container.get_generar_reporte_productor_use_case()
        )
        self.generar_reporte_impacto_economico_use_case = (
            self.container.get_generar_reporte_impacto_economico_use_case()
        )
        self.generar_reporte_innovacion_tecnologica_use_case = (
            self.container.get_generar_reporte_innovacion_tecnologica_use_case()
        )
        self.generar_reporte_sostenibilidad_use_case = (
            self.container.get_generar_reporte_sostenibilidad_use_case()
        )


# ============================================================================
# ENDPOINTS DE REPORTES ESPECIALIZADOS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporte_productor_individual(request):
    """Reporte individual para productor específico"""
    try:
        controller = ReporteEspecializadoController()

        # Obtener parámetros
        productor_id = request.query_params.get("productor_id", "")
        periodo_dias = int(request.query_params.get("periodo_dias", 365))

        if not productor_id:
            return Response(
                {"error": "Parámetro productor_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte de productor
        reporte = controller.generar_reporte_productor_use_case.execute(
            {
                "productor_id": productor_id,
                "periodo_dias": periodo_dias,
                "incluir_benchmarking": True,
                "incluir_recomendaciones": True,
            }
        )

        return Response(
            {
                "productor": {
                    "id": productor_id,
                    "nombre": reporte.nombre_productor,
                    "departamento": reporte.departamento,
                },
                "periodo_analisis": f"{periodo_dias} días",
                "metricas_personales": {
                    "total_marcas": reporte.total_marcas,
                    "total_cabezas": reporte.total_cabezas,
                    "ingresos_totales": reporte.ingresos_totales,
                    "tasa_aprobacion": reporte.tasa_aprobacion,
                    "crecimiento_periodo": reporte.crecimiento_periodo,
                },
                "benchmarking": {
                    "posicion_percentil": reporte.posicion_percentil,
                    "clasificacion": reporte.clasificacion,
                    "comparacion_sector": reporte.comparacion_sector,
                    "fortalezas_relativas": reporte.fortalezas_relativas,
                    "areas_mejora": reporte.areas_mejora,
                },
                "tendencias_temporales": reporte.tendencias_temporales,
                "recomendaciones_personalizadas": reporte.recomendaciones_personalizadas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte de productor: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporte_impacto_economico(request):
    """Reporte de impacto económico del sector ganadero"""
    try:
        controller = ReporteEspecializadoController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        if not año:
            return Response(
                {"error": "Parámetro año es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte de impacto económico
        reporte = controller.generar_reporte_impacto_economico_use_case.execute(
            {"año": año, "incluir_analisis": True, "incluir_proyecciones": True}
        )

        return Response(
            {
                "año": año,
                "impacto_economico": {
                    "valor_ganado_total": reporte.valor_ganado_total,
                    "contribucion_pib": reporte.contribucion_pib,
                    "empleos_generados": reporte.empleos_generados,
                    "ingresos_fiscales": reporte.ingresos_fiscales,
                },
                "analisis_por_proposito": reporte.analisis_por_proposito,
                "comparacion_sectorial": reporte.comparacion_sectorial,
                "proyecciones_economicas": reporte.proyecciones_economicas,
                "recomendaciones_politicas": reporte.recomendaciones_politicas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte de impacto económico: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporte_innovacion_tecnologica(request):
    """Reporte de innovación tecnológica en el sector"""
    try:
        controller = ReporteEspecializadoController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        if not año:
            return Response(
                {"error": "Parámetro año es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte de innovación tecnológica
        reporte = controller.generar_reporte_innovacion_tecnologica_use_case.execute(
            {"año": año, "incluir_analisis": True, "incluir_evaluacion": True}
        )

        return Response(
            {
                "año": año,
                "adopcion_tecnologica": {
                    "tasa_adopcion_ia": reporte.tasa_adopcion_ia,
                    "tiempo_promedio_generacion": reporte.tiempo_promedio_generacion,
                    "calidad_generacion": reporte.calidad_generacion,
                    "satisfaccion_usuario": reporte.satisfaccion_usuario,
                },
                "tendencias_adopcion": reporte.tendencias_adopcion,
                "evaluacion_modelo_ia": reporte.evaluacion_modelo_ia,
                "impacto_operacional": reporte.impacto_operacional,
                "recomendaciones_tecnologicas": reporte.recomendaciones_tecnologicas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte de innovación tecnológica: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporte_sostenibilidad_sectorial(request):
    """Reporte de sostenibilidad del sector ganadero"""
    try:
        controller = ReporteEspecializadoController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        if not año:
            return Response(
                {"error": "Parámetro año es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte de sostenibilidad
        reporte = controller.generar_reporte_sostenibilidad_use_case.execute(
            {"año": año, "incluir_analisis": True, "incluir_evaluacion": True}
        )

        return Response(
            {
                "año": año,
                "indicadores_sostenibilidad": {
                    "score_economica": reporte.score_economica,
                    "score_social": reporte.score_social,
                    "score_ambiental": reporte.score_ambiental,
                    "score_general": reporte.score_general,
                },
                "analisis_ambiental": {
                    "huella_carbono": reporte.huella_carbono,
                    "diversidad_genetica": reporte.diversidad_genetica,
                    "practicas_sostenibles": reporte.practicas_sostenibles,
                },
                "analisis_social": {
                    "inclusion_productores": reporte.inclusion_productores,
                    "equidad_geografica": reporte.equidad_geografica,
                    "desarrollo_rural": reporte.desarrollo_rural,
                },
                "nivel_maduracion": reporte.nivel_maduracion,
                "recomendaciones_sostenibilidad": reporte.recomendaciones_sostenibilidad,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte de sostenibilidad: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
