"""
Admin para KPIs de ganado bovino siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa para KPIGanadoBovinoModel
- Proporcionar visualización de métricas
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import KPIGanadoBovinoModel


@admin.register(KPIGanadoBovinoModel)
class KPIGanadoBovinoAdmin(BaseAnalyticsAdmin):
    """
    Admin para KPIs de ganado bovino - Clean Architecture.

    Responsabilidades:
    - Configurar visualización de KPIs
    - Proporcionar análisis de eficiencia
    - Gestionar métricas del sistema
    """

    list_display = [
        "fecha",
        "marcas_registradas_mes",
        "tiempo_promedio_procesamiento",
        "porcentaje_aprobacion",
        "ingresos_mes",
        "total_cabezas_registradas",
        "tasa_exito_logos",
        "eficiencia_display",
    ]

    list_filter = ["fecha"]

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
    ]

    fieldsets = (
        ("Información General", {"fields": ("fecha",)}),
        (
            "KPIs Principales",
            {
                "fields": (
                    "marcas_registradas_mes",
                    "tiempo_promedio_procesamiento",
                    "porcentaje_aprobacion",
                    "ingresos_mes",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Métricas de Ganado Bovino",
            {
                "fields": ("total_cabezas_registradas", "promedio_cabezas_por_marca"),
            },
        ),
        (
            "Distribución por Propósito",
            {
                "fields": (
                    "marcas_carne",
                    "marcas_leche",
                    "marcas_doble_proposito",
                    "marcas_reproduccion",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Distribución Geográfica",
            {
                "fields": (
                    "marcas_santa_cruz",
                    "marcas_beni",
                    "marcas_la_paz",
                    "marcas_otros_departamentos",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "KPIs de Logos",
            {
                "fields": (
                    "tasa_exito_logos",
                    "total_logos_generados",
                    "tiempo_promedio_generacion_logos",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Análisis", {"fields": ("eficiencia_display",), "classes": ("wide",)}),
    )

    def eficiencia_display(self, obj):
        """Muestra un resumen de eficiencia del sistema"""
        return self._generar_html_eficiencia(obj)

    eficiencia_display.short_description = "Resumen de Eficiencia"

    def has_add_permission(self, request):
        """Los KPIs se generan automáticamente"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Los KPIs no se pueden eliminar"""
        return False

    # Métodos privados (Encapsulation)
    def _generar_html_eficiencia(self, obj):
        """Genera el HTML para mostrar eficiencia"""
        html = "<div style='padding: 10px; background-color: #f5f5f5; border-radius: 5px;'>"

        # Eficiencia de aprobación
        html += self._generar_indicador_aprobacion(obj.porcentaje_aprobacion)

        # Eficiencia de tiempo
        html += self._generar_indicador_tiempo(obj.tiempo_promedio_procesamiento)

        # Eficiencia de logos
        html += self._generar_indicador_logos(obj.tasa_exito_logos)

        html += "</div>"
        return format_html(html)

    def _generar_indicador_aprobacion(self, porcentaje):
        """Genera indicador de aprobación"""
        if porcentaje >= 80:
            color = "#4caf50"
            icon = "✅"
        elif porcentaje >= 60:
            color = "#ff9800"
            icon = "⚠️"
        else:
            color = "#f44336"
            icon = "❌"

        return (
            f"<p><strong>{icon} Aprobación:</strong> "
            f"<span style='color: {color};'>{porcentaje:.1f}%</span></p>"
        )

    def _generar_indicador_tiempo(self, tiempo):
        """Genera indicador de tiempo"""
        if tiempo <= 24:
            color = "#4caf50"
            icon = "⚡"
        elif tiempo <= 72:
            color = "#ff9800"
            icon = "⏰"
        else:
            color = "#f44336"
            icon = "🐌"

        return (
            f"<p><strong>{icon} Tiempo Promedio:</strong> "
            f"<span style='color: {color};'>{tiempo:.1f}h</span></p>"
        )

    def _generar_indicador_logos(self, tasa):
        """Genera indicador de logos"""
        if tasa >= 85:
            color = "#4caf50"
            icon = "🎨"
        elif tasa >= 70:
            color = "#ff9800"
            icon = "🖼️"
        else:
            color = "#f44336"
            icon = "🚫"

        return (
            f"<p><strong>{icon} Logos:</strong> "
            f"<span style='color: {color};'>{tasa:.1f}%</span></p>"
        )
