"""
Clase base para configuraciones de admin siguiendo Clean Architecture.

Esta clase proporciona funcionalidades comunes para todos los admins,
siguiendo el principio DRY y la separación de responsabilidades.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone


class BaseAnalyticsAdmin(admin.ModelAdmin):
    """
    Clase base para admins de analytics siguiendo Clean Architecture.

    Proporciona funcionalidades comunes como:
    - Configuración de colores para estados
    - Métodos de formateo de tiempo
    - Configuración de permisos
    """

    # Colores para estados (Single Responsibility Principle)
    ESTADO_COLORS = {
        "PENDIENTE": "#ff9800",
        "EN_PROCESO": "#2196f3",
        "APROBADO": "#4caf50",
        "RECHAZADO": "#f44336",
    }

    def get_estado_color(self, estado):
        """Obtiene el color para un estado específico"""
        return self.ESTADO_COLORS.get(estado, "#757575")

    def format_estado_with_color(self, obj, estado_field="estado"):
        """Formatea el estado con color"""
        estado = getattr(obj, estado_field)
        color = self.get_estado_color(estado)
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color,
            obj.get_estado_display() if hasattr(obj, "get_estado_display") else estado,
        )

    def format_tiempo_segundos(self, segundos):
        """Formatea tiempo en segundos a formato legible"""
        if segundos < 60:
            return f"{segundos} segundos"
        else:
            minutos = segundos // 60
            seg_restantes = segundos % 60
            return f"{minutos}m {seg_restantes}s"

    def format_dias_con_color(self, dias):
        """Formatea días con color según el rango"""
        if dias <= 7:
            color = "#4caf50"  # Verde
        elif dias <= 30:
            color = "#ff9800"  # Naranja
        else:
            color = "#f44336"  # Rojo

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} días</span>', color, dias
        )

    def has_add_permission(self, request):
        """Permisos de creación - sobrescribir en subclases"""
        return True

    def has_change_permission(self, request, obj=None):
        """Permisos de modificación - sobrescribir en subclases"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Permisos de eliminación - sobrescribir en subclases"""
        return True
