# business_intelligence/views/logo_bovino_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta

from ..models import LogoMarcaBovina, MarcaGanadoBovino
from ..serializers import LogoMarcaBovinaSerializer, RendimientoModelosIASerializer
from ..services import DataGenerationService


class LogoMarcaBovinaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de logos de marcas bovinas

    Funcionalidades:
    - CRUD de logos
    - Análisis de rendimiento por modelo IA
    - Regeneración de logos fallidos
    - Estadísticas de calidad
    """

    queryset = LogoMarcaBovina.objects.all()
    serializer_class = LogoMarcaBovinaSerializer

    def get_queryset(self):
        """Queryset con filtros"""
        queryset = LogoMarcaBovina.objects.select_related("marca")

        # Filtros
        modelo_ia = self.request.query_params.get("modelo_ia")
        if modelo_ia:
            queryset = queryset.filter(modelo_ia_usado=modelo_ia)

        exito = self.request.query_params.get("exito")
        if exito is not None:
            queryset = queryset.filter(exito=exito.lower() == "true")

        calidad = self.request.query_params.get("calidad")
        if calidad:
            queryset = queryset.filter(calidad_logo=calidad)

        # Filtro por marca
        marca_numero = self.request.query_params.get("marca_numero")
        if marca_numero:
            queryset = queryset.filter(marca__numero_marca=marca_numero)

        # Filtro por raza de la marca
        raza_bovino = self.request.query_params.get("raza_bovino")
        if raza_bovino:
            queryset = queryset.filter(marca__raza_bovino=raza_bovino)

        # Filtro por departamento
        departamento = self.request.query_params.get("departamento")
        if departamento:
            queryset = queryset.filter(marca__departamento=departamento)

        return queryset.order_by("-fecha_generacion")

    @action(detail=False, methods=["get"])
    def logos_pendientes(self, request):
        """Marcas que necesitan generación de logos"""
        # Marcas aprobadas sin logos o con logos fallidos
        marcas_sin_logos = (
            MarcaGanadoBovino.objects.filter(estado="APROBADO")
            .exclude(logos__exito=True)
            .distinct()
        )

        pendientes_data = []
        for marca in marcas_sin_logos:
            logos_fallidos = marca.logos.filter(exito=False).count()
            pendientes_data.append(
                {
                    "marca_id": marca.id,
                    "numero_marca": marca.numero_marca,
                    "nombre_productor": marca.nombre_productor,
                    "raza_bovino": marca.get_raza_bovino_display(),
                    "proposito_ganado": marca.get_proposito_ganado_display(),
                    "cantidad_cabezas": marca.cantidad_cabezas,
                    "logos_fallidos": logos_fallidos,
                    "necesita_logo": marca.logos.filter(exito=True).count() == 0,
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

    @action(detail=False, methods=["get"])
    def logos_fallidos(self, request):
        """Logos que fallaron en la generación"""
        fallidos = self.get_queryset().filter(exito=False).order_by("-fecha_generacion")

        # Agrupar por modelo IA para análisis
        por_modelo = (
            fallidos.values("modelo_ia_usado")
            .annotate(
                total_fallidos=Count("id"),
                tiempo_promedio=Avg("tiempo_generacion_segundos"),
            )
            .order_by("-total_fallidos")
        )

        serializer = self.get_serializer(fallidos, many=True)

        return Response(
            {
                "count": fallidos.count(),
                "logos_fallidos": serializer.data,
                "analisis_por_modelo": list(por_modelo),
                "recomendaciones": self._generar_recomendaciones_fallidos(por_modelo),
            }
        )

    def _generar_recomendaciones_fallidos(self, estadisticas_modelo):
        """Genera recomendaciones basadas en fallos por modelo"""
        recomendaciones = []

        for modelo in estadisticas_modelo:
            if modelo["total_fallidos"] > 5:
                if modelo["tiempo_promedio"] > 60:
                    recomendaciones.append(
                        f"Modelo {modelo['modelo_ia_usado']}: Alto tiempo de generación ({modelo['tiempo_promedio']:.1f}s). "
                        "Considerar optimizar prompts o cambiar modelo."
                    )
                else:
                    recomendaciones.append(
                        f"Modelo {modelo['modelo_ia_usado']}: {modelo['total_fallidos']} fallos recientes. "
                        "Revisar configuración del modelo."
                    )

        return recomendaciones

    @action(detail=False, methods=["get"])
    def logos_por_calidad(self, request):
        """Distribución de logos por calidad"""
        distribucion = (
            self.get_queryset()
            .values("calidad_logo")
            .annotate(
                total=Count("id"), tiempo_promedio=Avg("tiempo_generacion_segundos")
            )
            .order_by("-total")
        )

        # Porcentajes
        total_logos = self.get_queryset().count()
        for item in distribucion:
            item["porcentaje"] = round(
                (item["total"] / total_logos * 100) if total_logos > 0 else 0, 2
            )
            item["calidad_display"] = dict(
                LogoMarcaBovina._meta.get_field("calidad_logo").choices
            ).get(item["calidad_logo"], item["calidad_logo"])

        return Response(
            {
                "total_logos": total_logos,
                "distribucion_calidad": list(distribucion),
                "metricas_calidad": {
                    "alta_calidad_porcentaje": next(
                        (
                            item["porcentaje"]
                            for item in distribucion
                            if item["calidad_logo"] == "ALTA"
                        ),
                        0,
                    ),
                    "necesita_mejora": total_logos
                    - self.get_queryset().filter(calidad_logo="ALTA").count(),
                },
            }
        )

    @action(detail=False, methods=["get"])
    def rendimiento_modelos_ia(self, request):
        """Análisis completo del rendimiento de modelos IA"""
        modelos_stats = (
            self.get_queryset()
            .values("modelo_ia_usado")
            .annotate(
                total_generados=Count("id"),
                exitosos=Count("id", filter=Q(exito=True)),
                fallidos=Count("id", filter=Q(exito=False)),
                tiempo_promedio_generacion=Avg("tiempo_generacion_segundos"),
                logos_alta_calidad=Count("id", filter=Q(calidad_logo="ALTA")),
                logos_media_calidad=Count("id", filter=Q(calidad_logo="MEDIA")),
                logos_baja_calidad=Count("id", filter=Q(calidad_logo="BAJA")),
            )
            .order_by("-total_generados")
        )

        # Calcular métricas adicionales
        for modelo in modelos_stats:
            modelo["tasa_exito"] = round(
                (
                    (modelo["exitosos"] / modelo["total_generados"] * 100)
                    if modelo["total_generados"] > 0
                    else 0
                ),
                2,
            )
            modelo["porcentaje_alta_calidad"] = round(
                (
                    (modelo["logos_alta_calidad"] / modelo["total_generados"] * 100)
                    if modelo["total_generados"] > 0
                    else 0
                ),
                2,
            )
            modelo["tiempo_promedio_formateado"] = (
                f"{modelo['tiempo_promedio_generacion']:.1f}s"
            )
            modelo["modelo_display"] = dict(
                LogoMarcaBovina._meta.get_field("modelo_ia_usado").choices
            ).get(modelo["modelo_ia_usado"], modelo["modelo_ia_usado"])

        serializer = RendimientoModelosIASerializer(modelos_stats, many=True)

        # Ranking de modelos
        ranking = sorted(
            modelos_stats,
            key=lambda x: (x["tasa_exito"], x["porcentaje_alta_calidad"]),
            reverse=True,
        )

        return Response(
            {
                "modelos_rendimiento": serializer.data,
                "ranking_modelos": [
                    {
                        "posicion": idx + 1,
                        "modelo": modelo["modelo_ia_usado"],
                        "score_general": round(
                            (modelo["tasa_exito"] + modelo["porcentaje_alta_calidad"])
                            / 2,
                            2,
                        ),
                    }
                    for idx, modelo in enumerate(ranking)
                ],
                "recomendacion_modelo": (
                    ranking[0]["modelo_ia_usado"] if ranking else None
                ),
            }
        )

    @action(detail=True, methods=["post"])
    def regenerar_logo(self, request, pk=None):
        """Regenerar un logo específico"""
        logo = self.get_object()

        # Verificar que el logo anterior haya fallado
        if logo.exito:
            return Response(
                {"error": "Solo se pueden regenerar logos que fallaron"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parámetros para regeneración
        nuevo_modelo = request.data.get("modelo_ia", logo.modelo_ia_usado)
        nuevo_prompt = request.data.get("prompt_personalizado")

        try:
            # Generar nuevo prompt si no se proporciona uno personalizado
            if not nuevo_prompt:
                prompts_disponibles = DataGenerationService.generar_prompt_logo_bovino(
                    logo.marca
                )
                nuevo_prompt = prompts_disponibles[0]  # Usar el primer prompt

            # Simular regeneración (aquí iría la llamada real a la IA)
            import random

            tiempo_generacion = random.randint(15, 60)
            exito_regeneracion = random.random() > 0.3  # 70% de probabilidad de éxito

            # Crear nuevo logo
            nuevo_logo = LogoMarcaBovina.objects.create(
                marca=logo.marca,
                url_logo=f"https://logos.ganaderia.bo/bovino/{logo.marca.numero_marca}_{nuevo_modelo.lower().replace('-', '_')}_v2.png",
                exito=exito_regeneracion,
                tiempo_generacion_segundos=tiempo_generacion,
                modelo_ia_usado=nuevo_modelo,
                prompt_usado=nuevo_prompt,
                calidad_logo="ALTA" if exito_regeneracion else "BAJA",
            )

            serializer = self.get_serializer(nuevo_logo)

            return Response(
                {
                    "mensaje": (
                        "Logo regenerado exitosamente"
                        if exito_regeneracion
                        else "Regeneración falló, pero se creó registro"
                    ),
                    "logo_original": logo.id,
                    "logo_nuevo": serializer.data,
                    "mejora": exito_regeneracion and not logo.exito,
                }
            )

        except Exception as e:
            return Response(
                {"error": f"Error regenerando logo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"])
    def generar_logos_masivo(self, request):
        """Generación masiva de logos para marcas sin logos"""
        modelo_preferido = request.data.get("modelo_ia", "DALL-E-3")
        limite_marcas = request.data.get("limite", 10)

        # Obtener marcas que necesitan logos
        marcas_sin_logos = (
            MarcaGanadoBovino.objects.filter(estado="APROBADO")
            .exclude(logos__exito=True)
            .distinct()[:limite_marcas]
        )

        resultados = []
        errores = []

        for marca in marcas_sin_logos:
            try:
                # Generar prompt específico para la marca
                prompts = DataGenerationService.generar_prompt_logo_bovino(marca)
                prompt_seleccionado = prompts[0]

                # Simular generación
                import random

                tiempo_generacion = random.randint(20, 80)
                exito = random.random() > 0.2  # 80% de probabilidad de éxito

                logo = LogoMarcaBovina.objects.create(
                    marca=marca,
                    url_logo=f"https://logos.ganaderia.bo/bovino/{marca.numero_marca}_{modelo_preferido.lower().replace('-', '_')}.png",
                    exito=exito,
                    tiempo_generacion_segundos=tiempo_generacion,
                    modelo_ia_usado=modelo_preferido,
                    prompt_usado=prompt_seleccionado,
                    calidad_logo=(
                        random.choice(["ALTA", "MEDIA", "BAJA"]) if exito else "BAJA"
                    ),
                )

                resultados.append(
                    {
                        "marca_numero": marca.numero_marca,
                        "logo_id": logo.id,
                        "exito": exito,
                        "tiempo_generacion": tiempo_generacion,
                    }
                )

            except Exception as e:
                errores.append({"marca_numero": marca.numero_marca, "error": str(e)})

        return Response(
            {
                "mensaje": f"Generación masiva completada: {len(resultados)} logos procesados",
                "resultados": resultados,
                "errores": errores,
                "estadisticas": {
                    "total_procesadas": len(resultados),
                    "exitosos": len([r for r in resultados if r["exito"]]),
                    "fallidos": len([r for r in resultados if not r["exito"]]),
                    "tiempo_promedio": (
                        round(
                            sum(r["tiempo_generacion"] for r in resultados)
                            / len(resultados),
                            2,
                        )
                        if resultados
                        else 0
                    ),
                },
            }
        )

    @action(detail=False, methods=["post"])
    def evaluar_calidad_masiva(self, request):
        """Evaluación masiva de calidad de logos"""
        logo_ids = request.data.get("logo_ids", [])
        nueva_calidad = request.data.get("calidad", "MEDIA")

        if nueva_calidad not in ["ALTA", "MEDIA", "BAJA"]:
            return Response(
                {"error": "Calidad debe ser ALTA, MEDIA o BAJA"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logos = LogoMarcaBovina.objects.filter(id__in=logo_ids)

        actualizados = []
        for logo in logos:
            calidad_anterior = logo.calidad_logo
            logo.calidad_logo = nueva_calidad
            logo.save()

            actualizados.append(
                {
                    "logo_id": logo.id,
                    "marca_numero": logo.marca.numero_marca,
                    "calidad_anterior": calidad_anterior,
                    "calidad_nueva": nueva_calidad,
                }
            )

        return Response(
            {
                "mensaje": f"{len(actualizados)} logos actualizados",
                "actualizados": actualizados,
                "nueva_distribucion": self._obtener_distribucion_calidad(),
            }
        )

    def _obtener_distribucion_calidad(self):
        """Obtiene la distribución actual de calidad de logos"""
        total = LogoMarcaBovina.objects.count()
        if total == 0:
            return {"alta": 0, "media": 0, "baja": 0}

        distribucion = LogoMarcaBovina.objects.values("calidad_logo").annotate(
            total=Count("id")
        )

        resultado = {"alta": 0, "media": 0, "baja": 0}
        for item in distribucion:
            if item["calidad_logo"] == "ALTA":
                resultado["alta"] = round((item["total"] / total) * 100, 2)
            elif item["calidad_logo"] == "MEDIA":
                resultado["media"] = round((item["total"] / total) * 100, 2)
            elif item["calidad_logo"] == "BAJA":
                resultado["baja"] = round((item["total"] / total) * 100, 2)

        return resultado

    @action(detail=False, methods=["get"])
    def analisis_prompts(self, request):
        """Análisis de efectividad de prompts"""
        # Agrupar por palabras clave en prompts
        logos_con_prompts = (
            self.get_queryset()
            .exclude(prompt_usado__isnull=True)
            .exclude(prompt_usado="")
        )

        analisis = {
            "prompts_mas_exitosos": [],
            "palabras_clave_efectivas": [],
            "tiempo_promedio_por_tipo_prompt": [],
        }

        # Análisis de prompts más exitosos
        prompts_stats = {}
        for logo in logos_con_prompts:
            prompt_hash = hash(logo.prompt_usado)
            if prompt_hash not in prompts_stats:
                prompts_stats[prompt_hash] = {
                    "prompt": (
                        logo.prompt_usado[:100] + "..."
                        if len(logo.prompt_usado) > 100
                        else logo.prompt_usado
                    ),
                    "total": 0,
                    "exitosos": 0,
                    "tiempo_promedio": 0,
                    "tiempos": [],
                }

            prompts_stats[prompt_hash]["total"] += 1
            prompts_stats[prompt_hash]["tiempos"].append(
                logo.tiempo_generacion_segundos
            )
            if logo.exito:
                prompts_stats[prompt_hash]["exitosos"] += 1

        # Calcular métricas finales
        for prompt_data in prompts_stats.values():
            prompt_data["tasa_exito"] = round(
                (prompt_data["exitosos"] / prompt_data["total"]) * 100, 2
            )
            prompt_data["tiempo_promedio"] = round(
                sum(prompt_data["tiempos"]) / len(prompt_data["tiempos"]), 2
            )
            del prompt_data["tiempos"]  # Limpiar datos temporales

        # Top 5 prompts más exitosos
        analisis["prompts_mas_exitosos"] = sorted(
            prompts_stats.values(),
            key=lambda x: (x["tasa_exito"], -x["tiempo_promedio"]),
            reverse=True,
        )[:5]

        return Response(analisis)
