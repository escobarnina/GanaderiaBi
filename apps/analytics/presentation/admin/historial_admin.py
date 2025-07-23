"""
Admin para historial de estados siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa para HistorialEstadoMarcaModel
- Proporcionar visualización de cambios de estado
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import HistorialEstadoMarcaModel


@admin.register(HistorialEstadoMarcaModel)
class HistorialEstadoMarcaAdmin(BaseAnalyticsAdmin):
    """
    Admin para historial de estados - Clean Architecture.

    Responsabilidades:
    - Configurar visualización de historial
    - Proporcionar auditoría de cambios
    - Gestionar trazabilidad de estados
    """

    list_display = [
        "marca_numero",
        "marca_productor",
        "estado_anterior",
        "estado_nuevo",
        "fecha_cambio",
        "usuario_responsable",
        "cambio_display",
    ]

    list_filter = [
        "estado_anterior",
        "estado_nuevo",
        "fecha_cambio",
        "usuario_responsable",
    ]

    search_fields = [
        "marca__numero_marca",
        "marca__nombre_productor",
        "usuario_responsable",
        "observaciones_cambio",
    ]

    readonly_fields = [
        "marca",
        "estado_anterior",
        "estado_nuevo",
        "fecha_cambio",
        "usuario_responsable",
    ]

    date_hierarchy = "fecha_cambio"

    fieldsets = (
        ("Información de la Marca", {"fields": ("marca",)}),
        (
            "Cambio de Estado",
            {
                "fields": ("estado_anterior", "estado_nuevo", "fecha_cambio"),
                "classes": ("wide",),
            },
        ),
        ("Responsable", {"fields": ("usuario_responsable",)}),
        ("Observaciones", {"fields": ("observaciones_cambio",), "classes": ("wide",)}),
    )

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

    def cambio_display(self, obj):
        """Muestra el cambio de estado con colores"""
        return self._formatear_cambio_estado(obj)

    cambio_display.short_description = "Cambio"

    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        return super().get_queryset(request).select_related("marca")

    def has_add_permission(self, request):
        """El historial se crea automáticamente"""
        return False

    def has_change_permission(self, request, obj=None):
        """El historial no se debe modificar"""
        return False

    # Métodos privados (Encapsulation)
    def _formatear_cambio_estado(self, obj):
        """Formatea el cambio de estado con colores"""
        color_anterior = self.get_estado_color(obj.estado_anterior)
        color_nuevo = self.get_estado_color(obj.estado_nuevo)

        return format_html(
            '<span style="color: {};">{}</span> → <span style="color: {}; font-weight: bold;">{}</span>',
            color_anterior,
            obj.estado_anterior or "INICIAL",
            color_nuevo,
            obj.estado_nuevo,
        )
