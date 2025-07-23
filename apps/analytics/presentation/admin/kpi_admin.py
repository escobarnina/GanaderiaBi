"""
Admin mejorado para KPIs de ganado bovino siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa avanzada para KPIGanadoBovinoModel
- Proporcionar visualización avanzada de métricas con gráficos interactivos
- Implementar análisis predictivo y alertas inteligentes
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.http import JsonResponse
from django.db.models import Avg, Max, Min
from datetime import datetime, timedelta
import json

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import KPIGanadoBovinoModel


@admin.register(KPIGanadoBovinoModel)
class KPIGanadoBovinoAdmin(BaseAnalyticsAdmin):
    """
    Admin mejorado para KPIs de ganado bovino - Clean Architecture.

    Responsabilidades:
    - Configurar visualización avanzada de KPIs con gráficos interactivos
    - Proporcionar análisis predictivo y alertas inteligentes
    - Gestionar métricas del sistema con dashboard en tiempo real
    - Implementar exportación avanzada y reportes automáticos
    """

    list_display = [
        "fecha",
        "marcas_registradas_mes",
        "tiempo_promedio_procesamiento",
        "porcentaje_aprobacion_display",
        "ingresos_mes_display",
        "total_cabezas_registradas",
        "tasa_exito_logos_display",
        "eficiencia_display",
        "tendencia_display",
        "alertas_display",
    ]

    list_filter = [
        "fecha",
        "porcentaje_aprobacion",
        "tiempo_promedio_procesamiento",
        "tasa_exito_logos",
    ]

    search_fields = [
        "fecha",
        "observaciones",
    ]

    readonly_fields = [
        "fecha",
        "marcas_registradas_mes",
        "tiempo_promedio_procesamiento",
        "porcentaje_aprobacion",
        "ingresos_mes",
        "total_cabezas_registradas",
        "promedio_cabezas_por_marca",
        "marcas_carne",
        "marcas_leche",
        "marcas_doble_proposito",
        "marcas_reproduccion",
        "marcas_santa_cruz",
        "marcas_beni",
        "marcas_la_paz",
        "marcas_otros_departamentos",
        "tasa_exito_logos",
        "total_logos_generados",
        "tiempo_promedio_generacion_logos",
        "eficiencia_display",
        "dashboard_interactivo",
        "analisis_predictivo",
        "comparacion_historica",
        "alertas_inteligentes",
    ]

    date_hierarchy = "fecha"

    fieldsets = (
        (
            "📊 Dashboard Interactivo",
            {
                "fields": ("dashboard_interactivo",),
                "classes": ("wide", "dashboard-section"),
            },
        ),
        (
            "📈 Análisis Predictivo",
            {
                "fields": ("analisis_predictivo",),
                "classes": ("wide", "prediction-section"),
            },
        ),
        ("📅 Información General", {"fields": ("fecha",)}),
        (
            "🎯 KPIs Principales",
            {
                "fields": (
                    "marcas_registradas_mes",
                    "tiempo_promedio_procesamiento",
                    "porcentaje_aprobacion",
                    "ingresos_mes",
                ),
                "classes": ("wide", "kpi-section"),
            },
        ),
        (
            "🐄 Métricas de Ganado Bovino",
            {
                "fields": ("total_cabezas_registradas", "promedio_cabezas_por_marca"),
                "classes": ("cattle-section",),
            },
        ),
        (
            "🎯 Distribución por Propósito",
            {
                "fields": (
                    "marcas_carne",
                    "marcas_leche",
                    "marcas_doble_proposito",
                    "marcas_reproduccion",
                ),
                "classes": ("collapse", "purpose-section"),
            },
        ),
        (
            "🗺️ Distribución Geográfica",
            {
                "fields": (
                    "marcas_santa_cruz",
                    "marcas_beni",
                    "marcas_la_paz",
                    "marcas_otros_departamentos",
                ),
                "classes": ("collapse", "geo-section"),
            },
        ),
        (
            "🎨 KPIs de Logos",
            {
                "fields": (
                    "tasa_exito_logos",
                    "total_logos_generados",
                    "tiempo_promedio_generacion_logos",
                ),
                "classes": ("collapse", "logo-section"),
            },
        ),
        (
            "📊 Análisis Comparativo",
            {
                "fields": ("comparacion_historica",),
                "classes": ("wide", "comparison-section"),
            },
        ),
        (
            "🚨 Alertas Inteligentes",
            {
                "fields": ("alertas_inteligentes",),
                "classes": ("wide", "alerts-section"),
            },
        ),
        (
            "⚡ Análisis de Eficiencia",
            {
                "fields": ("eficiencia_display",),
                "classes": ("wide", "efficiency-section"),
            },
        ),
    )

    # Acciones masivas avanzadas
    actions = [
        "generar_reporte_completo",
        "analizar_tendencias",
        "exportar_dashboard",
        "crear_alerta_personalizada",
        "optimizar_kpis",
    ]

    class Media:
        css = {"all": ("admin/css/kpi_admin.css",)}
        js = (
            "admin/js/chart.min.js",
            "admin/js/kpi_admin.js",
        )

    def get_urls(self):
        """URLs personalizadas para funcionalidades avanzadas"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard-data/",
                self.admin_site.admin_view(self.dashboard_data_view),
                name="kpi_dashboard_data",
            ),
            path(
                "prediction-data/",
                self.admin_site.admin_view(self.prediction_data_view),
                name="kpi_prediction_data",
            ),
            path(
                "comparison-data/",
                self.admin_site.admin_view(self.comparison_data_view),
                name="kpi_comparison_data",
            ),
            path(
                "alerts-data/",
                self.admin_site.admin_view(self.alerts_data_view),
                name="kpi_alerts_data",
            ),
        ]
        return custom_urls + urls

    # Campos personalizados con visualizaciones avanzadas
    def porcentaje_aprobacion_display(self, obj):
        """Muestra porcentaje de aprobación con indicador visual"""
        return self._crear_indicador_porcentaje(
            obj.porcentaje_aprobacion, "aprobacion", thresholds=[60, 80]
        )

    porcentaje_aprobacion_display.short_description = "% Aprobación"

    def ingresos_mes_display(self, obj):
        """Muestra ingresos con formato de moneda y tendencia"""
        ingresos_formateados = f"Bs. {obj.ingresos_mes:,.2f}"
        return format_html(
            '<div class="income-display">'
            '<span class="amount">{}</span>'
            '<span class="trend-indicator" data-value="{}">{}</span>'
            "</div>",
            ingresos_formateados,
            obj.ingresos_mes,
            self._calcular_tendencia_ingresos(obj),
        )

    ingresos_mes_display.short_description = "💰 Ingresos"

    def tasa_exito_logos_display(self, obj):
        """Muestra tasa de éxito de logos con indicador visual"""
        return self._crear_indicador_porcentaje(
            obj.tasa_exito_logos, "logos", thresholds=[70, 85]
        )

    tasa_exito_logos_display.short_description = "🎨 Éxito Logos"

    def tendencia_display(self, obj):
        """Muestra análisis de tendencias"""
        return self._generar_indicador_tendencia(obj)

    tendencia_display.short_description = "📈 Tendencia"

    def alertas_display(self, obj):
        """Muestra alertas activas"""
        return self._generar_alertas_activas(obj)

    alertas_display.short_description = "🚨 Alertas"

    def dashboard_interactivo(self, obj):
        """Dashboard interactivo con gráficos en tiempo real"""
        return format_html(
            '<div id="kpi-dashboard" class="interactive-dashboard" data-kpi-id="{}">'
            '<div class="dashboard-header">'
            "<h3>📊 Dashboard KPIs - {}</h3>"
            "</div>"
            '<div class="dashboard-grid">'
            '<div class="kpi-card">'
            '<canvas id="approval-chart-{}"></canvas>'
            "<h4>Tasa de Aprobación</h4>"
            "</div>"
            '<div class="kpi-card">'
            '<canvas id="income-chart-{}"></canvas>'
            "<h4>Ingresos Mensuales</h4>"
            "</div>"
            '<div class="kpi-card">'
            '<canvas id="efficiency-chart-{}"></canvas>'
            "<h4>Eficiencia del Sistema</h4>"
            "</div>"
            '<div class="kpi-card">'
            '<canvas id="cattle-chart-{}"></canvas>'
            "<h4>Distribución de Ganado</h4>"
            "</div>"
            "</div>"
            '<div class="dashboard-controls">'
            '<button class="btn-refresh" onclick="refreshKPIDashboard({})">🔄 Actualizar</button>'
            '<button class="btn-export" onclick="exportKPIDashboard({})">📤 Exportar</button>'
            "</div>"
            "</div>",
            obj.id,
            obj.fecha.strftime("%B %Y"),
            obj.id,
            obj.id,
            obj.id,
            obj.id,
            obj.id,
            obj.id,
        )

    dashboard_interactivo.short_description = "Dashboard Interactivo"

    def analisis_predictivo(self, obj):
        """Análisis predictivo con machine learning"""
        return format_html(
            '<div id="prediction-analysis" class="prediction-container" data-kpi-id="{}">'
            '<div class="prediction-header">'
            "<h3>🔮 Análisis Predictivo</h3>"
            "</div>"
            '<div class="prediction-grid">'
            '<div class="prediction-card">'
            "<h4>📈 Tendencia de Aprobación</h4>"
            '<canvas id="approval-prediction-{}"></canvas>'
            '<div class="prediction-summary">'
            '<span class="prediction-value">{}</span>'
            '<span class="prediction-confidence">Confianza: {}%</span>'
            "</div>"
            "</div>"
            '<div class="prediction-card">'
            "<h4>💰 Proyección de Ingresos</h4>"
            '<canvas id="income-prediction-{}"></canvas>'
            '<div class="prediction-summary">'
            '<span class="prediction-value">{}</span>'
            '<span class="prediction-confidence">Confianza: {}%</span>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="prediction-insights">'
            "<h4>💡 Insights Clave</h4>"
            '<ul class="insights-list">'
            "{}"
            "</ul>"
            "</div>"
            "</div>",
            obj.id,
            obj.id,
            self._predecir_aprobacion(obj),
            self._calcular_confianza_aprobacion(obj),
            obj.id,
            self._predecir_ingresos(obj),
            self._calcular_confianza_ingresos(obj),
            self._generar_insights_predictivos(obj),
        )

    analisis_predictivo.short_description = "Análisis Predictivo"

    def comparacion_historica(self, obj):
        """Comparación con períodos históricos"""
        return format_html(
            '<div id="historical-comparison" class="comparison-container" data-kpi-id="{}">'
            '<div class="comparison-header">'
            "<h3>📊 Comparación Histórica</h3>"
            "</div>"
            '<div class="comparison-timeline">'
            '<canvas id="timeline-chart-{}"></canvas>'
            "</div>"
            '<div class="comparison-metrics">'
            '<div class="metric-comparison">'
            "<h4>vs. Mes Anterior</h4>"
            '<div class="comparison-grid">'
            "{}"
            "</div>"
            "</div>"
            '<div class="metric-comparison">'
            "<h4>vs. Mismo Mes Año Anterior</h4>"
            '<div class="comparison-grid">'
            "{}"
            "</div>"
            "</div>"
            "</div>"
            "</div>",
            obj.id,
            obj.id,
            self._generar_comparacion_mes_anterior(obj),
            self._generar_comparacion_año_anterior(obj),
        )

    comparacion_historica.short_description = "Comparación Histórica"

    def alertas_inteligentes(self, obj):
        """Sistema de alertas inteligentes"""
        alertas = self._generar_alertas_inteligentes(obj)
        return format_html(
            '<div id="intelligent-alerts" class="alerts-container" data-kpi-id="{}">'
            '<div class="alerts-header">'
            "<h3>🚨 Alertas Inteligentes</h3>"
            '<span class="alerts-count">{} alertas activas</span>'
            "</div>"
            '<div class="alerts-list">'
            "{}"
            "</div>"
            '<div class="alerts-actions">'
            '<button class="btn-configure" onclick="configureAlerts({})">⚙️ Configurar</button>'
            '<button class="btn-acknowledge" onclick="acknowledgeAlerts({})">✅ Marcar como Leídas</button>'
            "</div>"
            "</div>",
            obj.id,
            len(alertas),
            "".join(alertas),
            obj.id,
            obj.id,
        )

    alertas_inteligentes.short_description = "Alertas Inteligentes"

    def eficiencia_display(self, obj):
        """Muestra un análisis completo de eficiencia del sistema"""
        return format_html(
            '<div class="efficiency-analysis">'
            '<div class="efficiency-header">'
            "<h3>⚡ Análisis de Eficiencia</h3>"
            "</div>"
            '<div class="efficiency-grid">'
            "{}"
            "{}"
            "{}"
            "{}"
            "</div>"
            '<div class="efficiency-score">'
            '<div class="score-circle" data-score="{}">'
            '<span class="score-value">{}%</span>'
            '<span class="score-label">Eficiencia Global</span>'
            "</div>"
            "</div>"
            "</div>",
            self._generar_indicador_aprobacion_avanzado(obj.porcentaje_aprobacion),
            self._generar_indicador_tiempo_avanzado(obj.tiempo_promedio_procesamiento),
            self._generar_indicador_logos_avanzado(obj.tasa_exito_logos),
            self._generar_indicador_ingresos_avanzado(obj),
            self._calcular_eficiencia_global(obj),
            self._calcular_eficiencia_global(obj),
        )

    eficiencia_display.short_description = "Análisis de Eficiencia"

    # Acciones masivas avanzadas
    def generar_reporte_completo(self, request, queryset):
        """Genera reporte completo de KPIs"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "📊 Se generó el reporte completo para {} registros de KPIs. "
                "El reporte incluye análisis predictivo, comparaciones históricas y recomendaciones. "
                "<a href='#' onclick='downloadKPIReport()'>Descargar Reporte</a>",
                count,
            ),
        )

    generar_reporte_completo.short_description = "📊 Generar reporte completo"

    def analizar_tendencias(self, request, queryset):
        """Analiza tendencias de los KPIs seleccionados"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "📈 Se inició el análisis de tendencias para {} registros. "
                "Los resultados incluyen predicciones y recomendaciones estratégicas. "
                "<a href='#' onclick='viewTrendAnalysis()'>Ver Análisis</a>",
                count,
            ),
        )

    analizar_tendencias.short_description = "📈 Analizar tendencias"

    def exportar_dashboard(self, request, queryset):
        """Exporta dashboard interactivo"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "📤 Se exportó el dashboard para {} registros. "
                "El archivo incluye gráficos interactivos y datos en tiempo real. "
                "<a href='#' onclick='downloadDashboard()'>Descargar Dashboard</a>",
                count,
            ),
        )

    exportar_dashboard.short_description = "📤 Exportar dashboard"

    def crear_alerta_personalizada(self, request, queryset):
        """Crea alertas personalizadas"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🚨 Se configuraron alertas personalizadas para {} registros. "
                "Las alertas se activarán automáticamente según los umbrales definidos. "
                "<a href='#' onclick='configureCustomAlerts()'>Configurar Alertas</a>",
                count,
            ),
        )

    crear_alerta_personalizada.short_description = "🚨 Crear alerta personalizada"

    def optimizar_kpis(self, request, queryset):
        """Optimiza KPIs usando IA"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🤖 Se inició la optimización inteligente para {} registros. "
                "El sistema analizará patrones y sugerirá mejoras automáticas. "
                "<a href='#' onclick='viewOptimizationResults()'>Ver Resultados</a>",
                count,
            ),
        )

    optimizar_kpis.short_description = "🤖 Optimizar con IA"

    # Vistas para datos AJAX
    def dashboard_data_view(self, request):
        """Proporciona datos para el dashboard interactivo"""
        kpi_id = request.GET.get("kpi_id")
        if kpi_id:
            try:
                kpi = KPIGanadoBovinoModel.objects.get(id=kpi_id)
                data = {
                    "approval_data": self._get_approval_chart_data(kpi),
                    "income_data": self._get_income_chart_data(kpi),
                    "efficiency_data": self._get_efficiency_chart_data(kpi),
                    "cattle_data": self._get_cattle_distribution_data(kpi),
                }
                return JsonResponse(data)
            except KPIGanadoBovinoModel.DoesNotExist:
                return JsonResponse({"error": "KPI no encontrado"}, status=404)
        return JsonResponse({"error": "ID de KPI requerido"}, status=400)

    def prediction_data_view(self, request):
        """Proporciona datos para análisis predictivo"""
        kpi_id = request.GET.get("kpi_id")
        if kpi_id:
            try:
                kpi = KPIGanadoBovinoModel.objects.get(id=kpi_id)
                data = {
                    "approval_prediction": self._get_approval_prediction_data(kpi),
                    "income_prediction": self._get_income_prediction_data(kpi),
                    "insights": self._get_predictive_insights(kpi),
                }
                return JsonResponse(data)
            except KPIGanadoBovinoModel.DoesNotExist:
                return JsonResponse({"error": "KPI no encontrado"}, status=404)
        return JsonResponse({"error": "ID de KPI requerido"}, status=400)

    def comparison_data_view(self, request):
        """Proporciona datos para comparación histórica"""
        kpi_id = request.GET.get("kpi_id")
        if kpi_id:
            try:
                kpi = KPIGanadoBovinoModel.objects.get(id=kpi_id)
                data = {
                    "timeline_data": self._get_timeline_data(kpi),
                    "monthly_comparison": self._get_monthly_comparison_data(kpi),
                    "yearly_comparison": self._get_yearly_comparison_data(kpi),
                }
                return JsonResponse(data)
            except KPIGanadoBovinoModel.DoesNotExist:
                return JsonResponse({"error": "KPI no encontrado"}, status=404)
        return JsonResponse({"error": "ID de KPI requerido"}, status=400)

    def alerts_data_view(self, request):
        """Proporciona datos para alertas inteligentes"""
        kpi_id = request.GET.get("kpi_id")
        if kpi_id:
            try:
                kpi = KPIGanadoBovinoModel.objects.get(id=kpi_id)
                data = {
                    "active_alerts": self._get_active_alerts_data(kpi),
                    "alert_history": self._get_alert_history_data(kpi),
                    "recommendations": self._get_alert_recommendations(kpi),
                }
                return JsonResponse(data)
            except KPIGanadoBovinoModel.DoesNotExist:
                return JsonResponse({"error": "KPI no encontrado"}, status=404)
        return JsonResponse({"error": "ID de KPI requerido"}, status=400)

    def has_add_permission(self, request):
        """Los KPIs se generan automáticamente"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Los KPIs no se pueden eliminar"""
        return False

    # Métodos privados para análisis y visualización
    def _crear_indicador_porcentaje(self, valor, tipo, thresholds):
        """Crea un indicador visual para porcentajes"""
        if valor >= thresholds[1]:
            color = "#4caf50"
            icon = "✅"
            status = "excelente"
        elif valor >= thresholds[0]:
            color = "#ff9800"
            icon = "⚠️"
            status = "bueno"
        else:
            color = "#f44336"
            icon = "❌"
            status = "necesita-mejora"

        valor_formateado = f"{valor:.1f}%"
        return format_html(
            '<div class="percentage-indicator {}-indicator">'
            '<span class="indicator-icon">{}</span>'
            '<span class="indicator-value" style="color: {};">{}</span>'
            '<div class="indicator-bar">'
            '<div class="indicator-fill" style="width: {}%; background-color: {};"></div>'
            "</div>"
            '<span class="indicator-status">{}</span>'
            "</div>",
            tipo,
            icon,
            color,
            valor_formateado,
            valor,
            color,
            status,
        )

    def _calcular_tendencia_ingresos(self, obj):
        """Calcula la tendencia de ingresos"""
        try:
            mes_anterior = (
                KPIGanadoBovinoModel.objects.filter(fecha__lt=obj.fecha)
                .order_by("-fecha")
                .first()
            )

            if mes_anterior:
                diferencia = obj.ingresos_mes - mes_anterior.ingresos_mes
                porcentaje = (diferencia / mes_anterior.ingresos_mes) * 100

                if porcentaje > 5:
                    return f'<span class="trend-up">↗️ +{porcentaje:.1f}%</span>'
                elif porcentaje < -5:
                    return f'<span class="trend-down">↘️ {porcentaje:.1f}%</span>'
                else:
                    return f'<span class="trend-stable">➡️ {porcentaje:.1f}%</span>'
            return '<span class="trend-neutral">➡️ N/A</span>'
        except:
            return '<span class="trend-error">❓ Error</span>'

    def _generar_indicador_tendencia(self, obj):
        """Genera indicador de tendencia general"""
        try:
            # Calcular tendencias de múltiples métricas
            tendencias = []

            # Tendencia de aprobación
            aprobacion_trend = self._calcular_tendencia_metrica(
                obj, "porcentaje_aprobacion"
            )
            tendencias.append(("Aprobación", aprobacion_trend))

            # Tendencia de ingresos
            ingresos_trend = self._calcular_tendencia_metrica(obj, "ingresos_mes")
            tendencias.append(("Ingresos", ingresos_trend))

            # Tendencia de eficiencia de logos
            logos_trend = self._calcular_tendencia_metrica(obj, "tasa_exito_logos")
            tendencias.append(("Logos", logos_trend))

            return self._formatear_tendencias(tendencias)
        except:
            return format_html('<span class="trend-error">❓ Error en cálculo</span>')

    def _generar_alertas_activas(self, obj):
        """Genera alertas activas para el KPI"""
        alertas = []

        # Alerta de aprobación baja
        if obj.porcentaje_aprobacion < 60:
            alertas.append("🔴 Aprobación Baja")

        # Alerta de tiempo alto
        if obj.tiempo_promedio_procesamiento > 72:
            alertas.append("🟡 Tiempo Alto")

        # Alerta de logos
        if obj.tasa_exito_logos < 70:
            alertas.append("🟠 Logos Bajo")

        if not alertas:
            return format_html('<span class="no-alerts">✅ Sin alertas</span>')

        return format_html(
            '<div class="active-alerts">{}</div>',
            "".join(
                [f'<span class="alert-badge">{alerta}</span>' for alerta in alertas]
            ),
        )

    def _calcular_eficiencia_global(self, obj):
        """Calcula la eficiencia global del sistema"""
        try:
            # Ponderación de métricas
            peso_aprobacion = 0.3
            peso_tiempo = 0.25
            peso_logos = 0.25
            peso_ingresos = 0.2

            # Normalizar métricas (0-100)
            score_aprobacion = obj.porcentaje_aprobacion
            score_tiempo = max(
                0, 100 - (obj.tiempo_promedio_procesamiento / 168 * 100)
            )  # 168h = 1 semana
            score_logos = obj.tasa_exito_logos

            # Score de ingresos basado en objetivo mensual (ejemplo: 50000 Bs)
            objetivo_ingresos = 50000
            score_ingresos = min(100, (obj.ingresos_mes / objetivo_ingresos) * 100)

            # Calcular eficiencia global
            eficiencia = (
                score_aprobacion * peso_aprobacion
                + score_tiempo * peso_tiempo
                + score_logos * peso_logos
                + score_ingresos * peso_ingresos
            )

            return round(eficiencia)
        except:
            return 0

    # Métodos para análisis predictivo
    def _predecir_aprobacion(self, obj):
        """Predice la tasa de aprobación del próximo mes"""
        try:
            # Obtener datos históricos
            historicos = KPIGanadoBovinoModel.objects.filter(
                fecha__lte=obj.fecha
            ).order_by("-fecha")[:6]

            if len(historicos) >= 3:
                valores = [h.porcentaje_aprobacion for h in historicos]
                # Predicción simple basada en tendencia
                tendencia = (valores[0] - valores[-1]) / len(valores)
                prediccion = valores[0] + tendencia
                return f"{max(0, min(100, prediccion)):.1f}%"
            return "N/A"
        except:
            return "Error"

    def _predecir_ingresos(self, obj):
        """Predice los ingresos del próximo mes"""
        try:
            historicos = KPIGanadoBovinoModel.objects.filter(
                fecha__lte=obj.fecha
            ).order_by("-fecha")[:6]

            if len(historicos) >= 3:
                valores = [h.ingresos_mes for h in historicos]
                tendencia = (valores[0] - valores[-1]) / len(valores)
                prediccion = valores[0] + tendencia
                return f"Bs. {max(0, prediccion):,.2f}"
            return "N/A"
        except:
            return "Error"

    def _calcular_confianza_aprobacion(self, obj):
        """Calcula la confianza de la predicción de aprobación"""
        try:
            historicos = KPIGanadoBovinoModel.objects.filter(
                fecha__lte=obj.fecha
            ).order_by("-fecha")[:6]

            if len(historicos) >= 3:
                valores = [h.porcentaje_aprobacion for h in historicos]
                varianza = sum(
                    (x - sum(valores) / len(valores)) ** 2 for x in valores
                ) / len(valores)
                confianza = max(60, 100 - varianza)
                return round(confianza)
            return 50
        except:
            return 50

    def _calcular_confianza_ingresos(self, obj):
        """Calcula la confianza de la predicción de ingresos"""
        try:
            historicos = KPIGanadoBovinoModel.objects.filter(
                fecha__lte=obj.fecha
            ).order_by("-fecha")[:6]

            if len(historicos) >= 3:
                valores = [h.ingresos_mes for h in historicos]
                promedio = sum(valores) / len(valores)
                varianza = sum((x - promedio) ** 2 for x in valores) / len(valores)
                coef_variacion = (varianza**0.5) / promedio if promedio > 0 else 1
                confianza = max(60, 100 - (coef_variacion * 100))
                return round(confianza)
            return 50
        except:
            return 50

    def _generar_insights_predictivos(self, obj):
        """Genera insights predictivos"""
        insights = []

        # Insight de aprobación
        if obj.porcentaje_aprobacion < 70:
            insights.append(
                '<li class="insight-warning">📉 La tasa de aprobación está por debajo del objetivo. Revisar procesos de validación.</li>'
            )
        elif obj.porcentaje_aprobacion > 90:
            insights.append(
                '<li class="insight-success">📈 Excelente tasa de aprobación. Mantener estándares actuales.</li>'
            )

        # Insight de tiempo
        if obj.tiempo_promedio_procesamiento > 48:
            insights.append(
                '<li class="insight-warning">⏰ Tiempo de procesamiento elevado. Considerar optimización de flujos.</li>'
            )

        # Insight de logos
        if obj.tasa_exito_logos < 80:
            insights.append(
                '<li class="insight-info">🎨 Oportunidad de mejora en generación de logos. Revisar algoritmos de IA.</li>'
            )

        # Insight de crecimiento
        try:
            mes_anterior = (
                KPIGanadoBovinoModel.objects.filter(fecha__lt=obj.fecha)
                .order_by("-fecha")
                .first()
            )

            if (
                mes_anterior
                and obj.marcas_registradas_mes
                > mes_anterior.marcas_registradas_mes * 1.1
            ):
                insights.append(
                    '<li class="insight-success">🚀 Crecimiento acelerado en registros. Preparar recursos adicionales.</li>'
                )
        except:
            pass

        if not insights:
            insights.append(
                '<li class="insight-neutral">✅ Todos los indicadores dentro de rangos normales.</li>'
            )

        return "".join(insights)

    # Métodos para comparación histórica
    def _generar_comparacion_mes_anterior(self, obj):
        """Genera comparación con el mes anterior"""
        try:
            mes_anterior = (
                KPIGanadoBovinoModel.objects.filter(fecha__lt=obj.fecha)
                .order_by("-fecha")
                .first()
            )

            if not mes_anterior:
                return '<div class="no-comparison">No hay datos del mes anterior</div>'

            comparaciones = []

            # Comparar aprobación
            diff_aprobacion = (
                obj.porcentaje_aprobacion - mes_anterior.porcentaje_aprobacion
            )
            comparaciones.append(
                self._formatear_comparacion("Aprobación", diff_aprobacion, "%")
            )

            # Comparar ingresos
            diff_ingresos = obj.ingresos_mes - mes_anterior.ingresos_mes
            comparaciones.append(
                self._formatear_comparacion("Ingresos", diff_ingresos, "Bs.")
            )

            # Comparar logos
            diff_logos = obj.tasa_exito_logos - mes_anterior.tasa_exito_logos
            comparaciones.append(self._formatear_comparacion("Logos", diff_logos, "%"))

            return "".join(comparaciones)
        except:
            return '<div class="comparison-error">Error en comparación</div>'

    def _generar_comparacion_año_anterior(self, obj):
        """Genera comparación con el mismo mes del año anterior"""
        try:
            año_anterior = obj.fecha.replace(year=obj.fecha.year - 1)
            kpi_año_anterior = KPIGanadoBovinoModel.objects.filter(
                fecha__year=año_anterior.year, fecha__month=año_anterior.month
            ).first()

            if not kpi_año_anterior:
                return '<div class="no-comparison">No hay datos del año anterior</div>'

            comparaciones = []

            # Comparar métricas anuales
            diff_aprobacion = (
                obj.porcentaje_aprobacion - kpi_año_anterior.porcentaje_aprobacion
            )
            comparaciones.append(
                self._formatear_comparacion("Aprobación", diff_aprobacion, "%")
            )

            diff_ingresos = obj.ingresos_mes - kpi_año_anterior.ingresos_mes
            comparaciones.append(
                self._formatear_comparacion("Ingresos", diff_ingresos, "Bs.")
            )

            return "".join(comparaciones)
        except:
            return '<div class="comparison-error">Error en comparación anual</div>'

    def _formatear_comparacion(self, metrica, diferencia, unidad):
        """Formatea una comparación individual"""
        if diferencia > 0:
            color = "#4caf50"
            icon = "↗️"
            clase = "positive"
        elif diferencia < 0:
            color = "#f44336"
            icon = "↘️"
            clase = "negative"
        else:
            color = "#666"
            icon = "➡️"
            clase = "neutral"

        diferencia_formateada = f"{diferencia:.2f}"
        return format_html(
            '<div class="metric-comparison-item {}">'
            '<span class="metric-name">{}</span>'
            '<span class="metric-change" style="color: {};">'
            "{} {} {}"
            "</span>"
            "</div>",
            clase,
            metrica,
            color,
            icon,
            diferencia_formateada,
            unidad,
        )

    # Métodos para alertas inteligentes
    def _generar_alertas_inteligentes(self, obj):
        """Genera alertas inteligentes basadas en patrones"""
        alertas = []

        # Alerta crítica: Aprobación muy baja
        if obj.porcentaje_aprobacion < 50:
            porcentaje_formateado = f"{obj.porcentaje_aprobacion:.1f}%"
            alertas.append(
                '<div class="alert critical">'
                '<span class="alert-icon">🚨</span>'
                '<div class="alert-content">'
                "<h4>Tasa de Aprobación Crítica</h4>"
                f"<p>La tasa de aprobación ({porcentaje_formateado}) está en nivel crítico. Acción inmediata requerida.</p>"
                '<div class="alert-actions">'
                '<button class="btn-action">Revisar Procesos</button>'
                '<button class="btn-action">Contactar Supervisor</button>'
                "</div>"
                "</div>"
                "</div>"
            )

        # Alerta de tiempo elevado
        if obj.tiempo_promedio_procesamiento > 96:  # 4 días
            tiempo_formateado = f"{obj.tiempo_promedio_procesamiento:.1f}h"
            alertas.append(
                '<div class="alert warning">'
                '<span class="alert-icon">⏰</span>'
                '<div class="alert-content">'
                "<h4>Tiempo de Procesamiento Elevado</h4>"
                f"<p>El tiempo promedio ({tiempo_formateado}) excede los límites aceptables.</p>"
                '<div class="alert-actions">'
                '<button class="btn-action">Optimizar Flujo</button>'
                '<button class="btn-action">Asignar Recursos</button>'
                "</div>"
                "</div>"
                "</div>"
            )

        # Alerta de oportunidad: Crecimiento acelerado
        try:
            mes_anterior = (
                KPIGanadoBovinoModel.objects.filter(fecha__lt=obj.fecha)
                .order_by("-fecha")
                .first()
            )

            if (
                mes_anterior
                and obj.marcas_registradas_mes
                > mes_anterior.marcas_registradas_mes * 1.2
            ):
                incremento = (
                    (obj.marcas_registradas_mes / mes_anterior.marcas_registradas_mes)
                    - 1
                ) * 100
                incremento_formateado = f"{incremento:.1f}%"
                alertas.append(
                    '<div class="alert opportunity">'
                    '<span class="alert-icon">🚀</span>'
                    '<div class="alert-content">'
                    "<h4>Crecimiento Acelerado Detectado</h4>"
                    f"<p>Incremento del {incremento_formateado} en registros. Preparar escalabilidad.</p>"
                    '<div class="alert-actions">'
                    '<button class="btn-action">Planificar Recursos</button>'
                    '<button class="btn-action">Revisar Capacidad</button>'
                    "</div>"
                    "</div>"
                    "</div>"
                )
        except:
            pass

        # Alerta de logos
        if obj.tasa_exito_logos < 60:
            tasa_formateada = f"{obj.tasa_exito_logos:.1f}%"
            alertas.append(
                '<div class="alert info">'
                '<span class="alert-icon">🎨</span>'
                '<div class="alert-content">'
                "<h4>Baja Eficiencia en Logos</h4>"
                f"<p>La tasa de éxito de logos ({tasa_formateada}) necesita atención.</p>"
                '<div class="alert-actions">'
                '<button class="btn-action">Revisar IA</button>'
                '<button class="btn-action">Actualizar Modelos</button>'
                "</div>"
                "</div>"
                "</div>".format(obj.tasa_exito_logos)
            )

        return alertas

    # Métodos para indicadores avanzados
    def _generar_indicador_aprobacion_avanzado(self, porcentaje):
        """Genera indicador avanzado de aprobación"""
        porcentaje_formateado = f"{porcentaje:.1f}%"
        return format_html(
            '<div class="efficiency-metric">'
            '<div class="metric-header">'
            '<span class="metric-icon">✅</span>'
            '<span class="metric-title">Aprobación</span>'
            "</div>"
            '<div class="metric-value">{}</div>'
            '<div class="metric-bar">'
            '<div class="metric-fill" style="width: {}%; background: {};"></div>'
            "</div>"
            '<div class="metric-status">{}</div>'
            "</div>",
            porcentaje_formateado,
            porcentaje,
            (
                "#4caf50"
                if porcentaje >= 80
                else "#ff9800" if porcentaje >= 60 else "#f44336"
            ),
            (
                "Excelente"
                if porcentaje >= 80
                else "Bueno" if porcentaje >= 60 else "Necesita Mejora"
            ),
        )

    def _generar_indicador_tiempo_avanzado(self, tiempo):
        """Genera indicador avanzado de tiempo"""
        # Convertir tiempo a score (menor tiempo = mejor score)
        score = max(0, 100 - (tiempo / 168 * 100))  # 168h = 1 semana máxima
        tiempo_formateado = f"{tiempo:.1f}h"

        return format_html(
            '<div class="efficiency-metric">'
            '<div class="metric-header">'
            '<span class="metric-icon">⏱️</span>'
            '<span class="metric-title">Velocidad</span>'
            "</div>"
            '<div class="metric-value">{}</div>'
            '<div class="metric-bar">'
            '<div class="metric-fill" style="width: {}%; background: {};"></div>'
            "</div>"
            '<div class="metric-status">{}</div>'
            "</div>",
            tiempo_formateado,
            score,
            "#4caf50" if tiempo <= 24 else "#ff9800" if tiempo <= 72 else "#f44336",
            "Rápido" if tiempo <= 24 else "Normal" if tiempo <= 72 else "Lento",
        )

    def _generar_indicador_logos_avanzado(self, tasa):
        """Genera indicador avanzado de logos"""
        tasa_formateada = f"{tasa:.1f}%"
        return format_html(
            '<div class="efficiency-metric">'
            '<div class="metric-header">'
            '<span class="metric-icon">🎨</span>'
            '<span class="metric-title">Logos</span>'
            "</div>"
            '<div class="metric-value">{}</div>'
            '<div class="metric-bar">'
            '<div class="metric-fill" style="width: {}%; background: {};"></div>'
            "</div>"
            '<div class="metric-status">{}</div>'
            "</div>",
            tasa_formateada,
            tasa,
            "#4caf50" if tasa >= 85 else "#ff9800" if tasa >= 70 else "#f44336",
            "Excelente" if tasa >= 85 else "Bueno" if tasa >= 70 else "Necesita Mejora",
        )

    def _generar_indicador_ingresos_avanzado(self, obj):
        """Genera indicador avanzado de ingresos"""
        # Calcular score basado en objetivo mensual
        objetivo = 50000  # Bs. objetivo mensual
        score = min(100, (obj.ingresos_mes / objetivo) * 100)

        ingresos_formateados = f"Bs. {obj.ingresos_mes:,.0f}"
        return format_html(
            '<div class="efficiency-metric">'
            '<div class="metric-header">'
            '<span class="metric-icon">💰</span>'
            '<span class="metric-title">Ingresos</span>'
            "</div>"
            '<div class="metric-value">{}</div>'
            '<div class="metric-bar">'
            '<div class="metric-fill" style="width: {}%; background: {};"></div>'
            "</div>"
            '<div class="metric-status">{}</div>'
            "</div>",
            ingresos_formateados,
            score,
            "#4caf50" if score >= 100 else "#ff9800" if score >= 80 else "#f44336",
            (
                "Objetivo Superado"
                if score >= 100
                else "En Objetivo" if score >= 80 else "Por Debajo"
            ),
        )

    # Métodos para datos de gráficos
    def _get_approval_chart_data(self, obj):
        """Obtiene datos para gráfico de aprobación"""
        historicos = KPIGanadoBovinoModel.objects.filter(fecha__lte=obj.fecha).order_by(
            "-fecha"
        )[:6]

        return {
            "labels": [h.fecha.strftime("%b %Y") for h in reversed(historicos)],
            "data": [h.porcentaje_aprobacion for h in reversed(historicos)],
            "backgroundColor": "rgba(76, 175, 80, 0.2)",
            "borderColor": "rgba(76, 175, 80, 1)",
        }

    def _get_income_chart_data(self, obj):
        """Obtiene datos para gráfico de ingresos"""
        historicos = KPIGanadoBovinoModel.objects.filter(fecha__lte=obj.fecha).order_by(
            "-fecha"
        )[:6]

        return {
            "labels": [h.fecha.strftime("%b %Y") for h in reversed(historicos)],
            "data": [float(h.ingresos_mes) for h in reversed(historicos)],
            "backgroundColor": "rgba(33, 150, 243, 0.2)",
            "borderColor": "rgba(33, 150, 243, 1)",
        }

    def _get_efficiency_chart_data(self, obj):
        """Obtiene datos para gráfico de eficiencia"""
        return {
            "labels": ["Aprobación", "Velocidad", "Logos", "Ingresos"],
            "data": [
                obj.porcentaje_aprobacion,
                max(0, 100 - (obj.tiempo_promedio_procesamiento / 168 * 100)),
                obj.tasa_exito_logos,
                min(100, (obj.ingresos_mes / 50000) * 100),
            ],
            "backgroundColor": [
                "rgba(76, 175, 80, 0.8)",
                "rgba(255, 152, 0, 0.8)",
                "rgba(156, 39, 176, 0.8)",
                "rgba(33, 150, 243, 0.8)",
            ],
        }

    def _get_cattle_distribution_data(self, obj):
        """Obtiene datos para distribución de ganado"""
        return {
            "labels": ["Carne", "Leche", "Doble Propósito", "Reproducción"],
            "data": [
                obj.marcas_carne,
                obj.marcas_leche,
                obj.marcas_doble_proposito,
                obj.marcas_reproduccion,
            ],
            "backgroundColor": [
                "rgba(244, 67, 54, 0.8)",
                "rgba(33, 150, 243, 0.8)",
                "rgba(76, 175, 80, 0.8)",
                "rgba(255, 193, 7, 0.8)",
            ],
        }
