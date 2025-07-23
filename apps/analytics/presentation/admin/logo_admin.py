"""
Admin para logos de marcas bovinas siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa para LogoMarcaBovinaModel
- Proporcionar acciones para gestión de logos
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import LogoMarcaBovinaModel


@admin.register(LogoMarcaBovinaModel)
class LogoMarcaBovinaAdmin(BaseAnalyticsAdmin):
    """
    Admin para logos de marcas bovinas - Clean Architecture.

    Responsabilidades:
    - Configurar visualización de logos
    - Proporcionar acciones para logos
    - Gestionar calidad de logos
    """

    list_display = [
        "marca_numero",
        "marca_productor",
        "modelo_ia_usado",
        "exito",
        "calidad_logo",
        "tiempo_generacion_segundos",
        "fecha_generacion",
        "success_indicator",
    ]

    list_filter = ["modelo_ia_usado", "exito", "calidad_logo", "fecha_generacion"]

    search_fields = ["marca__numero_marca", "marca__nombre_productor", "prompt_usado"]

    readonly_fields = ["fecha_generacion", "tiempo_generacion_display"]

    date_hierarchy = "fecha_generacion"

    fieldsets = (
        ("Información de la Marca", {"fields": ("marca",)}),
        (
            "Generación del Logo",
            {
                "fields": ("modelo_ia_usado", "prompt_usado", "fecha_generacion"),
                "classes": ("wide",),
            },
        ),
        (
            "Resultados",
            {
                "fields": (
                    "exito",
                    "calidad_logo",
                    "tiempo_generacion_segundos",
                    "tiempo_generacion_display",
                ),
            },
        ),
        (
            "Archivo",
            {
                "fields": ("url_logo",),
            },
        ),
    )

    # Acciones masivas
    actions = ["regenerar_logos_fallidos", "marcar_como_alta_calidad"]

    def marca_numero(self, obj):
        """Muestra el número de marca"""
        return obj.marca.numero_marca

    marca_numero.short_description = "Número de Marca"
    marca_numero.admin_order_field = "marca__numero_marca"

    def marca_productor(self, obj):
        """Muestra el nombre del productor"""
        return obj.marca.nombre_productor

    marca_productor.short_description = "Productor"
    marca_productor.admin_order_field = "marca__nombre_productor"

    def success_indicator(self, obj):
        """Indicador visual de éxito"""
        if obj.exito:
            return format_html(
                '<span style="color: #4caf50; font-weight: bold;">✅ Exitoso</span>'
            )
        else:
            return format_html(
                '<span style="color: #f44336; font-weight: bold;">❌ Fallido</span>'
            )

    success_indicator.short_description = "Resultado"

    def tiempo_generacion_display(self, obj):
        """Muestra el tiempo de generación formateado"""
        return self.format_tiempo_segundos(obj.tiempo_generacion_segundos)

    tiempo_generacion_display.short_description = "Tiempo de Generación"

    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        return super().get_queryset(request).select_related("marca")

    # Acciones masivas
    def regenerar_logos_fallidos(self, request, queryset):
        """Regenera logos fallidos"""
        fallidos = queryset.filter(exito=False).count()
        self.message_user(
            request,
            f"Se programó la regeneración de {fallidos} logos fallidos. "
            "Este proceso se ejecutará en segundo plano.",
        )

    regenerar_logos_fallidos.short_description = "🔄 Regenerar logos fallidos"

    def marcar_como_alta_calidad(self, request, queryset):
        """Marca logos como alta calidad"""
        count = queryset.update(calidad_logo="ALTA")
        self.message_user(request, f"{count} logos marcados como alta calidad.")

    marcar_como_alta_calidad.short_description = "⭐ Marcar como alta calidad"
