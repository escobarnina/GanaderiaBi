# business_intelligence/views/historial_views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from ..models import HistorialEstadoMarca, MarcaGanadoBovino
from ..serializers import HistorialEstadoMarcaSerializer


class HistorialEstadoMarcaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consulta del historial de estados de marcas

    Proporciona trazabilidad completa de cambios de estado
    con análisis de patrones y auditoría
    """

    queryset = HistorialEstadoMarca.objects.all()
    serializer_class = HistorialEstadoMarcaSerializer

    def get_queryset(self):
        """Queryset con filtros"""
        queryset = HistorialEstadoMarca.objects.select_related("marca")

        # Filtro por marca específica
        marca_id = self.request.query_params.get("marca_id")
        if marca_id:
            queryset = queryset.filter(marca_id=marca_id)

        # Filtro por número de marca
        numero_marca = self.request.query_params.get("numero_marca")
        if numero_marca:
            queryset = queryset.filter(marca__numero_marca__icontains=numero_marca)

        # Filtro por usuario responsable
        usuario = self.request.query_params.get("usuario_responsable")
        if usuario:
            queryset = queryset.filter(usuario_responsable__icontains=usuario)

        # Filtro por tipo de cambio
        estado_nuevo = self.request.query_params.get("estado_nuevo")
        if estado_nuevo:
            queryset = queryset.filter(estado_nuevo=estado_nuevo)

        estado_anterior = self.request.query_params.get("estado_anterior")
        if estado_anterior:
            queryset = queryset.filter(estado_anterior=estado_anterior)

        # Filtro por fecha
        fecha_desde = self.request.query_params.get("fecha_desde")
        if fecha_desde:
            queryset = queryset.filter(fecha_cambio__date__gte=fecha_desde)

        fecha_hasta = self.request.query_params.get("fecha_hasta")
        if fecha_hasta:
            queryset = queryset.filter(fecha_cambio__date__lte=fecha_hasta)

        return queryset.order_by("-fecha_cambio")

    @action(detail=False, methods=["get"])
    def actividad_reciente(self, request):
        """Actividad reciente en el sistema (últimas 24 horas)"""
        hace_24_horas = timezone.now() - timedelta(hours=24)

        actividad_reciente = self.get_queryset().filter(fecha_cambio__gte=hace_24_horas)

        # Agrupar por tipo de actividad
        por_estado = (
            actividad_reciente.values("estado_nuevo")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # Por usuario
        por_usuario = (
            actividad_reciente.values("usuario_responsable")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )

        # Actividad por hora
        actividad_por_hora = {}
        for cambio in actividad_reciente:
            hora = cambio.fecha_cambio.hour
            actividad_por_hora[hora] = actividad_por_hora.get(hora, 0) + 1

        # Marcas con más actividad
        marcas_activas = (
            actividad_reciente.values("marca__numero_marca", "marca__nombre_productor")
            .annotate(cambios=Count("id"))
            .order_by("-cambios")[:5]
        )

        serializer = self.get_serializer(actividad_reciente[:20], many=True)

        return Response(
            {
                "actividad_ultimas_24h": serializer.data,
                "resumen_actividad": {
                    "total_cambios": actividad_reciente.count(),
                    "por_estado": list(por_estado),
                    "usuarios_mas_activos": list(por_usuario),
                    "hora_mas_activa": (
                        max(actividad_por_hora.items(), key=lambda x: x[1])[0]
                        if actividad_por_hora
                        else None
                    ),
                    "marcas_con_mas_cambios": list(marcas_activas),
                },
                "periodo": "24 horas",
                "tendencia_actividad": self._analizar_tendencia_actividad(
                    actividad_reciente
                ),
            }
        )

    def _analizar_tendencia_actividad(self, actividad_reciente):
        """Analiza la tendencia de actividad por horas"""
        # Comparar últimas 12 horas vs anteriores 12 horas
        ahora = timezone.now()
        hace_12_horas = ahora - timedelta(hours=12)
        hace_24_horas = ahora - timedelta(hours=24)

        ultimas_12h = actividad_reciente.filter(fecha_cambio__gte=hace_12_horas).count()
        anteriores_12h = actividad_reciente.filter(
            fecha_cambio__gte=hace_24_horas, fecha_cambio__lt=hace_12_horas
        ).count()

        if anteriores_12h > 0:
            cambio_porcentual = ((ultimas_12h - anteriores_12h) / anteriores_12h) * 100
            if cambio_porcentual > 20:
                tendencia = "incremento_significativo"
            elif cambio_porcentual > 5:
                tendencia = "incremento_moderado"
            elif cambio_porcentual < -20:
                tendencia = "decremento_significativo"
            elif cambio_porcentual < -5:
                tendencia = "decremento_moderado"
            else:
                tendencia = "estable"
        else:
            tendencia = "nueva_actividad" if ultimas_12h > 0 else "sin_actividad"

        return {
            "tendencia": tendencia,
            "ultimas_12h": ultimas_12h,
            "anteriores_12h": anteriores_12h,
            "cambio_porcentual": round(
                (
                    ((ultimas_12h - anteriores_12h) / anteriores_12h * 100)
                    if anteriores_12h > 0
                    else 0
                ),
                2,
            ),
        }

    @action(detail=False, methods=["get"])
    def auditoria_usuario(self, request):
        """Auditoría de actividad por usuario"""
        usuario = request.query_params.get("usuario", "")
        dias = int(request.query_params.get("dias", 30))

        if not usuario:
            return Response({"error": "Parámetro usuario requerido"})

        hace_x_dias = timezone.now() - timedelta(days=dias)

        actividad_usuario = self.get_queryset().filter(
            usuario_responsable=usuario, fecha_cambio__gte=hace_x_dias
        )

        # Estadísticas del usuario
        total_cambios = actividad_usuario.count()
        cambios_por_estado = (
            actividad_usuario.values("estado_nuevo")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # Actividad por día
        actividad_diaria = {}
        for cambio in actividad_usuario:
            fecha_str = cambio.fecha_cambio.strftime("%Y-%m-%d")
            actividad_diaria[fecha_str] = actividad_diaria.get(fecha_str, 0) + 1

        # Marcas más trabajadas
        marcas_trabajadas = (
            actividad_usuario.values("marca__numero_marca", "marca__nombre_productor")
            .annotate(total_cambios=Count("id"))
            .order_by("-total_cambios")[:10]
        )

        # Análisis de eficiencia del usuario
        eficiencia_usuario = self._calcular_eficiencia_usuario(actividad_usuario, dias)

        # Patrones de trabajo
        patrones_trabajo = self._analizar_patrones_trabajo_usuario(actividad_usuario)

        serializer = self.get_serializer(actividad_usuario[:50], many=True)

        return Response(
            {
                "usuario": usuario,
                "periodo_dias": dias,
                "estadisticas": {
                    "total_cambios": total_cambios,
                    "promedio_cambios_por_dia": round(total_cambios / dias, 2),
                    "cambios_por_estado": list(cambios_por_estado),
                    "dias_activos": len(
                        [d for d in actividad_diaria.values() if d > 0]
                    ),
                },
                "eficiencia": eficiencia_usuario,
                "patrones_trabajo": patrones_trabajo,
                "actividad_diaria": actividad_diaria,
                "marcas_mas_trabajadas": list(marcas_trabajadas),
                "historial_detallado": serializer.data,
            }
        )

    def _calcular_eficiencia_usuario(self, actividad_usuario, dias):
        """Calcula métricas de eficiencia del usuario"""
        if not actividad_usuario:
            return {"mensaje": "Sin actividad en el período"}

        # Decisiones finales (aprobado/rechazado)
        decisiones_finales = actividad_usuario.filter(
            estado_nuevo__in=["APROBADO", "RECHAZADO"]
        )

        aprobaciones = decisiones_finales.filter(estado_nuevo="APROBADO").count()
        rechazos = decisiones_finales.filter(estado_nuevo="RECHAZADO").count()
        total_decisiones = aprobaciones + rechazos

        # Tiempo promedio de respuesta
        tiempos_respuesta = []
        for cambio in decisiones_finales:
            if cambio.marca.fecha_registro:
                tiempo_respuesta = (
                    cambio.fecha_cambio - cambio.marca.fecha_registro
                ).total_seconds() / 3600
                if tiempo_respuesta > 0:  # Evitar tiempos negativos
                    tiempos_respuesta.append(tiempo_respuesta)

        tiempo_promedio = (
            round(sum(tiempos_respuesta) / len(tiempos_respuesta), 2)
            if tiempos_respuesta
            else 0
        )

        return {
            "total_decisiones": total_decisiones,
            "tasa_aprobacion": round(
                (aprobaciones / total_decisiones * 100) if total_decisiones > 0 else 0,
                2,
            ),
            "tiempo_promedio_decision_horas": tiempo_promedio,
            "velocidad_evaluacion": (
                "rápida"
                if tiempo_promedio < 24
                else "normal" if tiempo_promedio < 72 else "lenta"
            ),
            "consistencia": self._evaluar_consistencia_usuario(actividad_usuario),
        }

    def _evaluar_consistencia_usuario(self, actividad_usuario):
        """Evalúa la consistencia del usuario en sus decisiones"""
        decisiones = actividad_usuario.filter(
            estado_nuevo__in=["APROBADO", "RECHAZADO"]
        ).order_by("fecha_cambio")

        if len(decisiones) < 10:
            return "insuficientes_datos"

        # Analizar variabilidad en tasa de aprobación por semana
        decisiones_por_semana = {}
        for decision in decisiones:
            semana = decision.fecha_cambio.strftime("%Y-%W")
            if semana not in decisiones_por_semana:
                decisiones_por_semana[semana] = {"aprobado": 0, "rechazado": 0}

            if decision.estado_nuevo == "APROBADO":
                decisiones_por_semana[semana]["aprobado"] += 1
            else:
                decisiones_por_semana[semana]["rechazado"] += 1

        # Calcular tasas de aprobación semanales
        tasas_semanales = []
        for semana, datos in decisiones_por_semana.items():
            total = datos["aprobado"] + datos["rechazado"]
            if total >= 3:  # Solo semanas con suficientes decisiones
                tasa = (datos["aprobado"] / total) * 100
                tasas_semanales.append(tasa)

        if len(tasas_semanales) >= 3:
            # Calcular desviación estándar de las tasas
            promedio = sum(tasas_semanales) / len(tasas_semanales)
            varianza = sum((tasa - promedio) ** 2 for tasa in tasas_semanales) / len(
                tasas_semanales
            )
            desviacion = varianza**0.5

            if desviacion < 10:
                return "muy_consistente"
            elif desviacion < 20:
                return "consistente"
            else:
                return "inconsistente"

        return "pocos_datos"

    def _analizar_patrones_trabajo_usuario(self, actividad_usuario):
        """Analiza patrones de trabajo del usuario"""
        if not actividad_usuario:
            return {}

        # Análisis por hora del día
        actividad_por_hora = {}
        for cambio in actividad_usuario:
            hora = cambio.fecha_cambio.hour
            actividad_por_hora[hora] = actividad_por_hora.get(hora, 0) + 1

        # Análisis por día de la semana
        actividad_por_dia_semana = {}
        for cambio in actividad_usuario:
            dia_semana = cambio.fecha_cambio.strftime("%A")
            actividad_por_dia_semana[dia_semana] = (
                actividad_por_dia_semana.get(dia_semana, 0) + 1
            )

        # Horario más productivo
        hora_mas_productiva = (
            max(actividad_por_hora.items(), key=lambda x: x[1])[0]
            if actividad_por_hora
            else None
        )
        dia_mas_productivo = (
            max(actividad_por_dia_semana.items(), key=lambda x: x[1])[0]
            if actividad_por_dia_semana
            else None
        )

        # Detectar horario de trabajo preferido
        if actividad_por_hora:
            horas_activas = [
                hora for hora, count in actividad_por_hora.items() if count > 0
            ]
            if horas_activas:
                hora_inicio = min(horas_activas)
                hora_fin = max(horas_activas)
                horario_trabajo = f"{hora_inicio:02d}:00 - {hora_fin:02d}:00"
            else:
                horario_trabajo = "no_detectado"
        else:
            horario_trabajo = "sin_datos"

        return {
            "actividad_por_hora": actividad_por_hora,
            "actividad_por_dia_semana": actividad_por_dia_semana,
            "hora_mas_productiva": (
                f"{hora_mas_productiva:02d}:00"
                if hora_mas_productiva is not None
                else None
            ),
            "dia_mas_productivo": dia_mas_productivo,
            "horario_trabajo_detectado": horario_trabajo,
            "tipo_trabajador": self._clasificar_tipo_trabajador(actividad_por_hora),
        }

    def _clasificar_tipo_trabajador(self, actividad_por_hora):
        """Clasifica el tipo de trabajador basado en horarios"""
        if not actividad_por_hora:
            return "sin_datos"

        # Horas de la mañana (6-12)
        actividad_mañana = sum(actividad_por_hora.get(h, 0) for h in range(6, 12))
        # Horas de la tarde (12-18)
        actividad_tarde = sum(actividad_por_hora.get(h, 0) for h in range(12, 18))
        # Horas de la noche (18-22)
        actividad_noche = sum(actividad_por_hora.get(h, 0) for h in range(18, 22))

        total_actividad = actividad_mañana + actividad_tarde + actividad_noche

        if total_actividad == 0:
            return "sin_patrón"

        porcentaje_mañana = (actividad_mañana / total_actividad) * 100
        porcentaje_tarde = (actividad_tarde / total_actividad) * 100
        porcentaje_noche = (actividad_noche / total_actividad) * 100

        if porcentaje_mañana > 50:
            return "matutino"
        elif porcentaje_tarde > 50:
            return "vespertino"
        elif porcentaje_noche > 30:
            return "nocturno"
        else:
            return "flexible"

    @action(detail=False, methods=["get"])
    def patrones_cambio_estado(self, request):
        """Análisis de patrones en cambios de estado"""
        dias = int(request.query_params.get("dias", 90))
        hace_x_dias = timezone.now() - timedelta(days=dias)

        cambios = self.get_queryset().filter(fecha_cambio__gte=hace_x_dias)

        # Flujos de estado más comunes
        flujos = (
            cambios.exclude(estado_anterior__isnull=True)
            .values("estado_anterior", "estado_nuevo")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # Análisis por hora del día
        cambios_por_hora = {}
        for cambio in cambios:
            hora = cambio.fecha_cambio.hour
            cambios_por_hora[hora] = cambios_por_hora.get(hora, 0) + 1

        # Análisis por día de la semana
        cambios_por_dia_semana = {}
        for cambio in cambios:
            dia_semana = calendar.day_name[cambio.fecha_cambio.weekday()]
            cambios_por_dia_semana[dia_semana] = (
                cambios_por_dia_semana.get(dia_semana, 0) + 1
            )

        # Estados que más se revierten
        reversiones = self._detectar_reversiones(cambios)

        # Análisis de tiempo entre cambios
        tiempos_entre_cambios = self._analizar_tiempos_entre_cambios(cambios)

        # Análisis de productividad por período
        productividad_temporal = self._analizar_productividad_temporal(cambios, dias)

        return Response(
            {
                "periodo_analisis": f"{dias} días",
                "flujos_mas_comunes": list(flujos[:10]),
                "patrones_temporales": {
                    "actividad_por_hora": cambios_por_hora,
                    "actividad_por_dia_semana": cambios_por_dia_semana,
                    "hora_mas_activa": (
                        max(cambios_por_hora.items(), key=lambda x: x[1])[0]
                        if cambios_por_hora
                        else None
                    ),
                    "dia_mas_activo": (
                        max(cambios_por_dia_semana.items(), key=lambda x: x[1])[0]
                        if cambios_por_dia_semana
                        else None
                    ),
                },
                "reversiones_detectadas": reversiones,
                "tiempos_entre_cambios": tiempos_entre_cambios,
                "productividad_temporal": productividad_temporal,
                "insights": self._generar_insights_patrones(
                    flujos, cambios_por_hora, reversiones
                ),
            }
        )

    def _detectar_reversiones(self, cambios):
        """Detecta patrones de reversión en cambios de estado"""
        reversiones = []

        # Agrupar por marca
        marcas_con_cambios = {}
        for cambio in cambios:
            marca_id = cambio.marca.id
            if marca_id not in marcas_con_cambios:
                marcas_con_cambios[marca_id] = []
            marcas_con_cambios[marca_id].append(cambio)

        # Buscar reversiones (A->B->A)
        for marca_id, historial_marca in marcas_con_cambios.items():
            if len(historial_marca) >= 3:
                # Ordenar por fecha
                historial_ordenado = sorted(
                    historial_marca, key=lambda x: x.fecha_cambio
                )

                for i in range(len(historial_ordenado) - 2):
                    cambio1 = historial_ordenado[i]
                    cambio2 = historial_ordenado[i + 1]
                    cambio3 = historial_ordenado[i + 2]

                    # Verificar patrón A->B->A
                    if (
                        cambio1.estado_nuevo == cambio3.estado_nuevo
                        and cambio1.estado_nuevo != cambio2.estado_nuevo
                    ):

                        reversiones.append(
                            {
                                "marca_numero": cambio1.marca.numero_marca,
                                "patron": f"{cambio1.estado_nuevo} → {cambio2.estado_nuevo} → {cambio3.estado_nuevo}",
                                "fechas": [
                                    cambio1.fecha_cambio.strftime("%Y-%m-%d %H:%M"),
                                    cambio2.fecha_cambio.strftime("%Y-%m-%d %H:%M"),
                                    cambio3.fecha_cambio.strftime("%Y-%m-%d %H:%M"),
                                ],
                                "usuarios": [
                                    cambio1.usuario_responsable,
                                    cambio2.usuario_responsable,
                                    cambio3.usuario_responsable,
                                ],
                            }
                        )

        return reversiones[:10]  # Limitar a 10 casos más recientes

    def _analizar_tiempos_entre_cambios(self, cambios):
        """Analiza tiempos promedio entre cambios de estado"""
        # Agrupar por tipo de flujo
        flujos_tiempo = {}

        for cambio in cambios:
            if cambio.estado_anterior:
                flujo = f"{cambio.estado_anterior}_to_{cambio.estado_nuevo}"

                if flujo not in flujos_tiempo:
                    flujos_tiempo[flujo] = []

                # Buscar el cambio anterior para esta marca
                cambio_anterior = (
                    HistorialEstadoMarca.objects.filter(
                        marca=cambio.marca,
                        fecha_cambio__lt=cambio.fecha_cambio,
                        estado_nuevo=cambio.estado_anterior,
                    )
                    .order_by("-fecha_cambio")
                    .first()
                )

                if cambio_anterior:
                    tiempo_transcurrido = (
                        cambio.fecha_cambio - cambio_anterior.fecha_cambio
                    ).total_seconds() / 3600
                    flujos_tiempo[flujo].append(tiempo_transcurrido)

        # Calcular promedios
        resumen_tiempos = {}
        for flujo, tiempos in flujos_tiempo.items():
            if tiempos:
                resumen_tiempos[flujo] = {
                    "tiempo_promedio_horas": round(sum(tiempos) / len(tiempos), 2),
                    "tiempo_minimo_horas": round(min(tiempos), 2),
                    "tiempo_maximo_horas": round(max(tiempos), 2),
                    "cantidad_casos": len(tiempos),
                }

        return resumen_tiempos

    def _analizar_productividad_temporal(self, cambios, dias):
        """Analiza la productividad por diferentes períodos temporales"""
        ahora = timezone.now()

        # Dividir en semanas
        productividad_semanal = {}
        for cambio in cambios:
            semana = cambio.fecha_cambio.strftime("%Y-%W")
            productividad_semanal[semana] = productividad_semanal.get(semana, 0) + 1

        # Calcular promedios
        semanas_activas = len(productividad_semanal)
        promedio_semanal = (
            sum(productividad_semanal.values()) / semanas_activas
            if semanas_activas > 0
            else 0
        )

        # Encontrar picos y valles
        if productividad_semanal:
            semana_mas_productiva = max(
                productividad_semanal.items(), key=lambda x: x[1]
            )
            semana_menos_productiva = min(
                productividad_semanal.items(), key=lambda x: x[1]
            )
        else:
            semana_mas_productiva = semana_menos_productiva = None

        return {
            "promedio_cambios_por_semana": round(promedio_semanal, 2),
            "semanas_analizadas": semanas_activas,
            "semana_mas_productiva": (
                {
                    "semana": semana_mas_productiva[0],
                    "cambios": semana_mas_productiva[1],
                }
                if semana_mas_productiva
                else None
            ),
            "semana_menos_productiva": (
                {
                    "semana": semana_menos_productiva[0],
                    "cambios": semana_menos_productiva[1],
                }
                if semana_menos_productiva
                else None
            ),
            "variabilidad": (
                "alta"
                if semanas_activas > 0
                and (
                    max(productividad_semanal.values())
                    - min(productividad_semanal.values())
                )
                > promedio_semanal
                else "baja"
            ),
        }

    def _generar_insights_patrones(self, flujos, cambios_por_hora, reversiones):
        """Genera insights sobre patrones de cambio"""
        insights = []

        # Insight sobre flujo más común
        if flujos:
            flujo_principal = flujos[0]
            insights.append(
                {
                    "categoria": "Flujo Principal",
                    "prioridad": "info",
                    "insight": f"El cambio más común es de {flujo_principal['estado_anterior']} a {flujo_principal['estado_nuevo']} ({flujo_principal['total']} veces)",
                    "recomendacion": "Optimizar este flujo principal para mejorar eficiencia general",
                }
            )

        # Insight sobre horarios
        if cambios_por_hora:
            hora_pico = max(cambios_por_hora.items(), key=lambda x: x[1])
            hora_valle = min(cambios_por_hora.items(), key=lambda x: x[1])

            insights.append(
                {
                    "categoria": "Horario de Actividad",
                    "prioridad": "media",
                    "insight": f"Mayor actividad a las {hora_pico[0]:02d}:00 horas ({hora_pico[1]} cambios), menor actividad a las {hora_valle[0]:02d}:00 horas ({hora_valle[1]} cambios)",
                    "recomendacion": f"Considerar redistribuir carga de trabajo desde las {hora_pico[0]:02d}:00 hacia horarios menos ocupados",
                }
            )

        # Insight sobre reversiones
        if reversiones:
            insights.append(
                {
                    "categoria": "Calidad del Proceso",
                    "prioridad": "alta",
                    "insight": f"Se detectaron {len(reversiones)} casos de reversión de estados, sugiriendo posible inconsistencia en criterios de evaluación",
                    "recomendacion": "Revisar y estandarizar criterios de evaluación, capacitar evaluadores sobre casos límite",
                }
            )
        else:
            insights.append(
                {
                    "categoria": "Calidad del Proceso",
                    "prioridad": "positivo",
                    "insight": "No se detectaron reversiones significativas en estados, indicando consistencia en el proceso",
                    "recomendacion": "Mantener los estándares actuales de evaluación",
                }
            )

        # Insight sobre eficiencia general
        total_cambios = sum(cambios_por_hora.values()) if cambios_por_hora else 0
        if total_cambios > 0:
            # Calcular concentración de actividad
            horas_activas = len([h for h, c in cambios_por_hora.items() if c > 0])
            if horas_activas < 8:
                insights.append(
                    {
                        "categoria": "Eficiencia Operacional",
                        "prioridad": "oportunidad",
                        "insight": f"Actividad concentrada en {horas_activas} horas del día",
                        "recomendacion": "Considerar ampliar horarios de operación para distribuir mejor la carga de trabajo",
                    }
                )

        return insights

    @action(detail=False, methods=["get"])
    def eficiencia_evaluadores(self, request):
        """Análisis de eficiencia de evaluadores"""
        dias = int(request.query_params.get("dias", 30))
        hace_x_dias = timezone.now() - timedelta(days=dias)

        # Obtener actividad de evaluadores (excluyendo sistema)
        actividad_evaluadores = (
            self.get_queryset()
            .filter(fecha_cambio__gte=hace_x_dias)
            .exclude(usuario_responsable__in=["sistema", "anonimo", ""])
        )

        # Estadísticas por evaluador
        stats_evaluadores = (
            actividad_evaluadores.values("usuario_responsable")
            .annotate(
                total_evaluaciones=Count("id"),
                aprobaciones=Count("id", filter=Q(estado_nuevo="APROBADO")),
                rechazos=Count("id", filter=Q(estado_nuevo="RECHAZADO")),
                en_proceso=Count("id", filter=Q(estado_nuevo="EN_PROCESO")),
                marcas_unicas=Count("marca", distinct=True),
            )
            .order_by("-total_evaluaciones")
        )

        # Calcular métricas adicionales
        for evaluador in stats_evaluadores:
            total_decisiones = evaluador["aprobaciones"] + evaluador["rechazos"]
            evaluador["tasa_aprobacion"] = round(
                (
                    (evaluador["aprobaciones"] / total_decisiones * 100)
                    if total_decisiones > 0
                    else 0
                ),
                2,
            )
            evaluador["decisiones_por_dia"] = round(
                evaluador["total_evaluaciones"] / dias, 2
            )

            # Calcular tiempo promedio de evaluación para este evaluador
            evaluaciones_evaluador = actividad_evaluadores.filter(
                usuario_responsable=evaluador["usuario_responsable"],
                estado_nuevo__in=["APROBADO", "RECHAZADO"],
            )

            tiempos_evaluacion = []
            for evaluacion in evaluaciones_evaluador:
                if evaluacion.marca.fecha_registro:
                    tiempo_eval = (
                        evaluacion.fecha_cambio - evaluacion.marca.fecha_registro
                    ).total_seconds() / 3600
                    if tiempo_eval > 0:  # Evitar tiempos negativos
                        tiempos_evaluacion.append(tiempo_eval)

            evaluador["tiempo_promedio_horas"] = round(
                (
                    sum(tiempos_evaluacion) / len(tiempos_evaluacion)
                    if tiempos_evaluacion
                    else 0
                ),
                2,
            )

            # Productividad (marcas únicas trabajadas)
            evaluador["productividad_marcas_unicas"] = evaluador["marcas_unicas"]

            # Especialización (% de un tipo de decisión)
            if total_decisiones > 0:
                evaluador["especializacion_aprobacion"] = round(
                    (evaluador["aprobaciones"] / total_decisiones) * 100, 2
                )
            else:
                evaluador["especializacion_aprobacion"] = 0

        # Calcular score de eficiencia
        for evaluador in stats_evaluadores:
            # Score de eficiencia: combinación de velocidad, precisión y productividad
            velocidad_score = min(
                evaluador["decisiones_por_dia"] * 10, 40
            )  # Max 40 puntos

            # Precisión: tasa de aprobación cerca del promedio del sistema (80% ideal)
            tasa_ideal = 80
            precision_score = max(
                0, 30 - abs(evaluador["tasa_aprobacion"] - tasa_ideal) * 0.5
            )

            # Tiempo de respuesta: mejor score para tiempos entre 24-48 horas
            tiempo_score = 0
            if 24 <= evaluador["tiempo_promedio_horas"] <= 48:
                tiempo_score = 30
            elif evaluador["tiempo_promedio_horas"] < 24:
                tiempo_score = 25  # Muy rápido puede comprometer calidad
            elif evaluador["tiempo_promedio_horas"] <= 72:
                tiempo_score = 20
            else:
                tiempo_score = 10  # Muy lento

            eficiencia_score = velocidad_score + precision_score + tiempo_score
            evaluador["eficiencia_score"] = round(max(eficiencia_score, 0), 2)

            # Clasificación de evaluador
            evaluador["clasificacion"] = self._clasificar_evaluador(evaluador)

        # Ordenar por score de eficiencia
        ranking_eficiencia = sorted(
            stats_evaluadores, key=lambda x: x["eficiencia_score"], reverse=True
        )

        # Métricas del sistema
        metricas_sistema = self._calcular_metricas_sistema(stats_evaluadores, dias)

        return Response(
            {
                "periodo_analisis": f"{dias} días",
                "estadisticas_evaluadores": list(stats_evaluadores),
                "ranking_eficiencia": ranking_eficiencia,
                "metricas_sistema": metricas_sistema,
                "analisis_comparativo": self._generar_analisis_comparativo(
                    ranking_eficiencia
                ),
                "recomendaciones": self._generar_recomendaciones_evaluadores(
                    ranking_eficiencia
                ),
            }
        )

    def _clasificar_evaluador(self, evaluador):
        """Clasifica al evaluador según sus métricas"""
        score = evaluador["eficiencia_score"]
        tiempo = evaluador["tiempo_promedio_horas"]
        tasa = evaluador["tasa_aprobacion"]
        velocidad = evaluador["decisiones_por_dia"]

        if score >= 80:
            return "excelente"
        elif score >= 65:
            if velocidad > 2:
                return "rapido_eficiente"
            else:
                return "calidad_premium"
        elif score >= 50:
            if tiempo > 72:
                return "meticuloso"
            else:
                return "competente"
        elif score >= 30:
            if velocidad < 0.5:
                return "necesita_motivacion"
            else:
                return "en_desarrollo"
        else:
            return "requiere_atencion"

    def _calcular_metricas_sistema(self, stats_evaluadores, dias):
        """Calcula métricas generales del sistema de evaluadores"""
        if not stats_evaluadores:
            return {"mensaje": "Sin evaluadores activos en el período"}

        total_evaluaciones = sum(e["total_evaluaciones"] for e in stats_evaluadores)
        total_decisiones = sum(
            e["aprobaciones"] + e["rechazos"] for e in stats_evaluadores
        )
        total_aprobaciones = sum(e["aprobaciones"] for e in stats_evaluadores)

        # Carga de trabajo
        evaluaciones_por_evaluador = [
            e["total_evaluaciones"] for e in stats_evaluadores
        ]
        carga_max = max(evaluaciones_por_evaluador)
        carga_min = min(evaluaciones_por_evaluador)
        carga_promedio = sum(evaluaciones_por_evaluador) / len(
            evaluaciones_por_evaluador
        )

        # Tiempos promedio
        tiempos_evaluadores = [
            e["tiempo_promedio_horas"]
            for e in stats_evaluadores
            if e["tiempo_promedio_horas"] > 0
        ]
        tiempo_sistema = (
            sum(tiempos_evaluadores) / len(tiempos_evaluadores)
            if tiempos_evaluadores
            else 0
        )

        return {
            "total_evaluadores_activos": len(stats_evaluadores),
            "total_evaluaciones_sistema": total_evaluaciones,
            "promedio_evaluaciones_por_evaluador": round(carga_promedio, 2),
            "distribucion_carga": {
                "maxima": carga_max,
                "minima": carga_min,
                "desbalance": round(
                    (
                        ((carga_max - carga_min) / carga_promedio * 100)
                        if carga_promedio > 0
                        else 0
                    ),
                    2,
                ),
            },
            "tasa_aprobacion_sistema": round(
                (
                    (total_aprobaciones / total_decisiones * 100)
                    if total_decisiones > 0
                    else 0
                ),
                2,
            ),
            "tiempo_promedio_sistema": round(tiempo_sistema, 2),
            "productividad_diaria_sistema": round(total_evaluaciones / dias, 2),
            "nivel_eficiencia_general": self._evaluar_eficiencia_general(
                stats_evaluadores
            ),
        }

    def _evaluar_eficiencia_general(self, stats_evaluadores):
        """Evalúa la eficiencia general del equipo de evaluadores"""
        if not stats_evaluadores:
            return "sin_datos"

        scores = [e["eficiencia_score"] for e in stats_evaluadores]
        score_promedio = sum(scores) / len(scores)

        # Porcentaje de evaluadores de alto rendimiento
        alto_rendimiento = len([s for s in scores if s >= 70])
        porcentaje_alto_rendimiento = (alto_rendimiento / len(scores)) * 100

        if score_promedio >= 75 and porcentaje_alto_rendimiento >= 70:
            return "excelente"
        elif score_promedio >= 60 and porcentaje_alto_rendimiento >= 50:
            return "bueno"
        elif score_promedio >= 45:
            return "aceptable"
        else:
            return "necesita_mejora"

    def _generar_analisis_comparativo(self, ranking):
        """Genera análisis comparativo entre evaluadores"""
        if len(ranking) < 2:
            return {"mensaje": "Insuficientes evaluadores para comparación"}

        mejor = ranking[0]
        peor = ranking[-1]

        # Diferencias clave
        diferencias = {
            "eficiencia_score": mejor["eficiencia_score"] - peor["eficiencia_score"],
            "velocidad": mejor["decisiones_por_dia"] - peor["decisiones_por_dia"],
            "tiempo_promedio": peor["tiempo_promedio_horas"]
            - mejor["tiempo_promedio_horas"],
            "tasa_aprobacion": abs(mejor["tasa_aprobacion"] - peor["tasa_aprobacion"]),
        }

        # Identificar fortalezas del mejor evaluador
        fortalezas_mejor = []
        if mejor["decisiones_por_dia"] > 1.5:
            fortalezas_mejor.append("alta_velocidad")
        if 70 <= mejor["tasa_aprobacion"] <= 90:
            fortalezas_mejor.append("tasa_equilibrada")
        if mejor["tiempo_promedio_horas"] <= 48:
            fortalezas_mejor.append("respuesta_rapida")

        return {
            "mejor_evaluador": {
                "nombre": mejor["usuario_responsable"],
                "score": mejor["eficiencia_score"],
                "fortalezas": fortalezas_mejor,
            },
            "evaluador_mejora": {
                "nombre": peor["usuario_responsable"],
                "score": peor["eficiencia_score"],
                "areas_mejora": self._identificar_areas_mejora(peor),
            },
            "diferencias_clave": diferencias,
            "oportunidades_nivelacion": self._generar_oportunidades_nivelacion(
                mejor, peor
            ),
        }

    def _identificar_areas_mejora(self, evaluador):
        """Identifica áreas específicas de mejora para un evaluador"""
        areas = []

        if evaluador["decisiones_por_dia"] < 0.5:
            areas.append("incrementar_velocidad")

        if evaluador["tiempo_promedio_horas"] > 72:
            areas.append("reducir_tiempo_respuesta")

        if evaluador["tasa_aprobacion"] < 60 or evaluador["tasa_aprobacion"] > 95:
            areas.append("equilibrar_criterios")

        if evaluador["total_evaluaciones"] < 10:
            areas.append("aumentar_actividad")

        return areas

    def _generar_oportunidades_nivelacion(self, mejor, peor):
        """Genera oportunidades para nivelar el desempeño"""
        oportunidades = []

        # Mentoring
        oportunidades.append(
            {
                "tipo": "mentoring",
                "descripcion": f"{mejor['usuario_responsable']} puede mentorear a {peor['usuario_responsable']}",
                "beneficio": "Transferencia de mejores prácticas y conocimiento",
            }
        )

        # Redistribución de carga
        if mejor["decisiones_por_dia"] > peor["decisiones_por_dia"] * 2:
            oportunidades.append(
                {
                    "tipo": "redistribucion_carga",
                    "descripcion": "Redistribuir casos complejos del evaluador más lento al más eficiente",
                    "beneficio": "Optimización general del tiempo de procesamiento",
                }
            )

        # Capacitación específica
        areas_mejora = self._identificar_areas_mejora(peor)
        if areas_mejora:
            oportunidades.append(
                {
                    "tipo": "capacitacion",
                    "descripcion": f"Capacitación específica en: {', '.join(areas_mejora)}",
                    "beneficio": "Mejora directa en áreas débiles identificadas",
                }
            )

        return oportunidades

    def _generar_recomendaciones_evaluadores(self, ranking):
        """Genera recomendaciones para mejorar eficiencia de evaluadores"""
        recomendaciones = []

        if not ranking:
            return recomendaciones

        # Mejor evaluador como referencia
        mejor_evaluador = ranking[0]
        recomendaciones.append(
            {
                "categoria": "Mejores Prácticas",
                "prioridad": "alta",
                "recomendacion": f'Documentar y replicar metodología de {mejor_evaluador["usuario_responsable"]} (score: {mejor_evaluador["eficiencia_score"]:.1f})',
                "detalle": f'Tasa aprobación: {mejor_evaluador["tasa_aprobacion"]:.1f}%, Velocidad: {mejor_evaluador["decisiones_por_dia"]:.1f} decisiones/día',
                "acciones": [
                    "Documentar proceso de evaluación",
                    "Crear guías de mejores prácticas",
                    "Implementar sesiones de sharing",
                ],
            }
        )

        # Evaluadores que necesitan capacitación
        evaluadores_bajo_rendimiento = [
            e for e in ranking if e["eficiencia_score"] < 40
        ]
        if evaluadores_bajo_rendimiento:
            recomendaciones.append(
                {
                    "categoria": "Capacitación",
                    "prioridad": "alta",
                    "recomendacion": f"{len(evaluadores_bajo_rendimiento)} evaluadores requieren capacitación adicional",
                    "evaluadores": [
                        {
                            "nombre": e["usuario_responsable"],
                            "clasificacion": e["clasificacion"],
                            "score": e["eficiencia_score"],
                        }
                        for e in evaluadores_bajo_rendimiento
                    ],
                    "acciones": [
                        "Programa de capacitación intensiva",
                        "Asignación de mentor",
                        "Seguimiento semanal de progreso",
                    ],
                }
            )

        # Evaluadores muy lentos
        evaluadores_lentos = [e for e in ranking if e["tiempo_promedio_horas"] > 72]
        if evaluadores_lentos:
            recomendaciones.append(
                {
                    "categoria": "Optimización de Tiempo",
                    "prioridad": "media",
                    "recomendacion": f"{len(evaluadores_lentos)} evaluadores exceden tiempo objetivo (72h)",
                    "evaluadores_afectados": [
                        e["usuario_responsable"] for e in evaluadores_lentos
                    ],
                    "acciones": [
                        "Revisar casos complejos asignados",
                        "Implementar herramientas de apoyo",
                        "Establecer metas incrementales",
                    ],
                }
            )

        # Evaluadores muy rápidos (posible compromiso de calidad)
        evaluadores_muy_rapidos = [
            e for e in ranking if e["tiempo_promedio_horas"] < 12
        ]
        if evaluadores_muy_rapidos:
            recomendaciones.append(
                {
                    "categoria": "Control de Calidad",
                    "prioridad": "media",
                    "recomendacion": f"{len(evaluadores_muy_rapidos)} evaluadores con tiempos muy bajos - verificar calidad",
                    "evaluadores_afectados": [
                        e["usuario_responsable"] for e in evaluadores_muy_rapidos
                    ],
                    "acciones": [
                        "Auditoría de calidad de decisiones",
                        "Revisión de casos procesados",
                        "Ajuste de criterios si es necesario",
                    ],
                }
            )

        # Recomendación de redistribución de carga
        cargas = [e["total_evaluaciones"] for e in ranking]
        if len(cargas) > 1:
            carga_max = max(cargas)
            carga_min = min(cargas)
            desbalance = ((carga_max - carga_min) / (sum(cargas) / len(cargas))) * 100

            if desbalance > 50:  # Más del 50% de desbalance
                recomendaciones.append(
                    {
                        "categoria": "Distribución de Carga",
                        "prioridad": "media",
                        "recomendacion": f"Desbalance significativo en carga de trabajo ({desbalance:.1f}%)",
                        "detalle": f"Rango: {carga_min} - {carga_max} evaluaciones",
                        "acciones": [
                            "Implementar sistema de asignación automática",
                            "Balancear carga según eficiencia de evaluadores",
                            "Monitorear distribución semanalmente",
                        ],
                    }
                )

        return recomendaciones
