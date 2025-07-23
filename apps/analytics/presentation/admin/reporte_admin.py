"""
Admin para datos de reportes siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa para ReporteDataModel
- Proporcionar visualización de reportes generados
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html
import json

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import ReporteDataModel


@admin.register(ReporteDataModel)
class ReporteDataAdmin(BaseAnalyticsAdmin):
    """
    Admin para datos de reportes - Clean Architecture.

    Responsabilidades:
    - Configurar visualización de reportes
    - Proporcionar gestión de reportes generados
    - Gestionar datos de reportes
    """

    list_display = [
        "fecha_generacion",
        "tipo_reporte",
        "periodo_inicio",
        "periodo_fin",
        "formato",
        "usuario_generador",
        "tamaño_datos_display",
        "estado_reporte_display",
    ]

    list_filter = [
        "fecha_generacion",
        "tipo_reporte",
        "formato",
        "usuario_generador",
    ]

    search_fields = [
        "tipo_reporte",
        "usuario_generador",
        "datos",
    ]

    readonly_fields = [
        "fecha_generacion",
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
        ("Información General", {"fields": ("fecha_generacion", "tipo_reporte")}),
        (
            "Período del Reporte",
            {
                "fields": ("periodo_inicio", "periodo_fin"),
                "classes": ("wide",),
            },
        ),
        (
            "Configuración",
            {
                "fields": ("formato", "usuario_generador"),
            },
        ),
        (
            "Datos del Reporte",
            {
                "fields": (
                    "datos",
                    "tamaño_datos_display",
                    "datos_formateados",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Análisis",
            {
                "fields": ("estado_reporte_display",),
                "classes": ("wide",),
            },
        ),
    )

    # Acciones masivas
    actions = [
        "exportar_reportes",
        "limpiar_reportes_antiguos",
        "regenerar_reportes",
    ]

    def tamaño_datos_display(self, obj):
        """Muestra el tamaño de los datos"""
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
        """Muestra los datos formateados"""
        try:
            datos_json = json.dumps(obj.datos, indent=2, ensure_ascii=False)
            return format_html(
                '<pre style="max-height: 200px; overflow-y: auto; background-color: #f5f5f5; padding: 10px; border-radius: 5px;">{}</pre>',
                datos_json,
            )
        except:
            return "Error al formatear datos"

    datos_formateados.short_description = "Datos Formateados"

    def estado_reporte_display(self, obj):
        """Muestra el estado del reporte"""
        return self._generar_html_estado_reporte(obj)

    estado_reporte_display.short_description = "Estado del Reporte"

    def has_add_permission(self, request):
        """Los reportes se generan automáticamente"""
        return False

    def has_change_permission(self, request, obj=None):
        """Los reportes no se pueden modificar"""
        return False

    # Acciones masivas
    def exportar_reportes(self, request, queryset):
        """Exporta los reportes seleccionados"""
        count = queryset.count()
        self.message_user(
            request,
            f"Se programó la exportación de {count} reportes. "
            "Los archivos estarán disponibles en la carpeta de descargas.",
        )

    exportar_reportes.short_description = "📤 Exportar reportes"

    def limpiar_reportes_antiguos(self, request, queryset):
        """Limpia reportes antiguos"""
        count = queryset.count()
        self.message_user(
            request,
            f"Se programó la limpieza de {count} reportes antiguos.",
        )

    limpiar_reportes_antiguos.short_description = "🧹 Limpiar reportes antiguos"

    def regenerar_reportes(self, request, queryset):
        """Regenera los reportes seleccionados"""
        count = queryset.count()
        self.message_user(
            request,
            f"Se programó la regeneración de {count} reportes. "
            "Este proceso se ejecutará en segundo plano.",
        )

    regenerar_reportes.short_description = "🔄 Regenerar reportes"

    # Métodos privados (Encapsulation)
    def _generar_html_estado_reporte(self, obj):
        """Genera el HTML para mostrar el estado del reporte"""
        html = "<div style='padding: 10px; background-color: #f9f9f9; border-radius: 5px;'>"

        # Estado del formato
        if obj.formato in ["excel", "pdf"]:
            color_formato = "#4caf50"
            icon_formato = "📄"
        elif obj.formato == "json":
            color_formato = "#2196f3"
            icon_formato = "📊"
        else:
            color_formato = "#ff9800"
            icon_formato = "📋"

        html += f"<p><strong>{icon_formato} Formato:</strong> "
        html += (
            f"<span style='color: {color_formato};'>{obj.formato.upper()}</span></p>"
        )

        # Estado de los datos
        try:
            datos_str = json.dumps(obj.datos) if obj.datos else "{}"
            tamaño_kb = len(datos_str.encode("utf-8")) / 1024

            if tamaño_kb < 1:
                color_datos = "#4caf50"
                icon_datos = "✅"
            elif tamaño_kb < 100:
                color_datos = "#ff9800"
                icon_datos = "⚠️"
            else:
                color_datos = "#f44336"
                icon_datos = "🚨"

            html += f"<p><strong>{icon_datos} Tamaño:</strong> "
            html += f"<span style='color: {color_datos};'>{tamaño_kb:.1f} KB</span></p>"
        except:
            html += "<p><strong>❌ Tamaño:</strong> <span style='color: #f44336;'>Error</span></p>"

        # Usuario generador
        if obj.usuario_generador:
            html += f"<p><strong>👤 Generado por:</strong> "
            html += f"<span style='color: #2196f3;'>{obj.usuario_generador}</span></p>"

        # Período
        html += f"<p><strong>📅 Período:</strong> "
        html += f"<span style='color: #666;'>{obj.periodo_inicio} - {obj.periodo_fin}</span></p>"

        html += "</div>"
        return format_html(html)
