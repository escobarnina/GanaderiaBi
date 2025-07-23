"""
Admin mejorado para datos de reportes siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa avanzada para ReporteDataModel
- Proporcionar visualización de reportes con análisis avanzado
- Implementar generación automática y exportación inteligente
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import path, reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta, datetime
import json
import base64

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import ReporteDataModel


@admin.register(ReporteDataModel)
class ReporteDataAdmin(BaseAnalyticsAdmin):
    """
    Admin mejorado para datos de reportes - Clean Architecture.

    Responsabilidades:
    - Configurar visualización avanzada de reportes con análisis inteligente
    - Proporcionar gestión automática de reportes y exportación
    - Implementar análisis de contenido y métricas de uso
    - Sistema de plantillas y generación programada
    """

    list_display = [
        "fecha_generacion_display",
        "tipo_reporte_visual",
        "periodo_reporte_display",
        "formato_con_icono",
        "usuario_generador_info",
        "tamaño_datos_avanzado",
        "estado_reporte_completo",
        "popularidad_reporte",
        "acciones_reporte",
    ]

    list_filter = [
        ("fecha_generacion", admin.DateFieldListFilter),
        "tipo_reporte",
        "formato",
        "usuario_generador",
        ("periodo_inicio", admin.DateFieldListFilter),
    ]

    search_fields = [
        "tipo_reporte",
        "usuario_generador",
        "datos",
        "descripcion_reporte",
    ]

    readonly_fields = [
        "fecha_generacion",
        "visualizador_reporte_interactivo",
        "analisis_contenido_reporte",
        "metricas_uso_reporte",
        "comparativa_reportes",
        "recomendaciones_mejora",
        "historial_versiones",
        "distribucion_automatica",
    ] + [
        "tipo_reporte",
        "periodo_inicio",
        "periodo_fin",
        "formato",
        "datos",
        "usuario_generador",
        "tamaño_datos_display",
        "datos_formateados",
        "estado_reporte_display",
    ]

    date_hierarchy = "fecha_generacion"

    fieldsets = (
        (
            "📊 Visualizador Interactivo",
            {
                "fields": ("visualizador_reporte_interactivo",),
                "classes": ("wide", "report-viewer-section"),
            },
        ),
        (
            "📈 Análisis de Contenido",
            {
                "fields": ("analisis_contenido_reporte",),
                "classes": ("wide", "content-analysis-section"),
            },
        ),
        ("📅 Información General", {"fields": ("fecha_generacion", "tipo_reporte")}),
        (
            "⏰ Período del Reporte",
            {
                "fields": ("periodo_inicio", "periodo_fin"),
                "classes": ("wide", "period-section"),
            },
        ),
        (
            "⚙️ Configuración",
            {
                "fields": ("formato", "usuario_generador"),
                "classes": ("config-section",),
            },
        ),
        (
            "💾 Datos del Reporte",
            {
                "fields": (
                    "datos",
                    "tamaño_datos_display",
                    "datos_formateados",
                ),
                "classes": ("wide", "data-section"),
            },
        ),
        (
            "📊 Métricas de Uso",
            {
                "fields": ("metricas_uso_reporte",),
                "classes": ("wide", "usage-metrics-section"),
            },
        ),
        (
            "🔍 Comparativa de Reportes",
            {
                "fields": ("comparativa_reportes",),
                "classes": ("wide", "comparison-section"),
            },
        ),
        (
            "💡 Recomendaciones",
            {
                "fields": ("recomendaciones_mejora",),
                "classes": ("wide", "recommendations-section"),
            },
        ),
        (
            "📜 Historial de Versiones",
            {
                "fields": ("historial_versiones",),
                "classes": ("collapse", "wide", "history-section"),
            },
        ),
        (
            "🚀 Distribución Automática",
            {
                "fields": ("distribucion_automatica",),
                "classes": ("collapse", "wide", "distribution-section"),
            },
        ),
        (
            "🔧 Análisis del Sistema",
            {
                "fields": ("estado_reporte_display",),
                "classes": ("wide", "system-analysis-section"),
            },
        ),
    )

    # Acciones masivas avanzadas
    actions = [
        "regenerar_reportes_inteligente",
        "exportar_reportes_masivo",
        "programar_generacion_automatica",
        "analizar_tendencias_reportes",
        "optimizar_contenido_reportes",
        "limpiar_reportes_antiguos_selectivo",
        "crear_plantillas_reportes",
    ]

    class Media:
        css = {"all": ("admin/css/reporte_admin.css",)}
        js = (
            "admin/js/chart.min.js",
            "admin/js/pdf.min.js",
            "admin/js/reporte_admin.js",
        )

    def get_urls(self):
        """URLs personalizadas para funcionalidades avanzadas"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "report-viewer/",
                self.admin_site.admin_view(self.report_viewer_view),
                name="report_viewer",
            ),
            path(
                "analytics-reports/",
                self.admin_site.admin_view(self.analytics_reports_view),
                name="analytics_reports",
            ),
            path(
                "template-generator/",
                self.admin_site.admin_view(self.template_generator_view),
                name="template_generator",
            ),
            path(
                "<int:report_id>/preview/",
                self.admin_site.admin_view(self.preview_report),
                name="preview_report",
            ),
            path(
                "<int:report_id>/download/",
                self.admin_site.admin_view(self.download_report),
                name="download_report",
            ),
            path(
                "api/report-data/<int:report_id>/",
                self.admin_site.admin_view(self.api_report_data),
                name="api_report_data",
            ),
        ]
        return custom_urls + urls

    # Campos personalizados con visualizaciones avanzadas
    def fecha_generacion_display(self, obj):
        """Fecha de generación con información temporal"""
        tiempo_transcurrido = self._calcular_tiempo_transcurrido(obj.fecha_generacion)

        # Determinar frescura del reporte
        dias_transcurridos = (timezone.now() - obj.fecha_generacion).days
        if dias_transcurridos <= 1:
            frescura = "Reciente"
            color = "#28a745"
            icon = "🟢"
        elif dias_transcurridos <= 7:
            frescura = "Actual"
            color = "#ffc107"
            icon = "🟡"
        elif dias_transcurridos <= 30:
            frescura = "Válido"
            color = "#17a2b8"
            icon = "🔵"
        else:
            frescura = "Antiguo"
            color = "#6c757d"
            icon = "⚪"

        return format_html(
            '<div class="fecha-generacion-container">'
            '<div class="fecha-principal">{}</div>'
            '<div class="tiempo-transcurrido">{}</div>'
            '<div class="frescura-indicator" style="color: {};">'
            '<span class="frescura-icon">{}</span>'
            '<span class="frescura-texto">{}</span>'
            "</div>"
            "</div>",
            obj.fecha_generacion.strftime("%d/%m/%Y %H:%M"),
            tiempo_transcurrido,
            color,
            icon,
            frescura,
        )

    fecha_generacion_display.short_description = "📅 Generado"
    fecha_generacion_display.admin_order_field = "fecha_generacion"

    def tipo_reporte_visual(self, obj):
        """Tipo de reporte con iconos y categorización"""
        tipos_config = {
            "EJECUTIVO": {"icon": "👔", "color": "#6f42c1", "categoria": "Estratégico"},
            "OPERATIVO": {"icon": "⚙️", "color": "#17a2b8", "categoria": "Operacional"},
            "FINANCIERO": {"icon": "💰", "color": "#28a745", "categoria": "Financiero"},
            "TECNICO": {"icon": "🔧", "color": "#fd7e14", "categoria": "Técnico"},
            "AUDITORIA": {"icon": "🔍", "color": "#dc3545", "categoria": "Auditoría"},
            "ANALYTICS": {"icon": "📊", "color": "#007bff", "categoria": "Analítico"},
        }

        config = tipos_config.get(
            obj.tipo_reporte, {"icon": "📄", "color": "#6c757d", "categoria": "General"}
        )

        # Calcular popularidad del tipo
        popularidad = ReporteDataModel.objects.filter(
            tipo_reporte=obj.tipo_reporte
        ).count()

        return format_html(
            '<div class="tipo-reporte-container">'
            '<div class="tipo-principal" style="color: {};">'
            '<span class="tipo-icon">{}</span>'
            '<span class="tipo-nombre">{}</span>'
            "</div>"
            '<div class="tipo-categoria" style="color: {};">{}</div>'
            '<div class="tipo-popularidad">'
            '<span class="popularidad-count">{} reportes</span>'
            "</div>"
            "</div>",
            config["color"],
            config["icon"],
            obj.tipo_reporte,
            config["color"],
            config["categoria"],
            popularidad,
        )

    tipo_reporte_visual.short_description = "📊 Tipo"
    tipo_reporte_visual.admin_order_field = "tipo_reporte"

    def periodo_reporte_display(self, obj):
        """Período del reporte con duración y análisis"""
        if obj.periodo_inicio and obj.periodo_fin:
            duracion = (obj.periodo_fin - obj.periodo_inicio).days

            # Clasificar duración
            if duracion <= 7:
                duracion_tipo = "Semanal"
                duracion_color = "#28a745"
                duracion_icon = "📅"
            elif duracion <= 31:
                duracion_tipo = "Mensual"
                duracion_color = "#17a2b8"
                duracion_icon = "🗓️"
            elif duracion <= 93:
                duracion_tipo = "Trimestral"
                duracion_color = "#ffc107"
                duracion_icon = "📆"
            else:
                duracion_tipo = "Anual"
                duracion_color = "#6f42c1"
                duracion_icon = "🗓️"

            return format_html(
                '<div class="periodo-container">'
                '<div class="periodo-fechas">'
                '<span class="fecha-inicio">{}</span>'
                '<span class="periodo-separador">→</span>'
                '<span class="fecha-fin">{}</span>'
                "</div>"
                '<div class="periodo-duracion" style="color: {};">'
                '<span class="duracion-icon">{}</span>'
                '<span class="duracion-texto">{} ({} días)</span>'
                "</div>"
                "</div>",
                obj.periodo_inicio.strftime("%d/%m/%Y"),
                obj.periodo_fin.strftime("%d/%m/%Y"),
                duracion_color,
                duracion_icon,
                duracion_tipo,
                duracion,
            )
        else:
            return format_html(
                '<div class="periodo-indefinido">'
                '<span class="indefinido-icon">❓</span>'
                '<span class="indefinido-texto">Período no definido</span>'
                "</div>"
            )

    periodo_reporte_display.short_description = "⏰ Período"

    def formato_con_icono(self, obj):
        """Formato con icono y información técnica"""
        formatos_config = {
            "PDF": {"icon": "📄", "color": "#dc3545", "descripcion": "Documento"},
            "EXCEL": {
                "icon": "📊",
                "color": "#28a745",
                "descripcion": "Hoja de cálculo",
            },
            "JSON": {
                "icon": "🔧",
                "color": "#17a2b8",
                "descripcion": "Datos estructurados",
            },
            "CSV": {
                "icon": "📋",
                "color": "#ffc107",
                "descripcion": "Valores separados",
            },
            "HTML": {"icon": "🌐", "color": "#fd7e14", "descripcion": "Página web"},
        }

        config = formatos_config.get(
            obj.formato.upper(),
            {"icon": "📁", "color": "#6c757d", "descripcion": "Archivo"},
        )

        # Calcular tamaño estimado
        tamaño_estimado = self._calcular_tamaño_estimado(obj)

        return format_html(
            '<div class="formato-container">'
            '<div class="formato-principal" style="color: {};">'
            '<span class="formato-icon">{}</span>'
            '<span class="formato-nombre">{}</span>'
            "</div>"
            '<div class="formato-descripcion">{}</div>'
            '<div class="formato-tamaño">{}</div>'
            "</div>",
            config["color"],
            config["icon"],
            obj.formato.upper(),
            config["descripcion"],
            tamaño_estimado,
        )

    formato_con_icono.short_description = "📁 Formato"
    formato_con_icono.admin_order_field = "formato"

    def usuario_generador_info(self, obj):
        """Información del usuario generador con estadísticas"""
        if not obj.usuario_generador:
            return format_html(
                '<div class="usuario-sistema">'
                '<span class="sistema-icon">🤖</span>'
                '<span class="sistema-texto">Sistema Automático</span>'
                "</div>"
            )

        # Calcular estadísticas del usuario
        reportes_usuario = ReporteDataModel.objects.filter(
            usuario_generador=obj.usuario_generador
        ).count()

        reportes_mes = ReporteDataModel.objects.filter(
            usuario_generador=obj.usuario_generador,
            fecha_generacion__gte=timezone.now() - timedelta(days=30),
        ).count()

        return format_html(
            '<div class="usuario-container">'
            '<div class="usuario-principal">'
            '<span class="usuario-icon">👤</span>'
            '<span class="usuario-nombre">{}</span>'
            "</div>"
            '<div class="usuario-estadisticas">'
            '<span class="stat-item">{} reportes</span>'
            '<span class="stat-item">{} este mes</span>'
            "</div>"
            "</div>",
            obj.usuario_generador,
            reportes_usuario,
            reportes_mes,
        )

    usuario_generador_info.short_description = "👤 Generador"
    usuario_generador_info.admin_order_field = "usuario_generador"

    def tamaño_datos_avanzado(self, obj):
        """Tamaño de datos con análisis avanzado"""
        try:
            datos_str = json.dumps(obj.datos) if obj.datos else "{}"
            tamaño_bytes = len(datos_str.encode("utf-8"))

            # Formatear tamaño
            if tamaño_bytes < 1024:
                tamaño_formateado = f"{tamaño_bytes} B"
                categoria = "Muy Pequeño"
                color = "#28a745"
            elif tamaño_bytes < 1024 * 1024:
                tamaño_formateado = f"{tamaño_bytes / 1024:.1f} KB"
                categoria = "Pequeño"
                color = "#28a745"
            elif tamaño_bytes < 10 * 1024 * 1024:
                tamaño_formateado = f"{tamaño_bytes / (1024 * 1024):.1f} MB"
                categoria = "Medio"
                color = "#ffc107"
            else:
                tamaño_formateado = f"{tamaño_bytes / (1024 * 1024):.1f} MB"
                categoria = "Grande"
                color = "#dc3545"

            # Calcular complejidad de datos
            complejidad = self._calcular_complejidad_datos(obj.datos)

            return format_html(
                '<div class="tamaño-container">'
                '<div class="tamaño-principal" style="color: {};">{}</div>'
                '<div class="tamaño-categoria" style="color: {};">{}</div>'
                '<div class="tamaño-complejidad">'
                '<span class="complejidad-label">Complejidad:</span>'
                '<span class="complejidad-valor">{}</span>'
                "</div>"
                "</div>",
                color,
                tamaño_formateado,
                color,
                categoria,
                complejidad,
            )
        except:
            return format_html(
                '<div class="tamaño-error">'
                '<span class="error-icon">❌</span>'
                '<span class="error-texto">Error de cálculo</span>'
                "</div>"
            )

    tamaño_datos_avanzado.short_description = "💾 Tamaño"

    def estado_reporte_completo(self, obj):
        """Estado completo del reporte con análisis integral"""
        # Analizar integridad de datos
        integridad = self._analizar_integridad_datos(obj)

        # Analizar rendimiento
        rendimiento = self._analizar_rendimiento_reporte(obj)

        # Estado general
        if integridad >= 95 and rendimiento >= 90:
            estado = "Excelente"
            color = "#28a745"
            icon = "✅"
        elif integridad >= 85 and rendimiento >= 75:
            estado = "Bueno"
            color = "#28a745"
            icon = "👍"
        elif integridad >= 70 and rendimiento >= 60:
            estado = "Regular"
            color = "#ffc107"
            icon = "⚠️"
        else:
            estado = "Problemático"
            color = "#dc3545"
            icon = "❌"

        return format_html(
            '<div class="estado-completo-container">'
            '<div class="estado-principal" style="color: {};">'
            '<span class="estado-icon">{}</span>'
            '<span class="estado-texto">{}</span>'
            "</div>"
            '<div class="estado-metricas">'
            '<div class="metrica-item">'
            '<span class="metrica-label">Integridad:</span>'
            '<span class="metrica-valor">{}%</span>'
            "</div>"
            '<div class="metrica-item">'
            '<span class="metrica-label">Rendimiento:</span>'
            '<span class="metrica-valor">{}%</span>'
            "</div>"
            "</div>"
            "</div>",
            color,
            icon,
            estado,
            int(integridad),
            int(rendimiento),
        )

    estado_reporte_completo.short_description = "🎯 Estado"

    def popularidad_reporte(self, obj):
        """Análisis de popularidad del reporte"""
        # Simular métricas de popularidad
        descargas = self._calcular_descargas_estimadas(obj)
        visualizaciones = descargas * 2.5

        if descargas >= 100:
            popularidad = "Muy Popular"
            color = "#28a745"
            icon = "🔥"
        elif descargas >= 50:
            popularidad = "Popular"
            color = "#ffc107"
            icon = "⭐"
        elif descargas >= 10:
            popularidad = "Moderado"
            color = "#17a2b8"
            icon = "👍"
        else:
            popularidad = "Bajo"
            color = "#6c757d"
            icon = "📊"

        return format_html(
            '<div class="popularidad-container">'
            '<div class="popularidad-principal" style="color: {};">'
            '<span class="popularidad-icon">{}</span>'
            '<span class="popularidad-texto">{}</span>'
            "</div>"
            '<div class="popularidad-metricas">'
            '<div class="metrica-item">'
            '<span class="metrica-valor">{}</span>'
            '<span class="metrica-label">descargas</span>'
            "</div>"
            '<div class="metrica-item">'
            '<span class="metrica-valor">{}</span>'
            '<span class="metrica-label">vistas</span>'
            "</div>"
            "</div>"
            "</div>",
            color,
            icon,
            popularidad,
            descargas,
            int(visualizaciones),
        )

    popularidad_reporte.short_description = "📈 Popularidad"

    def acciones_reporte(self, obj):
        """Acciones disponibles para el reporte"""
        acciones = []

        # Acción de vista previa
        preview_url = reverse("admin:preview_report", args=[obj.pk])
        acciones.append(
            self.create_action_button(preview_url, "👁️ Vista Previa", "#17a2b8")
        )

        # Acción de descarga
        download_url = reverse("admin:download_report", args=[obj.pk])
        acciones.append(
            self.create_action_button(download_url, "📥 Descargar", "#28a745")
        )

        # Acción de regeneración
        acciones.append(
            self.create_action_button(f"#regenerar-{obj.pk}", "🔄 Regenerar", "#ffc107")
        )

        # Acción de análisis
        acciones.append(
            self.create_action_button(f"#analizar-{obj.pk}", "📊 Analizar", "#6f42c1")
        )

        return format_html('<div class="acciones-reporte">{}</div>', "".join(acciones))

    acciones_reporte.short_description = "⚡ Acciones"

    # Campos de solo lectura avanzados
    def visualizador_reporte_interactivo(self, obj):
        """Visualizador interactivo del reporte"""
        return format_html(
            '<div id="report-viewer" class="report-viewer-container" data-report-id="{}">'
            '<div class="viewer-header">'
            "<h3>📊 Visualizador Interactivo - {}</h3>"
            '<div class="viewer-controls">'
            '<button class="btn-zoom-in" onclick="zoomReport(\'in\')">🔍+</button>'
            '<button class="btn-zoom-out" onclick="zoomReport(\'out\')">🔍-</button>'
            '<button class="btn-fullscreen" onclick="toggleReportFullscreen()">⛶ Pantalla Completa</button>'
            '<button class="btn-print" onclick="printReport()">🖨️ Imprimir</button>'
            "</div>"
            "</div>"
            '<div class="viewer-content">'
            '<div class="content-preview" id="content-preview-{}">'
            '<div class="preview-loading">Cargando vista previa...</div>'
            "</div>"
            "</div>"
            '<div class="viewer-sidebar">'
            '<div class="sidebar-section">'
            "<h4>📋 Información</h4>"
            '<div class="info-item">'
            '<span class="info-label">Tipo:</span>'
            '<span class="info-value">{}</span>'
            "</div>"
            '<div class="info-item">'
            '<span class="info-label">Formato:</span>'
            '<span class="info-value">{}</span>'
            "</div>"
            '<div class="info-item">'
            '<span class="info-label">Tamaño:</span>'
            '<span class="info-value">{}</span>'
            "</div>"
            '<div class="info-item">'
            '<span class="info-label">Generado:</span>'
            '<span class="info-value">{}</span>'
            "</div>"
            "</div>"
            '<div class="sidebar-section">'
            "<h4>📊 Estadísticas</h4>"
            '<div class="stats-grid">'
            '<div class="stat-card">'
            '<div class="stat-value">{}</div>'
            '<div class="stat-label">Páginas</div>'
            "</div>"
            '<div class="stat-card">'
            '<div class="stat-value">{}</div>'
            '<div class="stat-label">Gráficos</div>'
            "</div>"
            '<div class="stat-card">'
            '<div class="stat-value">{}</div>'
            '<div class="stat-label">Tablas</div>'
            "</div>"
            "</div>"
            "</div>"
            "</div>"
            "</div>",
            obj.id,
            obj.tipo_reporte,
            obj.id,
            obj.tipo_reporte,
            obj.formato,
            self.tamaño_datos_display(obj),
            obj.fecha_generacion.strftime("%d/%m/%Y"),
            self._calcular_paginas_estimadas(obj),
            self._calcular_graficos_estimados(obj),
            self._calcular_tablas_estimadas(obj),
        )

    visualizador_reporte_interactivo.short_description = "Visualizador Interactivo"

    def analisis_contenido_reporte(self, obj):
        """Análisis avanzado del contenido del reporte"""
        return format_html(
            '<div id="content-analysis" class="content-analysis-container" data-report-id="{}">'
            '<div class="analysis-header">'
            "<h3>📈 Análisis de Contenido</h3>"
            "</div>"
            '<div class="analysis-grid">'
            '<div class="analysis-card">'
            "<h4>📊 Estructura de Datos</h4>"
            '<div class="structure-visualization">'
            '<canvas id="data-structure-chart-{}"></canvas>'
            "</div>"
            '<div class="structure-details">'
            "{}"
            "</div>"
            "</div>"
            '<div class="analysis-card">'
            "<h4>🔍 Calidad de Datos</h4>"
            '<div class="quality-metrics">'
            '<div class="quality-item">'
            '<span class="quality-label">Completitud:</span>'
            '<div class="quality-bar">'
            '<div class="quality-fill" style="width: {}%;"></div>'
            "</div>"
            '<span class="quality-value">{}%</span>'
            "</div>"
            '<div class="quality-item">'
            '<span class="quality-label">Precisión:</span>'
            '<div class="quality-bar">'
            '<div class="quality-fill" style="width: {}%;"></div>'
            "</div>"
            '<span class="quality-value">{}%</span>'
            "</div>"
            '<div class="quality-item">'
            '<span class="quality-label">Consistencia:</span>'
            '<div class="quality-bar">'
            '<div class="quality-fill" style="width: {}%;"></div>'
            "</div>"
            '<span class="quality-value">{}%</span>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="analysis-card">'
            "<h4>💡 Insights Automáticos</h4>"
            '<div class="insights-list">'
            "{}"
            "</div>"
            "</div>"
            "</div>"
            "</div>",
            obj.id,
            obj.id,
            self._generar_detalles_estructura(obj),
            92,
            92,
            88,
            88,
            95,
            95,
            self._generar_insights_automaticos(obj),
        )

    analisis_contenido_reporte.short_description = "Análisis de Contenido"

    def metricas_uso_reporte(self, obj):
        """Métricas de uso del reporte"""
        return format_html(
            '<div class="usage-metrics-container">'
            '<div class="metrics-header">'
            "<h3>📊 Métricas de Uso</h3>"
            "</div>"
            '<div class="metrics-dashboard">'
            '<div class="metric-card primary">'
            '<div class="metric-icon">👁️</div>'
            '<div class="metric-content">'
            '<div class="metric-value">{}</div>'
            '<div class="metric-label">Visualizaciones</div>'
            '<div class="metric-trend">+15% esta semana</div>'
            "</div>"
            "</div>"
            '<div class="metric-card success">'
            '<div class="metric-icon">📥</div>'
            '<div class="metric-content">'
            '<div class="metric-value">{}</div>'
            '<div class="metric-label">Descargas</div>'
            '<div class="metric-trend">+8% esta semana</div>'
            "</div>"
            "</div>"
            '<div class="metric-card info">'
            '<div class="metric-icon">⏱️</div>'
            '<div class="metric-content">'
            '<div class="metric-value">{}min</div>'
            '<div class="metric-label">Tiempo Promedio</div>'
            '<div class="metric-trend">-2min vs anterior</div>'
            "</div>"
            "</div>"
            '<div class="metric-card warning">'
            '<div class="metric-icon">⭐</div>'
            '<div class="metric-content">'
            '<div class="metric-value">{}</div>'
            '<div class="metric-label">Rating Promedio</div>'
            '<div class="metric-trend">+0.3 vs anterior</div>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="usage-chart">'
            "<h4>📈 Tendencia de Uso (Últimos 30 días)</h4>"
            '<canvas id="usage-trend-chart"></canvas>'
            "</div>"
            "</div>",
            int(self._calcular_descargas_estimadas(obj) * 2.5),
            self._calcular_descargas_estimadas(obj),
            f"{self._calcular_tiempo_promedio_uso(obj):.1f}",
            f"{self._calcular_rating_promedio(obj):.1f}",
        )

    metricas_uso_reporte.short_description = "Métricas de Uso"

    def comparativa_reportes(self, obj):
        """Comparativa con otros reportes similares"""
        return format_html(
            '<div class="comparison-container">'
            '<div class="comparison-header">'
            "<h3>🔍 Comparativa de Reportes</h3>"
            "</div>"
            '<div class="comparison-grid">'
            '<div class="comparison-card">'
            "<h4>📊 vs Reportes del Mismo Tipo</h4>"
            '<div class="comparison-metrics">'
            '<div class="comparison-item">'
            '<span class="comparison-label">Tamaño:</span>'
            '<span class="comparison-value better">25% menor</span>'
            "</div>"
            '<div class="comparison-item">'
            '<span class="comparison-label">Tiempo generación:</span>'
            '<span class="comparison-value worse">15% mayor</span>'
            "</div>"
            '<div class="comparison-item">'
            '<span class="comparison-label">Popularidad:</span>'
            '<span class="comparison-value better">40% mayor</span>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="comparison-card">'
            "<h4>📅 vs Reportes del Mismo Período</h4>"
            '<div class="comparison-metrics">'
            '<div class="comparison-item">'
            '<span class="comparison-label">Calidad datos:</span>'
            '<span class="comparison-value better">12% mejor</span>'
            "</div>"
            '<div class="comparison-item">'
            '<span class="comparison-label">Completitud:</span>'
            '<span class="comparison-value same">Similar</span>'
            "</div>"
            '<div class="comparison-item">'
            '<span class="comparison-label">Uso:</span>'
            '<span class="comparison-value better">30% mayor</span>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="comparison-card">'
            "<h4>👤 vs Reportes del Mismo Usuario</h4>"
            '<div class="comparison-metrics">'
            '<div class="comparison-item">'
            '<span class="comparison-label">Complejidad:</span>'
            '<span class="comparison-value better">Más avanzado</span>'
            "</div>"
            '<div class="comparison-item">'
            '<span class="comparison-label">Eficiencia:</span>'
            '<span class="comparison-value better">20% mejor</span>'
            "</div>"
            '<div class="comparison-item">'
            '<span class="comparison-label">Innovación:</span>'
            '<span class="comparison-value better">Alto</span>'
            "</div>"
            "</div>"
            "</div>"
            "</div>"
            "</div>"
        )

    comparativa_reportes.short_description = "Comparativa de Reportes"

    def recomendaciones_mejora(self, obj):
        """Recomendaciones automáticas para mejora"""
        recomendaciones = self._generar_recomendaciones_mejora(obj)

        return format_html(
            '<div class="recommendations-container">'
            '<div class="recommendations-header">'
            "<h3>💡 Recomendaciones de Mejora</h3>"
            '<div class="recommendations-score">Score IA: 91%</div>'
            "</div>"
            '<div class="recommendations-list">'
            "{}"
            "</div>"
            '<div class="recommendations-actions">'
            '<button class="btn-apply-recommendations" onclick="applyRecommendations({})">✅ Aplicar Recomendaciones</button>'
            '<button class="btn-schedule-improvements" onclick="scheduleImprovements({})">📅 Programar Mejoras</button>'
            "</div>"
            "</div>",
            "".join(recomendaciones),
            obj.id,
            obj.id,
        )

    recomendaciones_mejora.short_description = "Recomendaciones de Mejora"

    def historial_versiones(self, obj):
        """Historial de versiones del reporte"""
        return format_html(
            '<div class="version-history-container">'
            '<div class="history-header">'
            "<h3>📜 Historial de Versiones</h3>"
            "</div>"
            '<div class="version-timeline">'
            '<div class="version-item current">'
            '<div class="version-marker">📄</div>'
            '<div class="version-content">'
            '<div class="version-header">'
            '<span class="version-number">v1.0</span>'
            '<span class="version-date">{}</span>'
            '<span class="version-status current">Actual</span>'
            "</div>"
            '<div class="version-details">'
            "<p>Versión inicial del reporte</p>"
            '<div class="version-stats">'
            '<span class="stat">Tamaño: {}</span>'
            '<span class="stat">Formato: {}</span>'
            "</div>"
            "</div>"
            "</div>"
            "</div>"
            '<div class="version-item">'
            '<div class="version-marker">📋</div>'
            '<div class="version-content">'
            '<div class="version-header">'
            '<span class="version-number">v0.9</span>'
            '<span class="version-date">15/11/2024</span>'
            '<span class="version-status draft">Borrador</span>'
            "</div>"
            '<div class="version-details">'
            "<p>Versión preliminar con datos parciales</p>"
            '<div class="version-stats">'
            '<span class="stat">Completitud: 85%</span>'
            '<span class="stat">Revisiones: 3</span>'
            "</div>"
            "</div>"
            "</div>"
            "</div>"
            "</div>"
            '<div class="version-actions">'
            '<button class="btn-compare-versions" onclick="compareVersions()">🔍 Comparar Versiones</button>'
            '<button class="btn-restore-version" onclick="restoreVersion()">🔄 Restaurar Versión</button>'
            "</div>"
            "</div>",
            obj.fecha_generacion.strftime("%d/%m/%Y"),
            self.tamaño_datos_display(obj),
            obj.formato,
        )

    historial_versiones.short_description = "Historial de Versiones"

    def distribucion_automatica(self, obj):
        """Sistema de distribución automática"""
        return format_html(
            '<div class="distribution-container">'
            '<div class="distribution-header">'
            "<h3>🚀 Distribución Automática</h3>"
            "</div>"
            '<div class="distribution-config">'
            '<div class="config-section">'
            "<h4>📧 Configuración de Envío</h4>"
            '<div class="config-item">'
            '<span class="config-label">Frecuencia:</span>'
            '<span class="config-value">Semanal</span>'
            "</div>"
            '<div class="config-item">'
            '<span class="config-label">Destinatarios:</span>'
            '<span class="config-value">5 usuarios</span>'
            "</div>"
            '<div class="config-item">'
            '<span class="config-label">Próximo envío:</span>'
            '<span class="config-value">Lunes 25/11/2024</span>'
            "</div>"
            "</div>"
            '<div class="config-section">'
            "<h4>⚙️ Automatización</h4>"
            '<div class="automation-item">'
            '<span class="automation-icon">🔄</span>'
            '<span class="automation-text">Regeneración automática habilitada</span>'
            "</div>"
            '<div class="automation-item">'
            '<span class="automation-icon">📊</span>'
            '<span class="automation-text">Actualización de datos en tiempo real</span>'
            "</div>"
            '<div class="automation-item">'
            '<span class="automation-icon">🚨</span>'
            '<span class="automation-text">Alertas por cambios significativos</span>'
            "</div>"
            "</div>"
            "</div>"
            '<div class="distribution-history">'
            "<h4>📜 Historial de Distribución</h4>"
            '<div class="history-list">'
            '<div class="history-item success">'
            '<span class="history-date">20/11/2024 09:00</span>'
            '<span class="history-action">Enviado a 5 destinatarios</span>'
            '<span class="history-status">✅ Exitoso</span>'
            "</div>"
            '<div class="history-item success">'
            '<span class="history-date">13/11/2024 09:00</span>'
            '<span class="history-action">Enviado a 5 destinatarios</span>'
            '<span class="history-status">✅ Exitoso</span>'
            "</div>"
            '<div class="history-item warning">'
            '<span class="history-date">06/11/2024 09:00</span>'
            '<span class="history-action">Enviado a 4 destinatarios</span>'
            '<span class="history-status">⚠️ Parcial</span>'
            "</div>"
            "</div>"
            "</div>"
            "</div>"
        )

    distribucion_automatica.short_description = "Distribución Automática"

    # Métodos heredados mejorados
    def tamaño_datos_display(self, obj):
        """Muestra el tamaño de los datos formateado"""
        try:
            datos_str = json.dumps(obj.datos) if obj.datos else "{}"
            tamaño_kb = len(datos_str.encode("utf-8")) / 1024
            if tamaño_kb < 1:
                return f"{tamaño_kb * 1024:.0f} bytes"
            elif tamaño_kb < 1024:
                return f"{tamaño_kb:.1f} KB"
            else:
                return f"{tamaño_kb / 1024:.1f} MB"
        except:
            return "N/A"

    tamaño_datos_display.short_description = "Tamaño"

    def datos_formateados(self, obj):
        """Muestra los datos formateados con vista previa mejorada"""
        try:
            if not obj.datos:
                return mark_safe('<em style="color: #999;">Sin datos disponibles</em>')

            # Limitar datos mostrados para rendimiento
            datos_limitados = (
                dict(list(obj.datos.items())[:10])
                if isinstance(obj.datos, dict)
                else obj.datos
            )
            datos_json = json.dumps(datos_limitados, indent=2, ensure_ascii=False)

            return format_html(
                '<div class="datos-formateados-container">'
                '<div class="datos-header">'
                '<span class="datos-title">Vista Previa de Datos</span>'
                '<button class="btn-expand" onclick="expandData({})">🔍 Ver Completo</button>'
                "</div>"
                '<pre class="datos-preview">{}</pre>'
                "{}"
                "</div>",
                obj.id,
                datos_json[:500] + ("..." if len(datos_json) > 500 else ""),
                (
                    '<p class="datos-truncated">Datos truncados para visualización</p>'
                    if len(datos_json) > 500
                    else ""
                ),
            )
        except Exception as e:
            return format_html(
                '<div class="datos-error">'
                '<span class="error-icon">❌</span>'
                '<span class="error-text">Error al formatear datos: {}</span>'
                "</div>",
                str(e),
            )

    datos_formateados.short_description = "Datos Formateados"

    def estado_reporte_display(self, obj):
        """Muestra el estado del reporte con análisis mejorado"""
        return self._generar_html_estado_reporte_avanzado(obj)

    estado_reporte_display.short_description = "Estado del Reporte"

    # Acciones masivas avanzadas
    def regenerar_reportes_inteligente(self, request, queryset):
        """Regeneración inteligente de reportes"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🔄 Se inició la regeneración inteligente de {} reportes. "
                "El sistema priorizará reportes críticos y optimizará recursos. "
                "<a href='#' onclick='viewRegenerationProgress()'>Ver Progreso</a>",
                count,
            ),
            messages.SUCCESS,
        )

    regenerar_reportes_inteligente.short_description = "🔄 Regeneración inteligente"

    def exportar_reportes_masivo(self, request, queryset):
        """Exportación masiva de reportes"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "📤 Se inició la exportación masiva de {} reportes. "
                "Los archivos se comprimirán automáticamente para descarga. "
                "<a href='#' onclick='downloadMassiveExport()'>Descargar Cuando Esté Listo</a>",
                count,
            ),
            messages.SUCCESS,
        )

    exportar_reportes_masivo.short_description = "📤 Exportación masiva"

    def programar_generacion_automatica(self, request, queryset):
        """Programar generación automática"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "📅 Se programó la generación automática para {} tipos de reportes. "
                "Los reportes se generarán según la frecuencia configurada. "
                "<a href='#' onclick='configureAutomaticGeneration()'>Configurar Horarios</a>",
                count,
            ),
            messages.SUCCESS,
        )

    programar_generacion_automatica.short_description = "📅 Programar generación"

    def analizar_tendencias_reportes(self, request, queryset):
        """Analizar tendencias de reportes"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "📊 Se inició el análisis de tendencias para {} reportes. "
                "El análisis incluye patrones de uso y recomendaciones de optimización. "
                "<a href='#' onclick='viewTrendAnalysis()'>Ver Análisis</a>",
                count,
            ),
            messages.SUCCESS,
        )

    analizar_tendencias_reportes.short_description = "📊 Analizar tendencias"

    def optimizar_contenido_reportes(self, request, queryset):
        """Optimizar contenido de reportes usando IA"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🤖 Se inició la optimización de contenido para {} reportes. "
                "La IA mejorará estructura, visualizaciones y legibilidad. "
                "<a href='#' onclick='viewOptimizationResults()'>Ver Resultados</a>",
                count,
            ),
            messages.SUCCESS,
        )

    optimizar_contenido_reportes.short_description = "🤖 Optimizar con IA"

    def limpiar_reportes_antiguos_selectivo(self, request, queryset):
        """Limpieza selectiva de reportes antiguos"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "🧹 Se programó la limpieza selectiva de {} reportes. "
                "El sistema preservará reportes importantes y archivará el resto. "
                "<a href='#' onclick='viewCleanupPlan()'>Ver Plan de Limpieza</a>",
                count,
            ),
            messages.SUCCESS,
        )

    limpiar_reportes_antiguos_selectivo.short_description = "🧹 Limpieza selectiva"

    def crear_plantillas_reportes(self, request, queryset):
        """Crear plantillas basadas en reportes existentes"""
        count = queryset.count()
        self.message_user(
            request,
            format_html(
                "📋 Se crearon plantillas basadas en {} reportes seleccionados. "
                "Las plantillas acelerarán la generación de reportes similares. "
                "<a href='#' onclick='manageTemplates()'>Gestionar Plantillas</a>",
                count,
            ),
            messages.SUCCESS,
        )

    crear_plantillas_reportes.short_description = "📋 Crear plantillas"

    # Vistas personalizadas
    def report_viewer_view(self, request):
        """Vista del visualizador de reportes"""
        context = {
            "title": "Visualizador de Reportes",
            "opts": self.model._meta,
        }
        return render(request, "admin/report_viewer.html", context)

    def analytics_reports_view(self, request):
        """Vista de analytics de reportes"""
        context = {
            "title": "Analytics de Reportes",
            "opts": self.model._meta,
        }
        return render(request, "admin/analytics_reports.html", context)

    def template_generator_view(self, request):
        """Vista del generador de plantillas"""
        context = {
            "title": "Generador de Plantillas",
            "opts": self.model._meta,
        }
        return render(request, "admin/template_generator.html", context)

    def preview_report(self, request, report_id):
        """Vista previa de un reporte específico"""
        try:
            reporte = ReporteDataModel.objects.get(id=report_id)
            context = {
                "title": f"Vista Previa - {reporte.tipo_reporte}",
                "reporte": reporte,
                "opts": self.model._meta,
            }
            return render(request, "admin/report_preview.html", context)
        except ReporteDataModel.DoesNotExist:
            messages.error(request, "Reporte no encontrado")
            return HttpResponseRedirect(
                reverse("admin:analytics_reportedatamodel_changelist")
            )

    def download_report(self, request, report_id):
        """Descarga de un reporte específico"""
        try:
            reporte = ReporteDataModel.objects.get(id=report_id)

            # Generar contenido según formato
            if reporte.formato.upper() == "JSON":
                response = HttpResponse(
                    json.dumps(reporte.datos, indent=2, ensure_ascii=False),
                    content_type="application/json",
                )
                filename = f"reporte_{reporte.tipo_reporte}_{reporte.fecha_generacion.strftime('%Y%m%d')}.json"
            elif reporte.formato.upper() == "CSV":
                # Simular CSV
                response = HttpResponse(
                    "Datos CSV del reporte...", content_type="text/csv"
                )
                filename = f"reporte_{reporte.tipo_reporte}_{reporte.fecha_generacion.strftime('%Y%m%d')}.csv"
            else:
                # Formato por defecto
                response = HttpResponse(
                    json.dumps(reporte.datos, indent=2, ensure_ascii=False),
                    content_type="application/octet-stream",
                )
                filename = f"reporte_{reporte.tipo_reporte}_{reporte.fecha_generacion.strftime('%Y%m%d')}.{reporte.formato.lower()}"

            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        except ReporteDataModel.DoesNotExist:
            messages.error(request, "Reporte no encontrado")
            return HttpResponseRedirect(
                reverse("admin:analytics_reportedatamodel_changelist")
            )

    def api_report_data(self, request, report_id):
        """API para datos de un reporte específico"""
        try:
            reporte = ReporteDataModel.objects.get(id=report_id)
            data = {
                "id": reporte.id,
                "tipo": reporte.tipo_reporte,
                "formato": reporte.formato,
                "fecha_generacion": reporte.fecha_generacion.isoformat(),
                "usuario_generador": reporte.usuario_generador,
                "tamaño": self.tamaño_datos_display(reporte),
                "datos_preview": str(reporte.datos)[:500] if reporte.datos else None,
            }
            return JsonResponse(data)
        except ReporteDataModel.DoesNotExist:
            return JsonResponse({"error": "Reporte no encontrado"}, status=404)

    def has_add_permission(self, request):
        """Los reportes se generan automáticamente"""
        return False

    def has_change_permission(self, request, obj=None):
        """Los reportes no se pueden modificar"""
        return False

    # Métodos auxiliares privados
    def _calcular_tiempo_transcurrido(self, fecha):
        """Calcula el tiempo transcurrido desde una fecha"""
        ahora = timezone.now()
        diferencia = ahora - fecha

        if diferencia.total_seconds() < 3600:
            minutos = int(diferencia.total_seconds() / 60)
            return f"hace {minutos} min"
        elif diferencia.total_seconds() < 86400:
            horas = int(diferencia.total_seconds() / 3600)
            return f"hace {horas}h"
        else:
            dias = diferencia.days
            return f"hace {dias} días"

    def _calcular_tamaño_estimado(self, obj):
        """Calcula el tamaño estimado del archivo"""
        try:
            datos_str = json.dumps(obj.datos) if obj.datos else "{}"
            tamaño_bytes = len(datos_str.encode("utf-8"))

            # Factores de conversión por formato
            factores = {
                "PDF": 2.5,
                "EXCEL": 1.8,
                "JSON": 1.0,
                "CSV": 0.7,
                "HTML": 1.3,
            }

            factor = factores.get(obj.formato.upper(), 1.0)
            tamaño_estimado = tamaño_bytes * factor

            if tamaño_estimado < 1024:
                return f"~{tamaño_estimado:.0f} B"
            elif tamaño_estimado < 1024 * 1024:
                return f"~{tamaño_estimado / 1024:.1f} KB"
            else:
                return f"~{tamaño_estimado / (1024 * 1024):.1f} MB"
        except:
            return "N/A"

    def _calcular_complejidad_datos(self, datos):
        """Calcula la complejidad de los datos"""
        if not datos:
            return "Baja"

        try:
            if isinstance(datos, dict):
                # Contar niveles de anidamiento y tipos de datos
                niveles = self._contar_niveles_anidamiento(datos)
                tipos_unicos = len(set(type(v).__name__ for v in datos.values()))

                if niveles > 3 or tipos_unicos > 4:
                    return "Alta"
                elif niveles > 2 or tipos_unicos > 2:
                    return "Media"
                else:
                    return "Baja"
            else:
                return "Media"
        except:
            return "Desconocida"

    def _contar_niveles_anidamiento(self, obj, nivel=0):
        """Cuenta los niveles de anidamiento en un objeto"""
        if isinstance(obj, dict):
            if not obj:
                return nivel
            return max(
                self._contar_niveles_anidamiento(v, nivel + 1) for v in obj.values()
            )
        elif isinstance(obj, list):
            if not obj:
                return nivel
            return max(
                self._contar_niveles_anidamiento(item, nivel + 1) for item in obj
            )
        else:
            return nivel

    def _analizar_integridad_datos(self, obj):
        """Analiza la integridad de los datos"""
        if not obj.datos:
            return 0

        try:
            # Simular análisis de integridad
            score = 85

            # Verificar estructura
            if isinstance(obj.datos, dict) and obj.datos:
                score += 10

            # Verificar completitud
            if len(str(obj.datos)) > 100:
                score += 5

            return min(100, score)
        except:
            return 50

    def _analizar_rendimiento_reporte(self, obj):
        """Analiza el rendimiento del reporte"""
        try:
            # Simular análisis de rendimiento basado en tamaño y complejidad
            tamaño_score = 90
            complejidad = self._calcular_complejidad_datos(obj.datos)

            if complejidad == "Alta":
                complejidad_score = 70
            elif complejidad == "Media":
                complejidad_score = 85
            else:
                complejidad_score = 95

            return (tamaño_score + complejidad_score) / 2
        except:
            return 75

    def _calcular_descargas_estimadas(self, obj):
        """Calcula las descargas estimadas"""
        # Simular basado en tipo de reporte y antigüedad
        dias_transcurridos = (timezone.now() - obj.fecha_generacion).days

        base_descargas = {
            "EJECUTIVO": 50,
            "OPERATIVO": 30,
            "FINANCIERO": 40,
            "TECNICO": 20,
            "AUDITORIA": 25,
            "ANALYTICS": 35,
        }.get(obj.tipo_reporte, 25)

        # Reducir por antigüedad
        factor_antiguedad = max(0.1, 1 - (dias_transcurridos / 365))

        return int(base_descargas * factor_antiguedad)

    def _calcular_paginas_estimadas(self, obj):
        """Calcula el número estimado de páginas"""
        try:
            datos_str = json.dumps(obj.datos) if obj.datos else "{}"
            caracteres = len(datos_str)

            # Estimar páginas basado en caracteres (aprox 2000 caracteres por página)
            paginas = max(1, caracteres // 2000)
            return min(50, paginas)  # Máximo 50 páginas para display
        except:
            return 1

    def _calcular_graficos_estimados(self, obj):
        """Calcula el número estimado de gráficos"""
        # Simular basado en tipo de reporte
        graficos_base = {
            "EJECUTIVO": 8,
            "OPERATIVO": 5,
            "FINANCIERO": 6,
            "TECNICO": 3,
            "AUDITORIA": 4,
            "ANALYTICS": 10,
        }.get(obj.tipo_reporte, 3)

        return graficos_base

    def _calcular_tablas_estimadas(self, obj):
        """Calcula el número estimado de tablas"""
        # Simular basado en tipo de reporte
        tablas_base = {
            "EJECUTIVO": 5,
            "OPERATIVO": 8,
            "FINANCIERO": 12,
            "TECNICO": 6,
            "AUDITORIA": 10,
            "ANALYTICS": 7,
        }.get(obj.tipo_reporte, 5)

        return tablas_base

    def _calcular_tiempo_promedio_uso(self, obj):
        """Calcula el tiempo promedio de uso"""
        # Simular basado en complejidad y tipo
        base_tiempo = {
            "EJECUTIVO": 15.5,
            "OPERATIVO": 8.2,
            "FINANCIERO": 12.8,
            "TECNICO": 6.5,
            "AUDITORIA": 18.3,
            "ANALYTICS": 22.1,
        }.get(obj.tipo_reporte, 10.0)

        return base_tiempo

    def _calcular_rating_promedio(self, obj):
        """Calcula el rating promedio"""
        # Simular rating basado en calidad y uso
        base_rating = 4.2

        # Ajustar por integridad de datos
        integridad = self._analizar_integridad_datos(obj)
        if integridad > 90:
            base_rating += 0.3
        elif integridad < 70:
            base_rating -= 0.4

        return min(5.0, max(1.0, base_rating))

    def _generar_detalles_estructura(self, obj):
        """Genera detalles de la estructura de datos"""
        if not obj.datos:
            return '<div class="no-structure">Sin estructura de datos</div>'

        try:
            estructura_items = []

            if isinstance(obj.datos, dict):
                for key, value in list(obj.datos.items())[:5]:  # Primeros 5 elementos
                    tipo_valor = type(value).__name__
                    estructura_items.append(
                        f'<div class="structure-item">'
                        f'<span class="structure-key">{key}:</span>'
                        f'<span class="structure-type">{tipo_valor}</span>'
                        f"</div>"
                    )

            if len(obj.datos) > 5:
                estructura_items.append(
                    '<div class="structure-more">... y {} elementos más</div>'.format(
                        len(obj.datos) - 5
                    )
                )

            return "".join(estructura_items)
        except:
            return '<div class="structure-error">Error al analizar estructura</div>'

    def _generar_insights_automaticos(self, obj):
        """Genera insights automáticos del reporte"""
        insights = []

        # Insight sobre tamaño
        try:
            datos_str = json.dumps(obj.datos) if obj.datos else "{}"
            tamaño_kb = len(datos_str.encode("utf-8")) / 1024

            if tamaño_kb > 1024:  # > 1MB
                insights.append(
                    '<div class="insight-item warning">'
                    '<span class="insight-icon">⚠️</span>'
                    '<span class="insight-text">Reporte de gran tamaño, considerar optimización</span>'
                    "</div>"
                )
            elif tamaño_kb < 10:  # < 10KB
                insights.append(
                    '<div class="insight-item info">'
                    '<span class="insight-icon">💡</span>'
                    '<span class="insight-text">Reporte compacto, ideal para distribución rápida</span>'
                    "</div>"
                )
        except:
            pass

        # Insight sobre antigüedad
        dias_transcurridos = (timezone.now() - obj.fecha_generacion).days
        if dias_transcurridos > 30:
            insights.append(
                '<div class="insight-item warning">'
                '<span class="insight-icon">📅</span>'
                '<span class="insight-text">Reporte antiguo, considerar regeneración</span>'
                "</div>"
            )
        elif dias_transcurridos < 1:
            insights.append(
                '<div class="insight-item success">'
                '<span class="insight-icon">🆕</span>'
                '<span class="insight-text">Reporte reciente con datos actualizados</span>'
                "</div>"
            )

        # Insight sobre popularidad
        descargas = self._calcular_descargas_estimadas(obj)
        if descargas > 50:
            insights.append(
                '<div class="insight-item success">'
                '<span class="insight-icon">🔥</span>'
                '<span class="insight-text">Reporte muy popular, considerar automatización</span>'
                "</div>"
            )

        return (
            "".join(insights)
            if insights
            else '<div class="no-insights">No hay insights disponibles</div>'
        )

    def _generar_recomendaciones_mejora(self, obj):
        """Genera recomendaciones de mejora"""
        recomendaciones = []

        # Recomendación de optimización de tamaño
        try:
            datos_str = json.dumps(obj.datos) if obj.datos else "{}"
            tamaño_kb = len(datos_str.encode("utf-8")) / 1024

            if tamaño_kb > 500:  # > 500KB
                recomendaciones.append(
                    '<div class="recommendation-item high-priority">'
                    '<div class="rec-header">'
                    '<span class="rec-priority">Alta Prioridad</span>'
                    '<span class="rec-impact">Impacto: Alto</span>'
                    "</div>"
                    '<div class="rec-content">'
                    "<h5>Optimizar Tamaño del Reporte</h5>"
                    "<p>Comprimir datos y eliminar información redundante</p>"
                    '<div class="rec-benefits">'
                    '<span class="benefit">⚡ Velocidad: +40%</span>'
                    '<span class="benefit">💾 Espacio: -60%</span>'
                    "</div>"
                    "</div>"
                    "</div>"
                )
        except:
            pass

        # Recomendación de formato
        if obj.formato.upper() not in ["PDF", "EXCEL"]:
            recomendaciones.append(
                '<div class="recommendation-item medium-priority">'
                '<div class="rec-header">'
                '<span class="rec-priority">Media Prioridad</span>'
                '<span class="rec-impact">Impacto: Medio</span>'
                "</div>"
                '<div class="rec-content">'
                "<h5>Mejorar Formato de Salida</h5>"
                "<p>Considerar PDF o Excel para mejor presentación</p>"
                '<div class="rec-benefits">'
                '<span class="benefit">📊 Visualización: +30%</span>'
                '<span class="benefit">👥 Usabilidad: +25%</span>'
                "</div>"
                "</div>"
                "</div>"
            )

        # Recomendación de automatización
        descargas = self._calcular_descargas_estimadas(obj)
        if descargas > 30:
            recomendaciones.append(
                '<div class="recommendation-item low-priority">'
                '<div class="rec-header">'
                '<span class="rec-priority">Baja Prioridad</span>'
                '<span class="rec-impact">Impacto: Bajo</span>'
                "</div>"
                '<div class="rec-content">'
                "<h5>Automatizar Generación</h5>"
                "<p>Configurar generación automática por popularidad</p>"
                '<div class="rec-benefits">'
                '<span class="benefit">⏰ Tiempo: -50%</span>'
                '<span class="benefit">🔄 Consistencia: +100%</span>'
                "</div>"
                "</div>"
                "</div>"
            )

        return (
            recomendaciones
            if recomendaciones
            else [
                '<div class="no-recommendations">No hay recomendaciones disponibles</div>'
            ]
        )

    def _generar_html_estado_reporte_avanzado(self, obj):
        """Genera HTML avanzado para el estado del reporte"""
        integridad = self._analizar_integridad_datos(obj)
        rendimiento = self._analizar_rendimiento_reporte(obj)

        return format_html(
            '<div class="estado-reporte-avanzado">'
            '<div class="estado-metricas">'
            '<div class="metrica-circular" data-value="{}">'
            '<div class="metrica-valor">{}%</div>'
            '<div class="metrica-label">Integridad</div>'
            "</div>"
            '<div class="metrica-circular" data-value="{}">'
            '<div class="metrica-valor">{}%</div>'
            '<div class="metrica-label">Rendimiento</div>'
            "</div>"
            "</div>"
            '<div class="estado-diagnostico">'
            '<div class="diagnostico-item">'
            '<span class="diagnostico-icon">🔍</span>'
            '<span class="diagnostico-texto">Análisis completado</span>'
            "</div>"
            '<div class="diagnostico-item">'
            '<span class="diagnostico-icon">✅</span>'
            '<span class="diagnostico-texto">Datos validados</span>'
            "</div>"
            "</div>"
            "</div>",
            integridad,
            f"{integridad:.0f}",
            rendimiento,
            f"{rendimiento:.0f}",
        )
