"""
Admin para marcas de ganado bovino siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa para MarcaGanadoBovinoModel
- Proporcionar acciones masivas para gestión de marcas
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import MarcaGanadoBovinoModel, HistorialEstadoMarcaModel


@admin.register(MarcaGanadoBovinoModel)
class MarcaGanadoBovinoAdmin(BaseAnalyticsAdmin):
    """
    Admin para marcas de ganado bovino - Clean Architecture.

    Responsabilidades:
    - Configurar visualización de marcas
    - Proporcionar acciones masivas
    - Gestionar estados de marcas
    """

    list_display = [
        "numero_marca",
        "nombre_productor",
        "raza_bovino",
        "proposito_ganado",
        "cantidad_cabezas",
        "departamento",
        "estado",
        "monto_certificacion",
        "fecha_registro",
        "colored_status",
        "dias_transcurridos",
    ]

    list_filter = [
        "estado",
        "raza_bovino",
        "proposito_ganado",
        "departamento",
        "fecha_registro",
        "fecha_procesamiento",
    ]

    search_fields = [
        "numero_marca",
        "nombre_productor",
        "ci_productor",
        "municipio",
        "comunidad",
    ]

    readonly_fields = [
        "fecha_registro",
        "actualizado_en",
        "tiempo_procesamiento_horas",
        "dias_transcurridos",
        "esta_procesado",
    ]

    date_hierarchy = "fecha_registro"

    fieldsets = (
        (
            "Información de la Marca",
            {
                "fields": (
                    "numero_marca",
                    "estado",
                    "fecha_registro",
                    "fecha_procesamiento",
                )
            },
        ),
        (
            "Datos del Productor",
            {
                "fields": (
                    "nombre_productor",
                    "ci_productor",
                    "telefono_productor",
                    "creado_por",
                )
            },
        ),
        (
            "Información del Ganado Bovino",
            {
                "fields": ("raza_bovino", "proposito_ganado", "cantidad_cabezas"),
                "classes": ("wide",),
            },
        ),
        (
            "Ubicación Geográfica",
            {
                "fields": ("departamento", "municipio", "comunidad"),
                "classes": ("collapse",),
            },
        ),
        (
            "Procesamiento y Certificación",
            {
                "fields": (
                    "monto_certificacion",
                    "tiempo_procesamiento_horas",
                    "observaciones",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Metadatos",
            {
                "fields": ("actualizado_en", "dias_transcurridos", "esta_procesado"),
                "classes": ("collapse",),
            },
        ),
    )

    # Acciones masivas (Single Responsibility Principle)
    actions = [
        "aprobar_marcas",
        "rechazar_marcas",
        "marcar_en_proceso",
        "calcular_tiempo_procesamiento",
    ]

    def colored_status(self, obj):
        """Muestra el estado con colores"""
        return self.format_estado_with_color(obj)

    colored_status.short_description = "Estado"
    colored_status.admin_order_field = "estado"

    def dias_transcurridos(self, obj):
        """Muestra los días transcurridos con colores"""
        dias = obj.dias_desde_registro
        return self.format_dias_con_color(dias)

    dias_transcurridos.short_description = "Días desde registro"

    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        return super().get_queryset(request).select_related()

    # Acciones masivas (Open/Closed Principle)
    def aprobar_marcas(self, request, queryset):
        """Aprueba las marcas seleccionadas"""
        ahora = timezone.now()
        count = 0

        for marca in queryset.filter(estado__in=["PENDIENTE", "EN_PROCESO"]):
            self._procesar_aprobacion_marca(marca, ahora, request.user.username)
            count += 1

        self.message_user(request, f"{count} marcas aprobadas exitosamente.")

    aprobar_marcas.short_description = "✅ Aprobar marcas seleccionadas"

    def rechazar_marcas(self, request, queryset):
        """Rechaza las marcas seleccionadas"""
        ahora = timezone.now()
        count = 0

        for marca in queryset.filter(estado__in=["PENDIENTE", "EN_PROCESO"]):
            self._procesar_rechazo_marca(marca, ahora, request.user.username)
            count += 1

        self.message_user(request, f"{count} marcas rechazadas.")

    rechazar_marcas.short_description = "❌ Rechazar marcas seleccionadas"

    def marcar_en_proceso(self, request, queryset):
        """Marca las marcas como en proceso"""
        count = queryset.filter(estado="PENDIENTE").update(estado="EN_PROCESO")
        self.message_user(request, f"{count} marcas marcadas como en proceso.")

    marcar_en_proceso.short_description = "🔄 Marcar como en proceso"

    def calcular_tiempo_procesamiento(self, request, queryset):
        """Calcula el tiempo de procesamiento"""
        ahora = timezone.now()
        count = 0

        for marca in queryset.filter(fecha_procesamiento__isnull=False):
            if marca.fecha_registro:
                tiempo_horas = int(
                    (marca.fecha_procesamiento - marca.fecha_registro).total_seconds()
                    / 3600
                )
                marca.tiempo_procesamiento_horas = tiempo_horas
                marca.save()
                count += 1

        self.message_user(
            request, f"Tiempo de procesamiento calculado para {count} marcas."
        )

    calcular_tiempo_procesamiento.short_description = (
        "⏱️ Calcular tiempo de procesamiento"
    )

    # Métodos privados (Encapsulation)
    def _procesar_aprobacion_marca(self, marca, ahora, username):
        """Procesa la aprobación de una marca"""
        if marca.fecha_registro:
            tiempo_horas = int((ahora - marca.fecha_registro).total_seconds() / 3600)
            marca.tiempo_procesamiento_horas = tiempo_horas

        marca.estado = "APROBADO"
        marca.fecha_procesamiento = ahora
        marca.save()

        self._crear_historial_cambio(
            marca, "APROBADO", username, "Aprobado masivamente"
        )

    def _procesar_rechazo_marca(self, marca, ahora, username):
        """Procesa el rechazo de una marca"""
        estado_anterior = marca.estado
        marca.estado = "RECHAZADO"
        marca.fecha_procesamiento = ahora
        marca.save()

        self._crear_historial_cambio(
            marca, "RECHAZADO", username, "Rechazado masivamente"
        )

    def _crear_historial_cambio(self, marca, estado_nuevo, username, observacion):
        """Crea registro en historial de cambios"""
        HistorialEstadoMarcaModel.objects.create(
            marca=marca,
            estado_anterior=marca.estado,
            estado_nuevo=estado_nuevo,
            usuario_responsable=username,
            observaciones_cambio=f"{observacion} desde admin por {username}",
        )
