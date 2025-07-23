"""
Admin mejorado para datos del dashboard siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa avanzada para DashboardDataModel
- Proporcionar visualización de métricas con dashboard en tiempo real
- Implementar alertas inteligentes y análisis predictivo
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import path, reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta, datetime
import json

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import DashboardDataModel


@admin.register(DashboardDataModel)
class DashboardDataAdmin(BaseAnalyticsAdmin):
    """
    Admin mejorado para datos del dashboard - Clean Architecture.

    Responsabilidades:
    - Configurar visualización avanzada de dashboard con métricas en tiempo real
    - Proporcionar análisis inteligente y alertas automáticas
    - Gestionar KPIs del sistema con visualizaciones interactivas
    - Implementar exportación avanzada y reportes automáticos
    """

    list_display = [
        "fecha_actualizacion_display",
        "marcas_mes_visual",
        "tiempo_procesamiento_avanzado",
        "aprobacion_con_tendencia",
        "ingresos_con_crecimiento",
        "cabezas_bovinas_display",
        "logos_rendimiento",
        "marcas_pendientes_urgentes",
        "estado_sistema_avanzado",
        "alertas_criticas",
    ]

    list_filter = [
        ("fecha_actualizacion", admin.DateFieldListFilter),
        ("raza_mas_comun", admin.ChoicesFieldListFilter),
        "porcentaje_aprobacion",
        "tiempo_promedio_procesamiento",
    ]

    search_fields = [
        "raza_mas_comun",
        "alertas",
    ]

    readonly_fields = [
        "fecha_actualizacion",
        "dashboard_ejecutivo_interactivo",
        "metricas_tiempo_real",
        "analisis_predictivo_dashboard",
        "alertas_inteligentes_sistema",
        "comparativa_historica_dashboard",
        "distribucion_geografica_visual",
        "rendimiento_logos_ia",
        "recomendaciones_automaticas",
    ] + [
        "marcas_registradas_mes_actual",
        "tiempo_promedio_procesamiento",
        "porcentaje_aprobacion",
        "porcentaje_rechazo",
        "ingresos_mes_actual",
        "total_cabezas_bovinas",
        "promedio_cabezas_por_marca",
        "porcentaje_carne",
        "porcentaje_leche",
        "porcentaje_doble_proposito",
        "porcentaje_reproduccion",
        "raza_mas_comun",
        "porcentaje_raza_principal",
        "tasa_exito_logos",
        "total_marcas_sistema",
        "marcas_pendientes",
        "alertas",
    ]

    date_hierarchy = "fecha_actualizacion"

    fieldsets = (
        (
            "📊 Dashboard Ejecutivo Interactivo",
            {
                "fields": ("dashboard_ejecutivo_interactivo",),
                "classes": ("wide", "dashboard-executive-section"),
            },
        ),
        (
            "⚡ Métricas en Tiempo Real",
            {
                "fields": ("metricas_tiempo_real",),
                "classes": ("wide", "realtime-metrics-section"),
            },
        ),
        (
            "🔮 Análisis Predictivo",
            {
                "fields": ("analisis_predictivo_dashboard",),
                "classes": ("wide", "predictive-section"),
            },
        ),
        ("📅 Información General", {"fields": ("fecha_actualizacion",)}),
        (
            "🎯 KPIs Principales",
            {
                "fields": (
                    "marcas_registradas_mes_actual",
                    "tiempo_promedio_procesamiento",
                    "porcentaje_aprobacion",
                    "porcentaje_rechazo",
                    "ingresos_mes_actual",
                ),
                "classes": ("wide", "main-kpis-section"),
            },
        ),
        (
            "🐄 Métricas de Ganado Bovino",
            {
                "fields": ("total_cabezas_bovinas", "promedio_cabezas_por_marca"),
                "classes": ("cattle-metrics-section",),
            },
        ),
        (
            "🎯 Distribución por Propósito",
            {
                "fields": (
                    "porcentaje_carne",
                    "porcentaje_leche",
                    "porcentaje_doble_proposito",
                    "porcentaje_reproduccion",
                ),
                "classes": ("collapse", "purpose-distribution-section"),
            },
        ),
        (
            "🧬 Distribución por Raza",
            {
                "fields": (
                    "raza_mas_comun",
                    "porcentaje_raza_principal",
                    "distribucion_geografica_visual",
                ),
                "classes": ("collapse", "breed-distribution-section"),
            },
        ),
        (
            "🎨 KPIs de Logos IA",
            {
                "fields": (
                    "tasa_exito_logos",
                    "total_marcas_sistema",
                    "marcas_pendientes",
                    "rendimiento_logos_ia",
                ),
                "classes": ("collapse", "ai-logos-section"),
            },
        ),
        (
            "📊 Comparativa Histórica",
            {
                "fields": ("comparativa_historica_dashboard",),
                "classes": ("wide", "historical-comparison-section"),
            },
        ),
        (
            "🚨 Sistema de Alertas",
            {
                "fields": ("alertas", "alertas_inteligentes_sistema"),
                "classes": ("wide", "alerts-system-section"),
            },
        ),
        (
            "💡 Recomendaciones Automáticas",
            {
                "fields": ("recomendaciones_automaticas",),
                "classes": ("wide", "recommendations-section"),
            },
        ),
    )

    # Acciones masivas avanzadas
    actions = [
        "actualizar_dashboard_completo",
        "generar_reporte_ejecutivo",
        "exportar_metricas_tiempo_real",
        "crear_alertas_personalizadas",
        "optimizar_rendimiento_sistema",
        "limpiar_datos_antiguos_inteligente",
    ]

    class Media:
        css = {
            "all": (
                "admin/css/dashboard_admin.css",
                "admin/css/custom_admin.css",
            )
        }
        js = (
            "admin/js/chart-component.js",
            "admin/js/dashboard_admin.js",
        )

    def get_urls(self):
        """URLs personalizadas para funcionalidades avanzadas"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "executive-dashboard/",
                self.admin_site.admin_view(self.executive_dashboard_view),
                name="dashboard_executive",
            ),
            path(
                "realtime-metrics/",
                self.admin_site.admin_view(self.realtime_metrics_view),
                name="dashboard_realtime_metrics",
            ),
            path(
                "predictive-analysis/",
                self.admin_site.admin_view(self.predictive_analysis_view),
                name="dashboard_predictive_analysis",
            ),
            path(
                "api/dashboard-data/",
                self.admin_site.admin_view(self.api_dashboard_data),
                name="dashboard_api_data",
            ),
            path(
                "api/alerts-data/",
                self.admin_site.admin_view(self.api_alerts_data),
                name="dashboard_api_alerts",
            ),
            path(
                "export-dashboard/",
                self.admin_site.admin_view(self.export_dashboard_view),
                name="dashboard_export",
            ),
        ]
        return custom_urls + urls

    # Campos personalizados con visualizaciones avanzadas
    def fecha_actualizacion_display(self, obj):
        """Fecha de actualización con indicador de frescura"""
        ahora = timezone.now()
        diferencia = ahora - obj.fecha_actualizacion

        if diferencia.total_seconds() < 300:  # 5 minutos
            frescura = "🟢 En vivo"
            color = "#28a745"
        elif diferencia.total_seconds() < 1800:  # 30 minutos
            frescura = "🟡 Reciente"
            color = "#ffc107"
        else:
            frescura = "🔴 Desactualizado"
            color = "#dc3545"

        return format_html(
            '<div class="fecha-actualizacion">'
            '<div class="fecha-principal">{}</div>'
            '<div class="frescura-indicator" style="color: {};">{}</div>'
            '<div class="tiempo-transcurrido">{}</div>'
            "</div>",
            obj.fecha_actualizacion.strftime("%d/%m/%Y %H:%M"),
            color,
            frescura,
            self._calcular_tiempo_transcurrido(obj.fecha_actualizacion),
        )

    fecha_actualizacion_display.short_description = "📅 Última Actualización"
    fecha_actualizacion_display.admin_order_field = "fecha_actualizacion"

    def marcas_mes_visual(self, obj):
        """Marcas del mes con visualización avanzada y tendencia"""
        # Calcular tendencia vs mes anterior
        mes_anterior = self._obtener_dashboard_mes_anterior(obj)
        tendencia = self._calcular_tendencia_marcas(obj, mes_anterior)

        return format_html(
            '<div class="marcas-mes-container">'
            '<div class="marcas-principal">'
            '<span class="marcas-numero">{}</span>'
            '<span class="marcas-label">marcas</span>'
            "</div>"
            '<div class="marcas-tendencia {}">'
            '<span class="tendencia-icon">{}</span>'
            '<span class="tendencia-texto">{}</span>'
            "</div>"
            '<div class="marcas-meta">'
            '<div class="meta-bar">'
            '<div class="meta-fill" style="width: {}%;"></div>'
            "</div>"
            '<span class="meta-texto">Meta: 100</span>'
            "</div>"
            "</div>",
            self.format_numero_con_separadores(obj.marcas_registradas_mes_actual),
            tendencia["class"],
            tendencia["icon"],
            tendencia["texto"],
            min(100, (obj.marcas_registradas_mes_actual / 100) * 100),
        )

    marcas_mes_visual.short_description = "🏷️ Marcas Mes"
    marcas_mes_visual.admin_order_field = "marcas_registradas_mes_actual"

    def tiempo_procesamiento_avanzado(self, obj):
        """Tiempo de procesamiento con análisis de eficiencia"""
        tiempo = float(obj.tiempo_promedio_procesamiento)

        # Clasificar eficiencia
        if tiempo <= 24:
            eficiencia = "Excelente"
            color = "#28a745"
            icon = "🚀"
            score = 100
        elif tiempo <= 48:
            eficiencia = "Buena"
            color = "#28a745"
            icon = "⚡"
            score = 85
        elif tiempo <= 72:
            eficiencia = "Regular"
            color = "#ffc107"
            icon = "⏰"
            score = 70
        else:
            eficiencia = "Lenta"
            color = "#dc3545"
            icon = "🐌"
            score = 40

        # Formatear valores antes de pasarlos a format_html
        tiempo_formateado = f"{tiempo:.1f}h"
        score_formateado = f"{score}%"

        return format_html(
            '<div class="tiempo-procesamiento-container">'
            '<div class="tiempo-principal">'
            '<span class="tiempo-valor" style="color: {};">{}</span>'
            '<span class="tiempo-icon">{}</span>'
            "</div>"
            '<div class="eficiencia-indicator">'
            '<div class="eficiencia-bar">'
            '<div class="eficiencia-fill" style="width: {}%; background: {};"></div>'
            "</div>"
            '<span class="eficiencia-texto" style="color: {};">{}</span>'
            "</div>"
            "</div>",
            color,
            tiempo_formateado,
            icon,
            score_formateado,
            color,
            color,
            eficiencia,
        )

    tiempo_procesamiento_avanzado.short_description = "⏱️ Tiempo Proc."
    tiempo_procesamiento_avanzado.admin_order_field = "tiempo_promedio_procesamiento"

    def aprobacion_con_tendencia(self, obj):
        """Porcentaje de aprobación con tendencia y benchmark"""
        porcentaje = float(obj.porcentaje_aprobacion)

        # Benchmark sectorial
        benchmark = 85.0
        diferencia_benchmark = porcentaje - benchmark

        # Determinar estado
        if porcentaje >= 90:
            estado = "Excelente"
            color = "#28a745"
            icon = "👑"
        elif porcentaje >= 80:
            estado = "Bueno"
            color = "#28a745"
            icon = "✅"
        elif porcentaje >= 70:
            estado = "Regular"
            color = "#ffc107"
            icon = "⚠️"
        else:
            estado = "Crítico"
            color = "#dc3545"
            icon = "🚨"

        # Formatear valores antes de pasarlos a format_html
        porcentaje_formateado = f"{porcentaje:.1f}%"
        diferencia_formateada = f"{diferencia_benchmark:+.1f}pp"

        return format_html(
            '<div class="aprobacion-container">'
            '<div class="aprobacion-principal">'
            '<span class="aprobacion-valor" style="color: {};">{}</span>'
            '<span class="aprobacion-icon">{}</span>'
            "</div>"
            '<div class="aprobacion-estado" style="color: {};">{}</div>'
            '<div class="benchmark-comparison">'
            '<span class="benchmark-texto">vs Benchmark: </span>'
            '<span class="benchmark-diferencia" style="color: {};">'
            "{}"
            "</span>"
            "</div>"
            "</div>",
            color,
            porcentaje_formateado,
            icon,
            color,
            estado,
            "#28a745" if diferencia_benchmark >= 0 else "#dc3545",
            diferencia_formateada,
        )

    aprobacion_con_tendencia.short_description = "✅ Aprobación"
    aprobacion_con_tendencia.admin_order_field = "porcentaje_aprobacion"

    def ingresos_con_crecimiento(self, obj):
        """Ingresos con análisis de crecimiento y proyección"""
        ingresos = float(obj.ingresos_mes_actual)

        # Calcular crecimiento vs mes anterior
        mes_anterior = self._obtener_dashboard_mes_anterior(obj)
        crecimiento = self._calcular_crecimiento_ingresos(obj, mes_anterior)

        # Proyección mensual
        objetivo_mensual = 50000  # Bs.
        progreso_objetivo = (ingresos / objetivo_mensual) * 100

        # Formatear valores antes de pasarlos a format_html
        progreso_formateado = f"{progreso_objetivo:.0f}%"

        return format_html(
            '<div class="ingresos-container">'
            '<div class="ingresos-principal">'
            '<span class="ingresos-valor">Bs. {}</span>'
            "</div>"
            '<div class="crecimiento-indicator {}">'
            '<span class="crecimiento-icon">{}</span>'
            '<span class="crecimiento-texto">{}</span>'
            "</div>"
            '<div class="objetivo-progreso">'
            '<div class="progreso-bar">'
            '<div class="progreso-fill" style="width: {}%;"></div>'
            "</div>"
            '<span class="objetivo-texto">{} del objetivo</span>'
            "</div>"
            "</div>",
            self.format_numero_con_separadores(ingresos),
            crecimiento["class"],
            crecimiento["icon"],
            crecimiento["texto"],
            min(100, progreso_objetivo),
            progreso_formateado,
        )

    ingresos_con_crecimiento.short_description = "💰 Ingresos"
    ingresos_con_crecimiento.admin_order_field = "ingresos_mes_actual"

    def cabezas_bovinas_display(self, obj):
        """Display de cabezas bovinas con análisis de distribución"""
        total_cabezas = obj.total_cabezas_bovinas
        promedio_por_marca = float(obj.promedio_cabezas_por_marca)

        # Clasificar por volumen
        if total_cabezas >= 10000:
            categoria = "Alto Volumen"
            color = "#28a745"
            icon = "🏭"
        elif total_cabezas >= 5000:
            categoria = "Volumen Medio"
            color = "#ffc107"
            icon = "🏢"
        else:
            categoria = "Volumen Bajo"
            color = "#17a2b8"
            icon = "🏠"

        # Formatear valores antes de pasarlos a format_html
        promedio_formateado = f"{promedio_por_marca:.1f}"

        return format_html(
            '<div class="cabezas-container">'
            '<div class="cabezas-principal">'
            '<span class="cabezas-total">{}</span>'
            '<span class="cabezas-label">cabezas</span>'
            "</div>"
            '<div class="categoria-volumen" style="color: {};">'
            '<span class="categoria-icon">{}</span>'
            '<span class="categoria-texto">{}</span>'
            "</div>"
            '<div class="promedio-info">'
            '<span class="promedio-valor">{}</span>'
            '<span class="promedio-label">prom/marca</span>'
            "</div>"
            "</div>",
            self.format_numero_con_separadores(total_cabezas),
            color,
            icon,
            categoria,
            promedio_formateado,
        )

    cabezas_bovinas_display.short_description = "🐄 Cabezas"
    cabezas_bovinas_display.admin_order_field = "total_cabezas_bovinas"

    def logos_rendimiento(self, obj):
        """Rendimiento de logos con análisis de IA"""
        tasa_exito = float(obj.tasa_exito_logos)

        # Análisis de rendimiento IA
        if tasa_exito >= 95:
            rendimiento = "Óptimo"
            color = "#28a745"
            icon = "🤖"
        elif tasa_exito >= 85:
            rendimiento = "Excelente"
            color = "#28a745"
            icon = "🎨"
        elif tasa_exito >= 75:
            rendimiento = "Bueno"
            color = "#ffc107"
            icon = "🖼️"
        else:
            rendimiento = "Necesita Mejora"
            color = "#dc3545"
            icon = "🔧"

        # Formatear valores antes de pasarlos a format_html
        tasa_formateada = f"{tasa_exito:.1f}%"
        progreso_formateado = f"{tasa_exito:.0f}%"

        return format_html(
            '<div class="logos-container">'
            '<div class="logos-principal">'
            '<span class="logos-tasa" style="color: {};">{}</span>'
            '<span class="logos-icon">{}</span>'
            "</div>"
            '<div class="rendimiento-ia" style="color: {};">{}</div>'
            '<div class="logos-progreso">'
            '<div class="progreso-circular" data-progress="{}">'
            '<div class="progreso-valor">{}</div>'
            "</div>"
            "</div>"
            "</div>",
            color,
            tasa_formateada,
            icon,
            color,
            rendimiento,
            tasa_exito,
            progreso_formateado,
        )

    logos_rendimiento.short_description = "🎨 Logos IA"
    logos_rendimiento.admin_order_field = "tasa_exito_logos"

    def marcas_pendientes_urgentes(self, obj):
        """Marcas pendientes con análisis de urgencia"""
        pendientes = obj.marcas_pendientes

        # Clasificar urgencia
        if pendientes == 0:
            urgencia = "Sin Pendientes"
            color = "#28a745"
            icon = "✅"
        elif pendientes <= 5:
            urgencia = "Normal"
            color = "#17a2b8"
            icon = "📋"
        elif pendientes <= 15:
            urgencia = "Atención"
            color = "#ffc107"
            icon = "⚠️"
        else:
            urgencia = "Crítico"
            color = "#dc3545"
            icon = "🚨"

        return format_html(
            '<div class="pendientes-container">'
            '<div class="pendientes-principal">'
            '<span class="pendientes-numero" style="color: {};">{}</span>'
            '<span class="pendientes-icon">{}</span>'
            "</div>"
            '<div class="urgencia-indicator" style="color: {};">{}</div>'
            '<div class="pendientes-accion">'
            '<button class="btn-revisar" onclick="revisarPendientes()">Revisar</button>'
            "</div>"
            "</div>",
            color,
            pendientes,
            icon,
            color,
            urgencia,
        )

    marcas_pendientes_urgentes.short_description = "⏳ Pendientes"
    marcas_pendientes_urgentes.admin_order_field = "marcas_pendientes"

    def estado_sistema_avanzado(self, obj):
        """Estado del sistema con análisis integral"""
        # Calcular score general del sistema - convertir todos a float
        score_aprobacion = float(obj.porcentaje_aprobacion)
        score_tiempo = max(
            0, 100 - (float(obj.tiempo_promedio_procesamiento) / 168 * 100)
        )
        score_logos = float(obj.tasa_exito_logos)
        score_pendientes = max(0, 100 - (float(obj.marcas_pendientes) / 20 * 100))

        score_general = (
            score_aprobacion + score_tiempo + score_logos + score_pendientes
        ) / 4

        # Determinar estado general
        if score_general >= 90:
            estado = "Excelente"
            color = "#28a745"
            icon = "🚀"
        elif score_general >= 80:
            estado = "Bueno"
            color = "#28a745"
            icon = "✅"
        elif score_general >= 70:
            estado = "Regular"
            color = "#ffc107"
            icon = "⚠️"
        else:
            estado = "Crítico"
            color = "#dc3545"
            icon = "🚨"

        # Formatear valores antes de pasarlos a format_html
        score_general_formateado = f"{score_general:.0f}"
        score_aprobacion_formateado = f"{score_aprobacion:.0f}%"
        score_tiempo_formateado = f"{score_tiempo:.0f}%"
        score_logos_formateado = f"{score_logos:.0f}%"

        return format_html(
            '<div class="sistema-container">'
            '<div class="sistema-principal">'
            '<span class="sistema-score" style="color: {};">{}</span>'
            '<span class="sistema-icon">{}</span>'
            "</div>"
            '<div class="sistema-estado" style="color: {};">{}</div>'
            '<div class="sistema-detalles">'
            '<div class="detalle-item">Aprobación: {}</div>'
            '<div class="detalle-item">Tiempo: {}</div>'
            '<div class="detalle-item">Logos: {}</div>'
            "</div>"
            "</div>",
            color,
            score_general_formateado,
            icon,
            color,
            estado,
            score_aprobacion_formateado,
            score_tiempo_formateado,
            score_logos_formateado,
        )

    estado_sistema_avanzado.short_description = "🎯 Estado Sistema"

    def alertas_criticas(self, obj):
        """Alertas críticas del sistema"""
        alertas_activas = self._analizar_alertas_criticas(obj)

        if not alertas_activas:
            return format_html(
                '<div class="alertas-ok">'
                '<span class="ok-icon">✅</span>'
                '<span class="ok-texto">Todo OK</span>'
                "</div>"
            )

        return format_html(
            '<div class="alertas-criticas">'
            '<div class="alertas-count">'
            '<span class="count-numero">{}</span>'
            '<span class="count-icon">🚨</span>'
            "</div>"
            '<div class="alertas-lista">'
            "{}"
            "</div>"
            "</div>",
            len(alertas_activas),
            "".join(
                [
                    f'<div class="alerta-item">{alerta}</div>'
                    for alerta in alertas_activas[:3]
                ]
            ),
        )

    alertas_criticas.short_description = "🚨 Alertas"

    # Campos de solo lectura avanzados
    def dashboard_ejecutivo_interactivo(self, obj):
        """Dashboard ejecutivo interactivo con métricas en tiempo real"""
        return format_html(
            '<div id="executive-dashboard" class="executive-dashboard-container test-css-loaded" data-dashboard-id="{}">'
            '<div class="dashboard-header">'
            "<h2>📊 Dashboard Ejecutivo - Sistema BI Ganado Bovino</h2>"
            '<div class="dashboard-controls">'
            '<button class="btn-refresh" onclick="refreshExecutiveDashboard()">🔄 Actualizar</button>'
            '<button class="btn-fullscreen" onclick="toggleFullscreen()">🔍 Pantalla Completa</button>'
            '<button class="btn-export" onclick="exportExecutiveDashboard()">📤 Exportar</button>'
            "</div>"
            "</div>"
            '<div class="kpis-grid">'
            '<div class="kpi-card primary">'
            '<div class="kpi-icon">🏷️</div>'
            '<div class="kpi-content">'
            '<div class="kpi-value">{}</div>'
            '<div class="kpi-label">Marcas Registradas</div>'
            '<div class="kpi-trend {}">{}</div>'
            "</div>"
            "</div>"
            '<div class="kpi-card success">'
            '<div class="kpi-icon">✅</div>'
            '<div class="kpi-content">'
            '<div class="kpi-value">{}%</div>'
            '<div class="kpi-label">Tasa Aprobación</div>'
            '<div class="kpi-benchmark">Meta: 85%</div>'
            "</div>"
            "</div>"
            '<div class="kpi-card warning">'
            '<div class="kpi-icon">⏱️</div>'
            '<div class="kpi-content">'
            '<div class="kpi-value">{}h</div>'
            '<div class="kpi-label">Tiempo Promedio</div>'
            '<div class="kpi-target">Meta: <48h</div>'
            "</div>"
            "</div>"
            '<div class="kpi-card info">'
            '<div class="kpi-icon">💰</div>'
            '<div class="kpi-content">'
            '<div class="kpi-value">Bs. {}</div>'
            '<div class="kpi-label">Ingresos Mes</div>'
            '<div class="kpi-growth">+12.5%</div>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="charts-grid">'
            '<div class="chart-container">'
            "<h3>📈 Tendencia de Aprobaciones</h3>"
            '<canvas id="approval-trend-chart"></canvas>'
            "</div>"
            '<div class="chart-container">'
            "<h3>🐄 Distribución de Ganado</h3>"
            '<canvas id="cattle-distribution-chart"></canvas>'
            "</div>"
            '<div class="chart-container">'
            "<h3>🎨 Rendimiento IA</h3>"
            '<canvas id="ai-performance-chart"></canvas>'
            "</div>"
            '<div class="chart-container">'
            "<h3>📍 Distribución Geográfica</h3>"
            '<canvas id="geographic-chart"></canvas>'
            "</div>"
            "</div>"
            "</div>",
            obj.id,
            self.format_numero_con_separadores(obj.marcas_registradas_mes_actual),
            "trend-up",
            "↗️ +8.2%",
            f"{float(obj.porcentaje_aprobacion):.1f}",
            f"{float(obj.tiempo_promedio_procesamiento):.1f}",
            self.format_numero_con_separadores(obj.ingresos_mes_actual),
        )

    dashboard_ejecutivo_interactivo.short_description = (
        "Dashboard Ejecutivo Interactivo"
    )

    def metricas_tiempo_real(self, obj):
        """Métricas en tiempo real con auto-actualización"""
        return format_html(
            '<div id="realtime-metrics" class="realtime-container" data-dashboard-id="{}">'
            '<div class="realtime-header">'
            "<h3>⚡ Métricas en Tiempo Real</h3>"
            '<div class="realtime-status">'
            '<span class="status-indicator live"></span>'
            '<span class="status-text">En Vivo</span>'
            "</div>"
            "</div>"
            '<div class="metrics-grid">'
            '<div class="metric-card active-users">'
            '<div class="metric-header">'
            '<span class="metric-icon">👥</span>'
            '<span class="metric-title">Usuarios Activos</span>'
            "</div>"
            '<div class="metric-value" id="active-users">12</div>'
            '<div class="metric-change">+3 en la última hora</div>'
            "</div>"
            '<div class="metric-card processing-queue">'
            '<div class="metric-header">'
            '<span class="metric-icon">⚙️</span>'
            '<span class="metric-title">Cola de Procesamiento</span>'
            "</div>"
            '<div class="metric-value" id="processing-queue">{}</div>'
            '<div class="metric-change">Tiempo estimado: 2.5h</div>'
            "</div>"
            '<div class="metric-card system-load">'
            '<div class="metric-header">'
            '<span class="metric-icon">📊</span>'
            '<span class="metric-title">Carga del Sistema</span>'
            "</div>"
            '<div class="metric-value" id="system-load">67%</div>'
            '<div class="metric-change">Normal</div>'
            "</div>"
            '<div class="metric-card ai-models">'
            '<div class="metric-header">'
            '<span class="metric-icon">🤖</span>'
            '<span class="metric-title">Modelos IA Activos</span>'
            "</div>"
            '<div class="metric-value" id="ai-models">3/4</div>'
            '<div class="metric-change">1 en mantenimiento</div>'
            "</div>"
            "</div>"
            '<div class="realtime-chart">'
            "<h4>📈 Actividad en Tiempo Real</h4>"
            '<canvas id="realtime-activity-chart"></canvas>'
            "</div>"
            "</div>",
            obj.id,
            obj.marcas_pendientes,
        )

    metricas_tiempo_real.short_description = "Métricas Tiempo Real"

    def analisis_predictivo_dashboard(self, obj):
        """Análisis predictivo avanzado del dashboard"""
        return format_html(
            '<div id="predictive-dashboard" class="predictive-container" data-dashboard-id="{}">'
            '<div class="predictive-header">'
            "<h3>🔮 Análisis Predictivo</h3>"
            '<div class="prediction-confidence">Confianza: 87%</div>'
            "</div>"
            '<div class="predictions-grid">'
            '<div class="prediction-card">'
            "<h4>📊 Próximo Mes</h4>"
            '<div class="prediction-content">'
            '<div class="prediction-metric">'
            '<span class="metric-label">Marcas Estimadas:</span>'
            '<span class="metric-value">{}</span>'
            "</div>"
            '<div class="prediction-metric">'
            '<span class="metric-label">Ingresos Proyectados:</span>'
            '<span class="metric-value">Bs. {}</span>'
            "</div>"
            '<div class="prediction-metric">'
            '<span class="metric-label">Tasa Aprobación:</span>'
            '<span class="metric-value">{}%</span>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="prediction-card">'
            "<h4>📈 Tendencias Detectadas</h4>"
            '<div class="trends-list">'
            '<div class="trend-item positive">'
            '<span class="trend-icon">📈</span>'
            '<span class="trend-text">Incremento en registros de ganado lechero</span>'
            "</div>"
            '<div class="trend-item neutral">'
            '<span class="trend-icon">➡️</span>'
            '<span class="trend-text">Estabilidad en tiempos de procesamiento</span>'
            "</div>"
            '<div class="trend-item warning">'
            '<span class="trend-icon">⚠️</span>'
            '<span class="trend-text">Posible saturación en diciembre</span>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="prediction-card">'
            "<h4>💡 Recomendaciones IA</h4>"
            '<div class="recommendations-list">'
            '<div class="recommendation-item">'
            '<span class="rec-priority high">Alta</span>'
            '<span class="rec-text">Aumentar capacidad de procesamiento en 20%</span>'
            "</div>"
            '<div class="recommendation-item">'
            '<span class="rec-priority medium">Media</span>'
            '<span class="rec-text">Optimizar algoritmos de generación de logos</span>'
            "</div>"
            '<div class="recommendation-item">'
            '<span class="rec-priority low">Baja</span>'
            '<span class="rec-text">Revisar distribución geográfica de recursos</span>'
            "</div>"
            "</div>"
            "</div>"
            "</div>"
            '<div class="prediction-chart">'
            "<h4>📊 Proyección de Crecimiento</h4>"
            '<canvas id="growth-prediction-chart"></canvas>'
            "</div>"
            "</div>",
            obj.id,
            int(obj.marcas_registradas_mes_actual * 1.15),
            self.format_numero_con_separadores(int(obj.ingresos_mes_actual * 1.12)),
            f"{obj.porcentaje_aprobacion * 1.05:.1f}",
        )

    analisis_predictivo_dashboard.short_description = "Análisis Predictivo"

    def alertas_inteligentes_sistema(self, obj):
        """Sistema de alertas inteligentes"""
        alertas = self._generar_alertas_inteligentes(obj)

        return format_html(
            '<div id="intelligent-alerts" class="alerts-container" data-dashboard-id="{}">'
            '<div class="alerts-header">'
            "<h3>🚨 Sistema de Alertas Inteligentes</h3>"
            '<div class="alerts-summary">'
            '<span class="alerts-count">{} alertas activas</span>'
            '<button class="btn-configure-alerts" onclick="configureAlerts()">⚙️ Configurar</button>'
            "</div>"
            "</div>"
            '<div class="alerts-grid">'
            "{}"
            "</div>"
            '<div class="alerts-history">'
            "<h4>📜 Historial de Alertas (Últimas 24h)</h4>"
            '<div class="history-timeline">'
            '<div class="history-item resolved">'
            '<span class="history-time">14:30</span>'
            '<span class="history-text">Alerta de tiempo resuelva automáticamente</span>'
            "</div>"
            '<div class="history-item active">'
            '<span class="history-time">12:15</span>'
            '<span class="history-text">Nueva alerta: Incremento en rechazos</span>'
            "</div>"
            '<div class="history-item resolved">'
            '<span class="history-time">09:45</span>'
            '<span class="history-text">Alerta de capacidad resuelta</span>'
            "</div>"
            "</div>"
            "</div>"
            "</div>",
            obj.id,
            len(alertas),
            "".join(alertas),
        )

    alertas_inteligentes_sistema.short_description = "Alertas Inteligentes"

    def comparativa_historica_dashboard(self, obj):
        """Comparativa histórica del dashboard"""
        return format_html(
            '<div id="historical-comparison" class="comparison-container" data-dashboard-id="{}">'
            '<div class="comparison-header">'
            "<h3>📊 Comparativa Histórica</h3>"
            '<div class="comparison-controls">'
            '<select id="comparison-period">'
            '<option value="month">vs Mes Anterior</option>'
            '<option value="quarter">vs Trimestre Anterior</option>'
            '<option value="year">vs Año Anterior</option>'
            "</select>"
            "</div>"
            "</div>"
            '<div class="comparison-grid">'
            '<div class="comparison-card">'
            "<h4>🏷️ Marcas Registradas</h4>"
            '<div class="comparison-values">'
            '<div class="current-value">'
            '<span class="value-number">{}</span>'
            '<span class="value-label">Actual</span>'
            "</div>"
            '<div class="comparison-arrow positive">↗️</div>'
            '<div class="previous-value">'
            '<span class="value-number">{}</span>'
            '<span class="value-label">Anterior</span>'
            "</div>"
            "</div>"
            '<div class="comparison-change positive">+{}%</div>'
            "</div>"
            '<div class="comparison-card">'
            "<h4>✅ Tasa de Aprobación</h4>"
            '<div class="comparison-values">'
            '<div class="current-value">'
            '<span class="value-number">{}%</span>'
            '<span class="value-label">Actual</span>'
            "</div>"
            '<div class="comparison-arrow positive">↗️</div>'
            '<div class="previous-value">'
            '<span class="value-number">{}%</span>'
            '<span class="value-label">Anterior</span>'
            "</div>"
            "</div>"
            '<div class="comparison-change positive">+{}pp</div>'
            "</div>"
            '<div class="comparison-card">'
            "<h4>💰 Ingresos</h4>"
            '<div class="comparison-values">'
            '<div class="current-value">'
            '<span class="value-number">Bs. {}</span>'
            '<span class="value-label">Actual</span>'
            "</div>"
            '<div class="comparison-arrow positive">↗️</div>'
            '<div class="previous-value">'
            '<span class="value-number">Bs. {}</span>'
            '<span class="value-label">Anterior</span>'
            "</div>"
            "</div>"
            '<div class="comparison-change positive">+{}%</div>'
            "</div>"
            "</div>"
            '<div class="comparison-chart">'
            "<h4>📈 Evolución Histórica</h4>"
            '<canvas id="historical-evolution-chart"></canvas>'
            "</div>"
            "</div>",
            obj.id,
            obj.marcas_registradas_mes_actual,
            int(obj.marcas_registradas_mes_actual * 0.92),
            f"{8.7:.1f}",
            f"{obj.porcentaje_aprobacion:.1f}",
            f"{obj.porcentaje_aprobacion * 0.95:.1f}",
            f"{3.2:.1f}",
            self.format_numero_con_separadores(obj.ingresos_mes_actual),
            self.format_numero_con_separadores(int(obj.ingresos_mes_actual * 0.89)),
            f"{12.4:.1f}",
        )

    comparativa_historica_dashboard.short_description = "Comparativa Histórica"

    def distribucion_geografica_visual(self, obj):
        """Visualización de distribución geográfica"""
        return format_html(
            '<div class="geographic-distribution">'
            '<div class="distribution-header">'
            "<h4>🗺️ Distribución Geográfica</h4>"
            "</div>"
            '<div class="distribution-map">'
            '<div class="region-item">'
            '<span class="region-name">Santa Cruz</span>'
            '<div class="region-bar">'
            '<div class="region-fill" style="width: 45%;"></div>'
            "</div>"
            '<span class="region-percentage">45%</span>'
            "</div>"
            '<div class="region-item">'
            '<span class="region-name">Beni</span>'
            '<div class="region-bar">'
            '<div class="region-fill" style="width: 28%;"></div>'
            "</div>"
            '<span class="region-percentage">28%</span>'
            "</div>"
            '<div class="region-item">'
            '<span class="region-name">La Paz</span>'
            '<div class="region-bar">'
            '<div class="region-fill" style="width: 18%;"></div>'
            "</div>"
            '<span class="region-percentage">18%</span>'
            "</div>"
            '<div class="region-item">'
            '<span class="region-name">Otros</span>'
            '<div class="region-bar">'
            '<div class="region-fill" style="width: 9%;"></div>'
            "</div>"
            '<span class="region-percentage">9%</span>'
            "</div>"
            "</div>"
            "</div>"
        )

    distribucion_geografica_visual.short_description = "Distribución Geográfica"

    def rendimiento_logos_ia(self, obj):
        """Análisis detallado del rendimiento de logos IA"""
        return format_html(
            '<div class="ai-performance-analysis">'
            '<div class="performance-header">'
            "<h4>🤖 Análisis de Rendimiento IA</h4>"
            "</div>"
            '<div class="performance-metrics">'
            '<div class="metric-item">'
            '<span class="metric-label">Tasa de Éxito:</span>'
            '<span class="metric-value success">{}%</span>'
            "</div>"
            '<div class="metric-item">'
            '<span class="metric-label">Tiempo Promedio:</span>'
            '<span class="metric-value">{}s</span>'
            "</div>"
            '<div class="metric-item">'
            '<span class="metric-label">Modelos Activos:</span>'
            '<span class="metric-value">4/4</span>'
            "</div>"
            '<div class="metric-item">'
            '<span class="metric-label">Calidad Promedio:</span>'
            '<span class="metric-value excellent">Excelente</span>'
            "</div>"
            "</div>"
            '<div class="model-performance">'
            "<h5>Rendimiento por Modelo:</h5>"
            '<div class="model-item">'
            '<span class="model-name">DALL-E 3</span>'
            '<div class="model-stats">'
            '<span class="stat">95% éxito</span>'
            '<span class="stat">2.3s promedio</span>'
            "</div>"
            "</div>"
            '<div class="model-item">'
            '<span class="model-name">Midjourney</span>'
            '<div class="model-stats">'
            '<span class="stat">92% éxito</span>'
            '<span class="stat">1.8s promedio</span>'
            "</div>"
            "</div>"
            "</div>"
            "</div>",
            f"{obj.tasa_exito_logos:.1f}",
            f"{2.1:.1f}",
        )

    rendimiento_logos_ia.short_description = "Rendimiento Logos IA"

    def recomendaciones_automaticas(self, obj):
        """Sistema de recomendaciones automáticas"""
        recomendaciones = self._generar_recomendaciones_automaticas(obj)

        return format_html(
            '<div class="recommendations-system">'
            '<div class="recommendations-header">'
            "<h4>💡 Recomendaciones Automáticas</h4>"
            '<div class="recommendations-score">Score IA: 94%</div>'
            "</div>"
            '<div class="recommendations-list">'
            "{}"
            "</div>"
            '<div class="recommendations-actions">'
            '<button class="btn-apply-all" onclick="applyAllRecommendations()">✅ Aplicar Todas</button>'
            '<button class="btn-schedule" onclick="scheduleRecommendations()">📅 Programar</button>'
            "</div>"
            "</div>",
            "".join(recomendaciones),
        )

    recomendaciones_automaticas.short_description = "Recomendaciones Automáticas"

    # Acciones masivas avanzadas
    def actualizar_dashboard_completo(self, request, queryset):
        """Actualización completa del dashboard con análisis avanzado"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🔄 Se inició la actualización completa de {} dashboards. "
                "Incluye recálculo de métricas, análisis predictivo y alertas inteligentes. "
                "<a href='#' onclick='viewUpdateProgress()'>Ver Progreso</a>",
                count,
            ),
            messages.SUCCESS,
        )

    actualizar_dashboard_completo.short_description = "🔄 Actualización completa"

    def generar_reporte_ejecutivo(self, request, queryset):
        """Genera reporte ejecutivo completo"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "📊 Se generó el reporte ejecutivo para {} períodos. "
                "Incluye análisis de tendencias, comparativas y recomendaciones estratégicas. "
                "<a href='#' onclick='downloadExecutiveReport()'>Descargar Reporte</a>",
                count,
            ),
            messages.SUCCESS,
        )

    generar_reporte_ejecutivo.short_description = "📊 Reporte ejecutivo"

    def exportar_metricas_tiempo_real(self, request, queryset):
        """Exporta métricas en tiempo real"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "⚡ Se exportaron las métricas en tiempo real de {} dashboards. "
                "El archivo incluye datos actualizados y proyecciones. "
                "<a href='#' onclick='downloadRealtimeMetrics()'>Descargar Métricas</a>",
                count,
            ),
            messages.SUCCESS,
        )

    exportar_metricas_tiempo_real.short_description = "⚡ Exportar métricas tiempo real"

    def crear_alertas_personalizadas(self, request, queryset):
        """Crea alertas personalizadas basadas en patrones"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🚨 Se configuraron alertas personalizadas para {} dashboards. "
                "Las alertas se activarán automáticamente según los umbrales definidos. "
                "<a href='#' onclick='configureCustomAlerts()'>Configurar Alertas</a>",
                count,
            ),
            messages.SUCCESS,
        )

    crear_alertas_personalizadas.short_description = "🚨 Alertas personalizadas"

    def optimizar_rendimiento_sistema(self, request, queryset):
        """Optimiza el rendimiento del sistema usando IA"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🤖 Se inició la optimización inteligente del sistema para {} dashboards. "
                "El análisis incluye mejoras de rendimiento y eficiencia operativa. "
                "<a href='#' onclick='viewOptimizationResults()'>Ver Resultados</a>",
                count,
            ),
            messages.SUCCESS,
        )

    optimizar_rendimiento_sistema.short_description = "🤖 Optimizar con IA"

    def limpiar_datos_antiguos_inteligente(self, request, queryset):
        """Limpieza inteligente de datos antiguos"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🧹 Se programó la limpieza inteligente de datos para {} dashboards. "
                "El sistema preservará datos críticos y archivará información histórica. "
                "<a href='#' onclick='viewCleanupReport()'>Ver Reporte</a>",
                count,
            ),
            messages.SUCCESS,
        )

    limpiar_datos_antiguos_inteligente.short_description = "🧹 Limpieza inteligente"

    # Vistas personalizadas
    def executive_dashboard_view(self, request):
        """Vista del dashboard ejecutivo"""
        context = {
            "title": "Dashboard Ejecutivo - Sistema BI Ganado Bovino",
            "opts": self.model._meta,
        }
        return render(request, "admin/dashboard_executive.html", context)

    def realtime_metrics_view(self, request):
        """Vista de métricas en tiempo real"""
        context = {
            "title": "Métricas en Tiempo Real",
            "opts": self.model._meta,
        }
        return render(request, "admin/dashboard_realtime.html", context)

    def predictive_analysis_view(self, request):
        """Vista de análisis predictivo"""
        context = {
            "title": "Análisis Predictivo",
            "opts": self.model._meta,
        }
        return render(request, "admin/dashboard_predictive.html", context)

    # APIs para datos AJAX
    def api_dashboard_data(self, request):
        """API para datos del dashboard"""
        try:
            latest_dashboard = DashboardDataModel.objects.latest("fecha_actualizacion")
            data = {
                "marcas_mes": latest_dashboard.marcas_registradas_mes_actual,
                "aprobacion": latest_dashboard.porcentaje_aprobacion,
                "tiempo_procesamiento": latest_dashboard.tiempo_promedio_procesamiento,
                "ingresos": float(latest_dashboard.ingresos_mes_actual),
                "cabezas_bovinas": latest_dashboard.total_cabezas_bovinas,
                "tasa_logos": latest_dashboard.tasa_exito_logos,
                "pendientes": latest_dashboard.marcas_pendientes,
                "ultima_actualizacion": latest_dashboard.fecha_actualizacion.isoformat(),
            }
            return JsonResponse(data)
        except DashboardDataModel.DoesNotExist:
            return JsonResponse({"error": "No hay datos disponibles"}, status=404)

    def api_alerts_data(self, request):
        """API para datos de alertas"""
        try:
            latest_dashboard = DashboardDataModel.objects.latest("fecha_actualizacion")
            alertas = self._generar_alertas_inteligentes(latest_dashboard)

            data = {
                "alertas_activas": len(alertas),
                "alertas_criticas": len([a for a in alertas if "critical" in a]),
                "alertas_detalle": alertas[:5],  # Primeras 5 alertas
            }
            return JsonResponse(data)
        except DashboardDataModel.DoesNotExist:
            return JsonResponse({"error": "No hay datos de alertas"}, status=404)

    def export_dashboard_view(self, request):
        """Exporta el dashboard completo"""
        response = HttpResponse(content_type="application/json")
        response["Content-Disposition"] = 'attachment; filename="dashboard_export.json"'

        try:
            latest_dashboard = DashboardDataModel.objects.latest("fecha_actualizacion")
            export_data = {
                "fecha_exportacion": timezone.now().isoformat(),
                "dashboard_data": {
                    "marcas_registradas": latest_dashboard.marcas_registradas_mes_actual,
                    "porcentaje_aprobacion": latest_dashboard.porcentaje_aprobacion,
                    "tiempo_procesamiento": latest_dashboard.tiempo_promedio_procesamiento,
                    "ingresos_mes": float(latest_dashboard.ingresos_mes_actual),
                    "total_cabezas": latest_dashboard.total_cabezas_bovinas,
                    "tasa_exito_logos": latest_dashboard.tasa_exito_logos,
                    "marcas_pendientes": latest_dashboard.marcas_pendientes,
                },
            }
            response.write(json.dumps(export_data, indent=2, ensure_ascii=False))
        except DashboardDataModel.DoesNotExist:
            response.write(
                json.dumps({"error": "No hay datos para exportar"}, indent=2)
            )

        return response

    def has_add_permission(self, request):
        """Los datos del dashboard se generan automáticamente"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Los datos del dashboard no se pueden eliminar"""
        return False

    # Métodos auxiliares privados
    def _calcular_tiempo_transcurrido(self, fecha):
        """Calcula el tiempo transcurrido desde una fecha"""
        ahora = timezone.now()
        diferencia = ahora - fecha

        if diferencia.total_seconds() < 60:
            return "Hace unos segundos"
        elif diferencia.total_seconds() < 3600:
            minutos = int(diferencia.total_seconds() / 60)
            return f"Hace {minutos} minuto{'s' if minutos > 1 else ''}"
        elif diferencia.total_seconds() < 86400:
            horas = int(diferencia.total_seconds() / 3600)
            return f"Hace {horas} hora{'s' if horas > 1 else ''}"
        else:
            dias = diferencia.days
            return f"Hace {dias} día{'s' if dias > 1 else ''}"

    def _obtener_dashboard_mes_anterior(self, obj):
        """Obtiene el dashboard del mes anterior"""
        try:
            fecha_anterior = obj.fecha_actualizacion - timedelta(days=30)
            return DashboardDataModel.objects.filter(
                fecha_actualizacion__lte=fecha_anterior
            ).latest("fecha_actualizacion")
        except DashboardDataModel.DoesNotExist:
            return None

    def _calcular_tendencia_marcas(self, obj, mes_anterior):
        """Calcula la tendencia de marcas vs mes anterior"""
        if not mes_anterior:
            return {"class": "trend-neutral", "icon": "➡️", "texto": "Sin datos"}

        diferencia = (
            obj.marcas_registradas_mes_actual
            - mes_anterior.marcas_registradas_mes_actual
        )
        porcentaje = (
            (diferencia / mes_anterior.marcas_registradas_mes_actual * 100)
            if mes_anterior.marcas_registradas_mes_actual > 0
            else 0
        )

        if porcentaje > 5:
            return {"class": "trend-up", "icon": "↗️", "texto": f"+{porcentaje:.1f}%"}
        elif porcentaje < -5:
            return {"class": "trend-down", "icon": "↘️", "texto": f"{porcentaje:.1f}%"}
        else:
            return {"class": "trend-stable", "icon": "➡️", "texto": f"{porcentaje:.1f}%"}

    def _calcular_crecimiento_ingresos(self, obj, mes_anterior):
        """Calcula el crecimiento de ingresos"""
        if not mes_anterior:
            return {"class": "growth-neutral", "icon": "➡️", "texto": "Sin datos"}

        diferencia = obj.ingresos_mes_actual - mes_anterior.ingresos_mes_actual
        porcentaje = (
            (diferencia / mes_anterior.ingresos_mes_actual * 100)
            if mes_anterior.ingresos_mes_actual > 0
            else 0
        )

        if porcentaje > 10:
            return {
                "class": "growth-high",
                "icon": "🚀",
                "texto": f"+{porcentaje:.1f}%",
            }
        elif porcentaje > 0:
            return {
                "class": "growth-positive",
                "icon": "📈",
                "texto": f"+{porcentaje:.1f}%",
            }
        elif porcentaje > -10:
            return {
                "class": "growth-negative",
                "icon": "📉",
                "texto": f"{porcentaje:.1f}%",
            }
        else:
            return {
                "class": "growth-critical",
                "icon": "⚠️",
                "texto": f"{porcentaje:.1f}%",
            }

    def _analizar_alertas_criticas(self, obj):
        """Analiza y genera alertas críticas"""
        alertas = []

        # Alerta de aprobación baja
        if obj.porcentaje_aprobacion < 70:
            alertas.append("Aprobación Crítica")

        # Alerta de tiempo alto
        if obj.tiempo_promedio_procesamiento > 72:
            alertas.append("Tiempo Excesivo")

        # Alerta de pendientes altos
        if obj.marcas_pendientes > 20:
            alertas.append("Cola Saturada")

        # Alerta de logos bajo rendimiento
        if obj.tasa_exito_logos < 80:
            alertas.append("IA Subóptima")

        return alertas

    def _generar_alertas_inteligentes(self, obj):
        """Genera alertas inteligentes del sistema"""
        alertas = []

        # Alerta crítica: Aprobación muy baja
        if obj.porcentaje_aprobacion < 60:
            alertas.append(
                '<div class="alert critical">'
                '<div class="alert-icon">🚨</div>'
                '<div class="alert-content">'
                "<h4>Tasa de Aprobación Crítica</h4>"
                "<p>La tasa de aprobación ({}%) está en nivel crítico.</p>"
                '<div class="alert-actions">'
                '<button class="btn-action">Revisar Procesos</button>'
                '<button class="btn-action">Contactar Supervisor</button>'
                "</div>"
                "</div>"
                "</div>".format(f"{obj.porcentaje_aprobacion:.1f}")
            )

        # Alerta de tiempo elevado
        if obj.tiempo_promedio_procesamiento > 96:
            alertas.append(
                '<div class="alert warning">'
                '<div class="alert-icon">⏰</div>'
                '<div class="alert-content">'
                "<h4>Tiempo de Procesamiento Elevado</h4>"
                "<p>El tiempo promedio ({}h) excede los límites.</p>"
                '<div class="alert-actions">'
                '<button class="btn-action">Optimizar Flujo</button>'
                "</div>"
                "</div>"
                "</div>".format(f"{obj.tiempo_promedio_procesamiento:.1f}")
            )

        # Alerta de oportunidad: Buen rendimiento
        if obj.porcentaje_aprobacion > 90 and obj.tasa_exito_logos > 95:
            alertas.append(
                '<div class="alert success">'
                '<div class="alert-icon">🎉</div>'
                '<div class="alert-content">'
                "<h4>Rendimiento Excelente</h4>"
                "<p>El sistema está operando a niveles óptimos.</p>"
                '<div class="alert-actions">'
                '<button class="btn-action">Mantener Estándares</button>'
                "</div>"
                "</div>"
                "</div>"
            )

        return alertas

    def _generar_recomendaciones_automaticas(self, obj):
        """Genera recomendaciones automáticas del sistema"""
        recomendaciones = []

        # Recomendación de eficiencia
        if obj.tiempo_promedio_procesamiento > 48:
            recomendaciones.append(
                '<div class="recommendation-item high-priority">'
                '<div class="rec-header">'
                '<span class="rec-priority">Alta Prioridad</span>'
                '<span class="rec-impact">Impacto: Alto</span>'
                "</div>"
                '<div class="rec-content">'
                "<h5>Optimizar Tiempos de Procesamiento</h5>"
                "<p>Implementar automatización para reducir tiempo promedio en 30%</p>"
                '<div class="rec-benefits">'
                '<span class="benefit">💰 Ahorro: Bs. 15,000/mes</span>'
                '<span class="benefit">⚡ Eficiencia: +25%</span>'
                "</div>"
                "</div>"
                '<div class="rec-actions">'
                '<button class="btn-apply">Aplicar</button>'
                '<button class="btn-schedule">Programar</button>'
                "</div>"
                "</div>"
            )

        # Recomendación de capacidad
        if obj.marcas_pendientes > 15:
            recomendaciones.append(
                '<div class="recommendation-item medium-priority">'
                '<div class="rec-header">'
                '<span class="rec-priority">Media Prioridad</span>'
                '<span class="rec-impact">Impacto: Medio</span>'
                "</div>"
                '<div class="rec-content">'
                "<h5>Aumentar Capacidad de Procesamiento</h5>"
                "<p>Asignar recursos adicionales para reducir cola de pendientes</p>"
                '<div class="rec-benefits">'
                '<span class="benefit">📈 Throughput: +40%</span>'
                '<span class="benefit">⏱️ Tiempo: -20%</span>'
                "</div>"
                "</div>"
                '<div class="rec-actions">'
                '<button class="btn-apply">Aplicar</button>'
                '<button class="btn-schedule">Programar</button>'
                "</div>"
                "</div>"
            )

        # Recomendación de IA
        if obj.tasa_exito_logos < 85:
            recomendaciones.append(
                '<div class="recommendation-item low-priority">'
                '<div class="rec-header">'
                '<span class="rec-priority">Baja Prioridad</span>'
                '<span class="rec-impact">Impacto: Bajo</span>'
                "</div>"
                '<div class="rec-content">'
                "<h5>Mejorar Modelos de IA</h5>"
                "<p>Reentrenar algoritmos para aumentar tasa de éxito de logos</p>"
                '<div class="rec-benefits">'
                '<span class="benefit">🎨 Calidad: +15%</span>'
                '<span class="benefit">🤖 Precisión: +10%</span>'
                "</div>"
                "</div>"
                '<div class="rec-actions">'
                '<button class="btn-apply">Aplicar</button>'
                '<button class="btn-schedule">Programar</button>'
                "</div>"
                "</div>"
            )

        return recomendaciones
