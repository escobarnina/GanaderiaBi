# business_intelligence/services.py
from django.db import models
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q, Max, Min
from .models import (
    MarcaGanadoBovino,
    LogoMarcaBovina,
    KPIGanadoBovino,
    HistorialEstadoMarca,
)
import requests
from datetime import datetime, timedelta
from decimal import Decimal
import json


class DataGenerationService:
    """Servicio para generar datos usando APIs externas y LLMs específico para ganado bovino"""

    @staticmethod
    def generar_datos_mockaroo(cantidad=50):
        """
        Genera datos de marcas bovinas usando Mockaroo API
        Requiere configurar API_KEY en settings
        """
        try:
            # URL de ejemplo para Mockaroo (requiere configuración)
            url = "https://my.api.mockaroo.com/ganaderia_bovino.json"
            headers = {"X-API-Key": "tu-api-key-aqui"}

            response = requests.get(url, headers=headers, params={"count": cantidad})

            if response.status_code == 200:
                datos = response.json()
                marcas_creadas = []

                for dato in datos:
                    marca = MarcaGanadoBovino.objects.create(
                        numero_marca=dato.get("numero_marca"),
                        nombre_productor=dato.get("nombre_productor"),
                        raza_bovino=dato.get("raza_bovino", "CRIOLLO"),
                        proposito_ganado=dato.get("proposito_ganado", "CARNE"),
                        cantidad_cabezas=dato.get("cantidad_cabezas", 50),
                        departamento=dato.get("departamento", "SANTA_CRUZ"),
                        municipio=dato.get("municipio", "Santa Cruz"),
                        ci_productor=dato.get("ci_productor"),
                        telefono_productor=dato.get("telefono_productor"),
                        monto_certificacion=dato.get("monto_certificacion", 0),
                        estado=dato.get("estado", "PENDIENTE"),
                    )
                    marcas_creadas.append(marca)

                return marcas_creadas
            else:
                raise Exception(f"Error en Mockaroo API: {response.status_code}")

        except Exception as e:
            print(f"Error generando datos con Mockaroo: {e}")
            return []

    @staticmethod
    def generar_descripcion_marca_llm(marca):
        """
        Genera descripción de marca bovina usando LLM
        Simulación de llamada a GPT/LlaMA con contexto bovino
        """
        try:
            # Aquí iría la llamada real a OpenAI, Anthropic, etc.
            prompt = f"""
            Genera una descripción profesional para una marca de ganado bovino con los siguientes datos:
            - Número de marca: {marca.numero_marca}
            - Productor: {marca.nombre_productor}
            - Raza bovina: {marca.get_raza_bovino_display()}
            - Propósito: {marca.get_proposito_ganado_display()}
            - Cantidad de cabezas: {marca.cantidad_cabezas}
            - Ubicación: {marca.municipio}, {marca.get_departamento_display()}
            
            La descripción debe ser profesional, específica para ganado bovino y adecuada para certificación oficial.
            """

            # Simulación de respuesta (reemplazar con llamada real)
            descripcion_simulada = f"""
            Marca de ganado bovino registrada oficialmente bajo el número {marca.numero_marca}, 
            perteneciente al productor {marca.nombre_productor}. El establecimiento ganadero cuenta 
            con {marca.cantidad_cabezas} cabezas de ganado de raza {marca.get_raza_bovino_display()}, 
            destinadas a {marca.get_proposito_ganado_display().lower()}. Las operaciones se desarrollan 
            en {marca.municipio}, departamento de {marca.get_departamento_display()}. Esta certificación 
            garantiza la trazabilidad y calidad del ganado bovino bajo los estándares nacionales de 
            producción pecuaria, cumpliendo con las normativas vigentes para la actividad ganadera en Bolivia.
            """

            return descripcion_simulada.strip()

        except Exception as e:
            print(f"Error generando descripción con LLM: {e}")
            return f"Marca Bovina {marca.numero_marca} - {marca.nombre_productor}"

    @staticmethod
    def generar_prompt_logo_bovino(marca):
        """Genera prompts específicos para logos de ganado bovino usando IA"""
        prompts_templates = [
            f"Logo profesional para estancia ganadera {marca.nombre_productor}, ganado {marca.get_raza_bovino_display()}, {marca.get_proposito_ganado_display()}, estilo corporativo moderno, colores tierra",
            f"Diseño de marca para {marca.cantidad_cabezas} cabezas de ganado bovino raza {marca.get_raza_bovino_display()}, elementos rurales, {marca.get_departamento_display()} Bolivia",
            f"Logo ganadero profesional, silueta de toro {marca.get_raza_bovino_display()}, marca {marca.numero_marca}, identidad visual robusta",
            f"Emblema para producción {marca.get_proposito_ganado_display()} de ganado bovino, {marca.municipio}, diseño tradicional boliviano contemporáneo",
        ]

        return prompts_templates


class AnalyticsService:
    """Servicio para análisis avanzado de datos de ganado bovino"""

    @staticmethod
    def calcular_tendencias_departamento():
        """Calcula tendencias de crecimiento por departamento para ganado bovino"""
        ahora = timezone.now()
        mes_actual = ahora.replace(day=1)
        mes_anterior = (mes_actual - timedelta(days=1)).replace(day=1)

        tendencias = []

        for dept in MarcaGanadoBovino.objects.values_list(
            "departamento", flat=True
        ).distinct():
            # Marcas mes actual
            actual = MarcaGanadoBovino.objects.filter(
                departamento=dept, fecha_registro__gte=mes_actual
            ).count()

            # Marcas mes anterior
            anterior = MarcaGanadoBovino.objects.filter(
                departamento=dept,
                fecha_registro__gte=mes_anterior,
                fecha_registro__lt=mes_actual,
            ).count()

            # Cabezas de ganado
            cabezas_actual = (
                MarcaGanadoBovino.objects.filter(
                    departamento=dept, fecha_registro__gte=mes_actual
                ).aggregate(total=Sum("cantidad_cabezas"))["total"]
                or 0
            )

            cabezas_anterior = (
                MarcaGanadoBovino.objects.filter(
                    departamento=dept,
                    fecha_registro__gte=mes_anterior,
                    fecha_registro__lt=mes_actual,
                ).aggregate(total=Sum("cantidad_cabezas"))["total"]
                or 0
            )

            # Calcular crecimiento
            if anterior > 0:
                crecimiento_marcas = ((actual - anterior) / anterior) * 100
            else:
                crecimiento_marcas = 100 if actual > 0 else 0

            if cabezas_anterior > 0:
                crecimiento_cabezas = (
                    (cabezas_actual - cabezas_anterior) / cabezas_anterior
                ) * 100
            else:
                crecimiento_cabezas = 100 if cabezas_actual > 0 else 0

            # Propósito predominante
            proposito_principal = (
                MarcaGanadoBovino.objects.filter(
                    departamento=dept, fecha_registro__gte=mes_actual
                )
                .values("proposito_ganado")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            tendencias.append(
                {
                    "departamento": dept,
                    "departamento_display": dict(
                        MarcaGanadoBovino.DEPARTAMENTO_CHOICES
                    ).get(dept, dept),
                    "marcas_mes_actual": actual,
                    "marcas_mes_anterior": anterior,
                    "cabezas_mes_actual": cabezas_actual,
                    "cabezas_mes_anterior": cabezas_anterior,
                    "crecimiento_marcas_porcentual": round(crecimiento_marcas, 2),
                    "crecimiento_cabezas_porcentual": round(crecimiento_cabezas, 2),
                    "proposito_principal": (
                        proposito_principal["proposito_ganado"]
                        if proposito_principal
                        else None
                    ),
                }
            )

        return sorted(
            tendencias, key=lambda x: x["crecimiento_marcas_porcentual"], reverse=True
        )

    @staticmethod
    def analizar_distribucion_razas():
        """Analiza la distribución de razas bovinas por departamento"""
        resultados = []

        for dept in MarcaGanadoBovino.objects.values_list(
            "departamento", flat=True
        ).distinct():
            razas_dept = (
                MarcaGanadoBovino.objects.filter(departamento=dept)
                .values("raza_bovino")
                .annotate(
                    total_marcas=Count("id"),
                    total_cabezas=Sum("cantidad_cabezas"),
                    promedio_cabezas=Avg("cantidad_cabezas"),
                    monto_promedio=Avg("monto_certificacion"),
                )
                .order_by("-total_marcas")
            )

            resultados.append(
                {
                    "departamento": dept,
                    "departamento_display": dict(
                        MarcaGanadoBovino.DEPARTAMENTO_CHOICES
                    ).get(dept, dept),
                    "razas": list(razas_dept),
                }
            )

        return resultados

    @staticmethod
    def predecir_demanda_mensual():
        """Predice la demanda para el próximo mes basado en tendencias históricas de ganado bovino"""
        # Obtener datos de los últimos 6 meses
        ahora = timezone.now()
        hace_6_meses = ahora - timedelta(days=180)

        marcas_por_mes = (
            MarcaGanadoBovino.objects.filter(fecha_registro__gte=hace_6_meses)
            .extra(select={"mes": "DATE_FORMAT(fecha_registro, '%%Y-%%m')"})
            .values("mes")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                ingresos=Sum("monto_certificacion", filter=Q(estado="APROBADO")),
            )
            .order_by("mes")
        )

        if len(marcas_por_mes) < 3:
            return {
                "prediccion_marcas": 0,
                "prediccion_cabezas": 0,
                "prediccion_ingresos": 0,
                "confianza": "Baja",
                "datos_insuficientes": True,
            }

        # Calcular tendencias
        ultimos_3_meses = list(marcas_por_mes)[-3:]

        promedio_marcas = sum(mes["total_marcas"] for mes in ultimos_3_meses) / len(
            ultimos_3_meses
        )
        promedio_cabezas = sum(
            mes["total_cabezas"] or 0 for mes in ultimos_3_meses
        ) / len(ultimos_3_meses)
        promedio_ingresos = sum(mes["ingresos"] or 0 for mes in ultimos_3_meses) / len(
            ultimos_3_meses
        )

        # Factor de crecimiento
        if len(marcas_por_mes) >= 6:
            primera_mitad = list(marcas_por_mes)[:3]
            segunda_mitad = list(marcas_por_mes)[-3:]

            prom_inicial_marcas = sum(mes["total_marcas"] for mes in primera_mitad) / 3
            prom_reciente_marcas = sum(mes["total_marcas"] for mes in segunda_mitad) / 3

            if prom_inicial_marcas > 0:
                factor_crecimiento = prom_reciente_marcas / prom_inicial_marcas
            else:
                factor_crecimiento = 1.1
        else:
            factor_crecimiento = 1.05

        # Predicciones
        prediccion_marcas = int(promedio_marcas * factor_crecimiento)
        prediccion_cabezas = int(promedio_cabezas * factor_crecimiento)
        prediccion_ingresos = promedio_ingresos * factor_crecimiento

        # Confianza basada en variabilidad
        varianza_marcas = sum(
            (mes["total_marcas"] - promedio_marcas) ** 2 for mes in ultimos_3_meses
        ) / len(ultimos_3_meses)
        coef_variacion = (
            (varianza_marcas**0.5) / promedio_marcas if promedio_marcas > 0 else 1
        )

        if coef_variacion < 0.2:
            confianza = "Alta"
        elif coef_variacion < 0.4:
            confianza = "Media"
        else:
            confianza = "Baja"

        return {
            "prediccion_marcas": prediccion_marcas,
            "prediccion_cabezas": prediccion_cabezas,
            "prediccion_ingresos": round(float(prediccion_ingresos), 2),
            "confianza": confianza,
            "factor_crecimiento": round(factor_crecimiento, 3),
            "datos_historicos": len(marcas_por_mes),
            "datos_insuficientes": False,
            "tendencia_proposito": AnalyticsService._analizar_tendencia_proposito(),
        }

    @staticmethod
    def _analizar_tendencia_proposito():
        """Analiza tendencias por propósito de ganado"""
        mes_actual = timezone.now().replace(day=1)

        return (
            MarcaGanadoBovino.objects.filter(fecha_registro__gte=mes_actual)
            .values("proposito_ganado")
            .annotate(total=Count("id"), cabezas=Sum("cantidad_cabezas"))
            .order_by("-total")
        )

    @staticmethod
    def analizar_eficiencia_regional():
        """Analiza la eficiencia de procesamiento por región"""
        resultados = []

        for dept in MarcaGanadoBovino.objects.values_list(
            "departamento", flat=True
        ).distinct():
            marcas_dept = MarcaGanadoBovino.objects.filter(departamento=dept)

            # Métricas de eficiencia
            tiempo_promedio = (
                marcas_dept.filter(tiempo_procesamiento_horas__isnull=False).aggregate(
                    Avg("tiempo_procesamiento_horas")
                )["tiempo_procesamiento_horas__avg"]
                or 0
            )

            total_procesadas = marcas_dept.filter(
                estado__in=["APROBADO", "RECHAZADO"]
            ).count()
            aprobadas = marcas_dept.filter(estado="APROBADO").count()
            tasa_aprobacion = (
                (aprobadas / total_procesadas * 100) if total_procesadas > 0 else 0
            )

            ingresos_total = (
                marcas_dept.filter(estado="APROBADO").aggregate(
                    Sum("monto_certificacion")
                )["monto_certificacion__sum"]
                or 0
            )

            resultados.append(
                {
                    "departamento": dept,
                    "departamento_display": dict(
                        MarcaGanadoBovino.DEPARTAMENTO_CHOICES
                    ).get(dept, dept),
                    "tiempo_promedio_horas": round(tiempo_promedio, 2),
                    "tasa_aprobacion": round(tasa_aprobacion, 2),
                    "total_marcas": marcas_dept.count(),
                    "total_cabezas": marcas_dept.aggregate(Sum("cantidad_cabezas"))[
                        "cantidad_cabezas__sum"
                    ]
                    or 0,
                    "ingresos_total": float(ingresos_total),
                    "eficiencia_score": round(
                        (tasa_aprobacion / max(tiempo_promedio, 1)) * 100, 2
                    ),
                }
            )

        return sorted(resultados, key=lambda x: x["eficiencia_score"], reverse=True)


class ReportService:
    """Servicio para generar reportes ejecutivos de ganado bovino"""

    @staticmethod
    def generar_reporte_mensual(año, mes):
        """Genera reporte ejecutivo mensual específico para ganado bovino"""
        # Filtros de fecha
        inicio_mes = datetime(año, mes, 1)
        if mes == 12:
            fin_mes = datetime(año + 1, 1, 1)
        else:
            fin_mes = datetime(año, mes + 1, 1)

        # Métricas principales
        marcas_registradas = MarcaGanadoBovino.objects.filter(
            fecha_registro__gte=inicio_mes, fecha_registro__lt=fin_mes
        ).count()

        # Total de cabezas bovinas registradas
        total_cabezas = (
            MarcaGanadoBovino.objects.filter(
                fecha_registro__gte=inicio_mes, fecha_registro__lt=fin_mes
            ).aggregate(Sum("cantidad_cabezas"))["cantidad_cabezas__sum"]
            or 0
        )

        marcas_aprobadas = MarcaGanadoBovino.objects.filter(
            fecha_procesamiento__gte=inicio_mes,
            fecha_procesamiento__lt=fin_mes,
            estado="APROBADO",
        ).count()

        marcas_rechazadas = MarcaGanadoBovino.objects.filter(
            fecha_procesamiento__gte=inicio_mes,
            fecha_procesamiento__lt=fin_mes,
            estado="RECHAZADO",
        ).count()

        ingresos_total = (
            MarcaGanadoBovino.objects.filter(
                fecha_procesamiento__gte=inicio_mes,
                fecha_procesamiento__lt=fin_mes,
                estado="APROBADO",
            ).aggregate(Sum("monto_certificacion"))["monto_certificacion__sum"]
            or 0
        )

        tiempo_promedio = (
            MarcaGanadoBovino.objects.filter(
                fecha_procesamiento__gte=inicio_mes,
                fecha_procesamiento__lt=fin_mes,
                tiempo_procesamiento_horas__isnull=False,
            ).aggregate(Avg("tiempo_procesamiento_horas"))[
                "tiempo_procesamiento_horas__avg"
            ]
            or 0
        )

        # Distribución por raza bovina
        por_raza_bovina = (
            MarcaGanadoBovino.objects.filter(
                fecha_registro__gte=inicio_mes, fecha_registro__lt=fin_mes
            )
            .values("raza_bovino")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                promedio_cabezas=Avg("cantidad_cabezas"),
            )
            .order_by("-total_marcas")
        )

        # Distribución por propósito
        por_proposito = (
            MarcaGanadoBovino.objects.filter(
                fecha_registro__gte=inicio_mes, fecha_registro__lt=fin_mes
            )
            .values("proposito_ganado")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                ingresos=Sum("monto_certificacion", filter=Q(estado="APROBADO")),
            )
            .order_by("-total_marcas")
        )

        # Top departamentos ganaderos
        por_departamento = (
            MarcaGanadoBovino.objects.filter(
                fecha_registro__gte=inicio_mes, fecha_registro__lt=fin_mes
            )
            .values("departamento")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                ingresos=Sum("monto_certificacion", filter=Q(estado="APROBADO")),
                promedio_cabezas=Avg("cantidad_cabezas"),
            )
            .order_by("-total_cabezas")[:5]
        )

        # Estadísticas de logos bovinos
        logos_generados = LogoMarcaBovina.objects.filter(
            fecha_generacion__gte=inicio_mes, fecha_generacion__lt=fin_mes
        ).count()

        logos_exitosos = LogoMarcaBovina.objects.filter(
            fecha_generacion__gte=inicio_mes, fecha_generacion__lt=fin_mes, exito=True
        ).count()

        # Análisis de calidad de logos
        logos_por_calidad = (
            LogoMarcaBovina.objects.filter(
                fecha_generacion__gte=inicio_mes, fecha_generacion__lt=fin_mes
            )
            .values("calidad_logo")
            .annotate(total=Count("id"))
        )

        return {
            "periodo": f"{mes:02d}/{año}",
            "tipo_reporte": "Ganado Bovino",
            "metricas_principales": {
                "marcas_registradas": marcas_registradas,
                "total_cabezas_bovinas": total_cabezas,
                "promedio_cabezas_por_marca": (
                    round(total_cabezas / marcas_registradas, 2)
                    if marcas_registradas > 0
                    else 0
                ),
                "marcas_aprobadas": marcas_aprobadas,
                "marcas_rechazadas": marcas_rechazadas,
                "tasa_aprobacion": round(
                    (
                        (
                            marcas_aprobadas
                            / (marcas_aprobadas + marcas_rechazadas)
                            * 100
                        )
                        if (marcas_aprobadas + marcas_rechazadas) > 0
                        else 0
                    ),
                    2,
                ),
                "ingresos_total": float(ingresos_total),
                "tiempo_promedio_procesamiento": round(tiempo_promedio, 2),
            },
            "distribucion_razas_bovinas": list(por_raza_bovina),
            "distribucion_por_proposito": list(por_proposito),
            "top_departamentos_ganaderos": list(por_departamento),
            "estadisticas_logos": {
                "total_generados": logos_generados,
                "exitosos": logos_exitosos,
                "tasa_exito": round(
                    (
                        (logos_exitosos / logos_generados * 100)
                        if logos_generados > 0
                        else 0
                    ),
                    2,
                ),
                "distribucion_calidad": list(logos_por_calidad),
            },
            "analisis_regional": AnalyticsService.analizar_eficiencia_regional(),
            "tendencias_departamentales": AnalyticsService.calcular_tendencias_departamento()[
                :5
            ],
        }

    @staticmethod
    def generar_reporte_productor(marca_id):
        """Genera reporte específico para un productor"""
        try:
            marca = MarcaGanadoBovino.objects.get(id=marca_id)

            # Historial de la marca
            historial = HistorialEstadoMarca.objects.filter(marca=marca).order_by(
                "-fecha_cambio"
            )

            # Logos asociados
            logos = LogoMarcaBovina.objects.filter(marca=marca)

            # Comparación regional
            marcas_region = MarcaGanadoBovino.objects.filter(
                departamento=marca.departamento, proposito_ganado=marca.proposito_ganado
            ).exclude(id=marca.id)

            promedio_regional_cabezas = (
                marcas_region.aggregate(Avg("cantidad_cabezas"))[
                    "cantidad_cabezas__avg"
                ]
                or 0
            )

            promedio_regional_monto = (
                marcas_region.aggregate(Avg("monto_certificacion"))[
                    "monto_certificacion__avg"
                ]
                or 0
            )

            return {
                "marca": {
                    "numero": marca.numero_marca,
                    "productor": marca.nombre_productor,
                    "raza": marca.get_raza_bovino_display(),
                    "proposito": marca.get_proposito_ganado_display(),
                    "cantidad_cabezas": marca.cantidad_cabezas,
                    "ubicacion": f"{marca.municipio}, {marca.get_departamento_display()}",
                    "estado": marca.get_estado_display(),
                    "monto": float(marca.monto_certificacion),
                    "dias_registro": marca.dias_desde_registro,
                },
                "historial_cambios": [
                    {
                        "fecha": h.fecha_cambio,
                        "estado_anterior": h.estado_anterior,
                        "estado_nuevo": h.estado_nuevo,
                        "responsable": h.usuario_responsable,
                        "observaciones": h.observaciones_cambio,
                    }
                    for h in historial
                ],
                "logos_generados": [
                    {
                        "modelo_ia": logo.modelo_ia_usado,
                        "calidad": logo.get_calidad_logo_display(),
                        "exito": logo.exito,
                        "fecha": logo.fecha_generacion,
                        "url": logo.url_logo,
                    }
                    for logo in logos
                ],
                "comparacion_regional": {
                    "promedio_cabezas_region": round(promedio_regional_cabezas, 2),
                    "promedio_monto_region": round(float(promedio_regional_monto), 2),
                    "posicion_cabezas": (
                        "superior"
                        if marca.cantidad_cabezas > promedio_regional_cabezas
                        else "inferior"
                    ),
                    "posicion_monto": (
                        "superior"
                        if marca.monto_certificacion > promedio_regional_monto
                        else "inferior"
                    ),
                },
            }

        except MarcaGanadoBovino.DoesNotExist:
            return {"error": "Marca no encontrada"}

    @staticmethod
    def exportar_datos_excel(filtros=None):
        """Prepara datos para exportación a Excel"""
        queryset = MarcaGanadoBovino.objects.all()

        if filtros:
            if filtros.get("departamento"):
                queryset = queryset.filter(departamento=filtros["departamento"])
            if filtros.get("raza_bovino"):
                queryset = queryset.filter(raza_bovino=filtros["raza_bovino"])
            if filtros.get("proposito_ganado"):
                queryset = queryset.filter(proposito_ganado=filtros["proposito_ganado"])
            if filtros.get("fecha_desde"):
                queryset = queryset.filter(fecha_registro__gte=filtros["fecha_desde"])
            if filtros.get("fecha_hasta"):
                queryset = queryset.filter(fecha_registro__lte=filtros["fecha_hasta"])

        datos_excel = []
        for marca in queryset:
            datos_excel.append(
                {
                    "Número de Marca": marca.numero_marca,
                    "Productor": marca.nombre_productor,
                    "CI Productor": marca.ci_productor,
                    "Teléfono": marca.telefono_productor,
                    "Raza Bovina": marca.get_raza_bovino_display(),
                    "Propósito": marca.get_proposito_ganado_display(),
                    "Cantidad Cabezas": marca.cantidad_cabezas,
                    "Departamento": marca.get_departamento_display(),
                    "Municipio": marca.municipio,
                    "Comunidad": marca.comunidad or "",
                    "Estado": marca.get_estado_display(),
                    "Monto Certificación": float(marca.monto_certificacion),
                    "Fecha Registro": marca.fecha_registro,
                    "Fecha Procesamiento": marca.fecha_procesamiento,
                    "Tiempo Procesamiento (hrs)": marca.tiempo_procesamiento_horas,
                    "Observaciones": marca.observaciones or "",
                }
            )

        return {
            "datos": datos_excel,
            "resumen": {
                "total_marcas": len(datos_excel),
                "total_cabezas": sum(d["Cantidad Cabezas"] for d in datos_excel),
                "total_ingresos": sum(
                    d["Monto Certificación"]
                    for d in datos_excel
                    if d["Estado"] == "Aprobado"
                ),
            },
        }
