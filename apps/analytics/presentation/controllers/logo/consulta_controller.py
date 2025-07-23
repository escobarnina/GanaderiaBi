"""
Controller para consultas especializadas de logos
Responsabilidad única: Consultas específicas (pendientes, fallidos, etc.)
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.logo_serializers import (
    LogoMarcaBovinaListSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class LogoConsultaController:
    """Controller para consultas especializadas de logos"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de consulta
        self.listar_logos_use_case = self.container.get_listar_logos_use_case()


# ============================================================================
# ENDPOINTS DE CONSULTA ESPECIALIZADA
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logos_pendientes(request):
    """Marcas que necesitan generación de logos"""
    try:
        controller = LogoConsultaController()

        # Filtros específicos para marcas que necesitan logos
        filters = {"necesita_logo": True, "estado_marca": "APROBADO"}

        # Ejecutar use case
        marcas_pendientes = controller.listar_logos_use_case.execute(filters)

        # Procesar datos para respuesta
        pendientes_data = []
        for marca in marcas_pendientes:
            logos_fallidos = sum(1 for logo in marca.logos if not logo.exito)
            pendientes_data.append(
                {
                    "marca_id": marca.id,
                    "numero_marca": marca.numero_marca,
                    "nombre_productor": marca.nombre_productor,
                    "raza_bovino": marca.raza_bovino,
                    "proposito_ganado": marca.proposito_ganado,
                    "cantidad_cabezas": marca.cantidad_cabezas,
                    "logos_fallidos": logos_fallidos,
                    "necesita_logo": sum(1 for logo in marca.logos if logo.exito) == 0,
                }
            )

        return Response(
            {
                "count": len(pendientes_data),
                "marcas_pendientes": pendientes_data,
                "resumen": {
                    "total_sin_logos": len(
                        [m for m in pendientes_data if m["necesita_logo"]]
                    ),
                    "total_con_logos_fallidos": len(
                        [m for m in pendientes_data if not m["necesita_logo"]]
                    ),
                },
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener logos pendientes: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logos_fallidos(request):
    """Logos que fallaron en la generación"""
    try:
        controller = LogoConsultaController()

        # Filtros para logos fallidos
        filters = {"exito": False, "ordering": "-fecha_generacion"}

        # Ejecutar use case
        logos_fallidos = controller.listar_logos_use_case.execute(filters)

        # Serializar respuesta
        serializer = LogoMarcaBovinaListSerializer()
        data = [serializer.to_representation(logo) for logo in logos_fallidos]

        # Análisis por modelo IA
        analisis_por_modelo = {}
        for logo in logos_fallidos:
            modelo = logo.modelo_ia_usado
            if modelo not in analisis_por_modelo:
                analisis_por_modelo[modelo] = {
                    "total_fallidos": 0,
                    "tiempo_promedio": 0,
                    "tiempos": [],
                }

            analisis_por_modelo[modelo]["total_fallidos"] += 1
            analisis_por_modelo[modelo]["tiempos"].append(
                logo.tiempo_generacion_segundos
            )

        # Calcular promedios
        for modelo, stats in analisis_por_modelo.items():
            stats["tiempo_promedio"] = sum(stats["tiempos"]) / len(stats["tiempos"])
            del stats["tiempos"]  # Limpiar datos temporales

        # Generar recomendaciones
        recomendaciones = []
        for modelo, stats in analisis_por_modelo.items():
            if stats["total_fallidos"] > 5:
                if stats["tiempo_promedio"] > 60:
                    recomendaciones.append(
                        f"Modelo {modelo}: Alto tiempo de generación ({stats['tiempo_promedio']:.1f}s). "
                        "Considerar optimizar prompts o cambiar modelo."
                    )
                else:
                    recomendaciones.append(
                        f"Modelo {modelo}: {stats['total_fallidos']} fallos recientes. "
                        "Revisar configuración del modelo."
                    )

        return Response(
            {
                "count": len(data),
                "logos_fallidos": data,
                "analisis_por_modelo": list(analisis_por_modelo.values()),
                "recomendaciones": recomendaciones,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener logos fallidos: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
