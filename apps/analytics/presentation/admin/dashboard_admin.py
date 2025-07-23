"""
Admin para datos del dashboard siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa para DashboardDataModel
- Proporcionar visualización de métricas del dashboard
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import DashboardDataModel


@admin.register(DashboardDataModel)
class DashboardDataAdmin(BaseAnalyticsAdmin):
    """
    Admin para datos del dashboard - Clean Architecture.

    Responsabilidades:
    - Configurar visualización de datos del dashboard
    - Proporcionar análisis de métricas
    - Gestionar KPIs del sistema
    """

    list_display = [
        "fecha_actualizacion",
        "marcas_registradas_mes_actual",
        "tiempo_promedio_procesamiento",
        "porcentaje_aprobacion",
        "ingresos_mes_actual",
        "total_cabezas_bovinas",
        "tasa_exito_logos",
        "marcas_pendientes",
        "estado_sistema_display",
    ]

    list_filter = [
        "fecha_actualizacion",
        "raza_mas_comun",
    ]

    readonly_fields = [
        "fecha_actualizacion",
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
        "estado_sistema_display",
    ]

    date_hierarchy = "fecha_actualizacion"

    fieldsets = (
        ("Información General", {"fields": ("fecha_actualizacion",)}),
        (
            "KPIs Principales",
            {
                "fields": (
                    "marcas_registradas_mes_actual",
                    "tiempo_promedio_procesamiento",
                    "porcentaje_aprobacion",
                    "porcentaje_rechazo",
                    "ingresos_mes_actual",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Métricas de Ganado Bovino",
            {
                "fields": (
                    "total_cabezas_bovinas",
                    "promedio_cabezas_por_marca",
                ),
            },
        ),
        (
            "Distribución por Propósito",
            {
                "fields": (
                    "porcentaje_carne",
                    "porcentaje_leche",
                    "porcentaje_doble_proposito",
                    "porcentaje_reproduccion",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Distribución por Raza",
            {
                "fields": (
                    "raza_mas_comun",
                    "porcentaje_raza_principal",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "KPIs de Logos",
            {
                "fields": (
                    "tasa_exito_logos",
                    "total_marcas_sistema",
                    "marcas_pendientes",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Alertas del Sistema",
            {
                "fields": ("alertas",),
                "classes": ("collapse",),
            },
        ),
        (
            "Análisis del Sistema",
            {
                "fields": ("estado_sistema_display",),
                "classes": ("wide",),
            },
        ),
    )

    # Acciones masivas
    actions = [
        "actualizar_dashboard",
        "limpiar_datos_antiguos",
    ]

    def estado_sistema_display(self, obj):
        """Muestra el estado general del sistema"""
        return self._generar_html_estado_sistema(obj)

    estado_sistema_display.short_description = "Estado del Sistema"

    def has_add_permission(self, request):
        """Los datos del dashboard se generan automáticamente"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Los datos del dashboard no se pueden eliminar"""
        return False

    # Acciones masivas
    def actualizar_dashboard(self, request, queryset):
        """Actualiza los datos del dashboard"""
        count = queryset.count()
        self.message_user(
            request,
            f"Se programó la actualización de {count} registros del dashboard. "
            "Este proceso se ejecutará en segundo plano.",
        )

    actualizar_dashboard.short_description = "🔄 Actualizar dashboard"

    def limpiar_datos_antiguos(self, request, queryset):
        """Limpia datos antiguos del dashboard"""
        count = queryset.count()
        self.message_user(
            request,
            f"Se programó la limpieza de {count} registros antiguos del dashboard.",
        )

    limpiar_datos_antiguos.short_description = "🧹 Limpiar datos antiguos"

    # Métodos privados (Encapsulation)
    def _generar_html_estado_sistema(self, obj):
        """Genera el HTML para mostrar el estado del sistema"""
        html = "<div style='padding: 10px; background-color: #f0f8ff; border-radius: 5px;'>"

        # Estado de marcas
        if obj.marcas_pendientes > 10:
            color_marcas = "#f44336"
            icon_marcas = "⚠️"
        elif obj.marcas_pendientes > 5:
            color_marcas = "#ff9800"
            icon_marcas = "⚡"
        else:
            color_marcas = "#4caf50"
            icon_marcas = "✅"

        html += f"<p><strong>{icon_marcas} Marcas Pendientes:</strong> "
        html += (
            f"<span style='color: {color_marcas};'>{obj.marcas_pendientes}</span></p>"
        )

        # Estado de aprobación
        if obj.porcentaje_aprobacion >= 80:
            color_aprobacion = "#4caf50"
            icon_aprobacion = "✅"
        elif obj.porcentaje_aprobacion >= 60:
            color_aprobacion = "#ff9800"
            icon_aprobacion = "⚠️"
        else:
            color_aprobacion = "#f44336"
            icon_aprobacion = "❌"

        html += f"<p><strong>{icon_aprobacion} Tasa de Aprobación:</strong> "
        html += f"<span style='color: {color_aprobacion};'>{obj.porcentaje_aprobacion:.1f}%</span></p>"

        # Estado de logos
        if obj.tasa_exito_logos >= 85:
            color_logos = "#4caf50"
            icon_logos = "🎨"
        elif obj.tasa_exito_logos >= 70:
            color_logos = "#ff9800"
            icon_logos = "🖼️"
        else:
            color_logos = "#f44336"
            icon_logos = "🚫"

        html += f"<p><strong>{icon_logos} Éxito de Logos:</strong> "
        html += f"<span style='color: {color_logos};'>{obj.tasa_exito_logos:.1f}%</span></p>"

        # Raza más común
        if obj.raza_mas_comun:
            html += f"<p><strong>🐄 Raza Principal:</strong> "
            html += f"<span style='color: #2196f3;'>{obj.raza_mas_comun} ({obj.porcentaje_raza_principal:.1f}%)</span></p>"

        html += "</div>"
        return format_html(html)
