# business_intelligence/admin.py
from django.contrib import admin
from django.db.models import Count, Avg, Sum
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import (
    MarcaGanadoBovino,
    LogoMarcaBovina,
    KPIGanadoBovino,
    HistorialEstadoMarca,
)


@admin.register(MarcaGanadoBovino)
class MarcaGanadoBovinoAdmin(admin.ModelAdmin):
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

    def colored_status(self, obj):
        colors = {
            "PENDIENTE": "#ff9800",
            "EN_PROCESO": "#2196f3",
            "APROBADO": "#4caf50",
            "RECHAZADO": "#f44336",
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            colors.get(obj.estado, "#757575"),
            obj.get_estado_display(),
        )

    colored_status.short_description = "Estado"
    colored_status.admin_order_field = "estado"

    def dias_transcurridos(self, obj):
        dias = obj.dias_desde_registro
        if dias <= 7:
            color = "#4caf50"  # Verde
        elif dias <= 30:
            color = "#ff9800"  # Naranja
        else:
            color = "#f44336"  # Rojo

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} días</span>', color, dias
        )

    dias_transcurridos.short_description = "Días desde registro"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

    # Acciones personalizadas
    actions = [
        "aprobar_marcas",
        "rechazar_marcas",
        "marcar_en_proceso",
        "calcular_tiempo_procesamiento",
        "exportar_reporte",
    ]

    def aprobar_marcas(self, request, queryset):
        ahora = timezone.now()
        count = 0
        for marca in queryset.filter(estado__in=["PENDIENTE", "EN_PROCESO"]):
            # Calcular tiempo de procesamiento
            if marca.fecha_registro:
                tiempo_horas = int(
                    (ahora - marca.fecha_registro).total_seconds() / 3600
                )
                marca.tiempo_procesamiento_horas = tiempo_horas

            marca.estado = "APROBADO"
            marca.fecha_procesamiento = ahora
            marca.save()

            # Crear registro en historial
            HistorialEstadoMarca.objects.create(
                marca=marca,
                estado_anterior=marca.estado,
                estado_nuevo="APROBADO",
                usuario_responsable=request.user.username,
                observaciones_cambio=f"Aprobado masivamente desde admin por {request.user.username}",
            )
            count += 1

        self.message_user(request, f"{count} marcas aprobadas exitosamente.")

    aprobar_marcas.short_description = "✅ Aprobar marcas seleccionadas"

    def rechazar_marcas(self, request, queryset):
        ahora = timezone.now()
        count = 0
        for marca in queryset.filter(estado__in=["PENDIENTE", "EN_PROCESO"]):
            estado_anterior = marca.estado
            marca.estado = "RECHAZADO"
            marca.fecha_procesamiento = ahora
            marca.save()

            # Crear registro en historial
            HistorialEstadoMarca.objects.create(
                marca=marca,
                estado_anterior=estado_anterior,
                estado_nuevo="RECHAZADO",
                usuario_responsable=request.user.username,
                observaciones_cambio=f"Rechazado masivamente desde admin por {request.user.username}",
            )
            count += 1

        self.message_user(request, f"{count} marcas rechazadas.")

    rechazar_marcas.short_description = "❌ Rechazar marcas seleccionadas"

    def marcar_en_proceso(self, request, queryset):
        count = queryset.filter(estado="PENDIENTE").update(estado="EN_PROCESO")
        self.message_user(request, f"{count} marcas marcadas como en proceso.")

    marcar_en_proceso.short_description = "🔄 Marcar como en proceso"

    def calcular_tiempo_procesamiento(self, request, queryset):
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


@admin.register(LogoMarcaBovina)
class LogoMarcaBovinaAdmin(admin.ModelAdmin):
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

    def marca_numero(self, obj):
        return obj.marca.numero_marca

    marca_numero.short_description = "Número de Marca"
    marca_numero.admin_order_field = "marca__numero_marca"

    def marca_productor(self, obj):
        return obj.marca.nombre_productor

    marca_productor.short_description = "Productor"
    marca_productor.admin_order_field = "marca__nombre_productor"

    def success_indicator(self, obj):
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
        segundos = obj.tiempo_generacion_segundos
        if segundos < 60:
            return f"{segundos} segundos"
        else:
            minutos = segundos // 60
            seg_restantes = segundos % 60
            return f"{minutos}m {seg_restantes}s"

    tiempo_generacion_display.short_description = "Tiempo de Generación"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("marca")

    actions = ["regenerar_logos_fallidos", "marcar_como_alta_calidad"]

    def regenerar_logos_fallidos(self, request, queryset):
        fallidos = queryset.filter(exito=False).count()
        self.message_user(
            request,
            f"Se programó la regeneración de {fallidos} logos fallidos. "
            "Este proceso se ejecutará en segundo plano.",
        )

    regenerar_logos_fallidos.short_description = "🔄 Regenerar logos fallidos"

    def marcar_como_alta_calidad(self, request, queryset):
        count = queryset.update(calidad_logo="ALTA")
        self.message_user(request, f"{count} logos marcados como alta calidad.")

    marcar_como_alta_calidad.short_description = "⭐ Marcar como alta calidad"


@admin.register(KPIGanadoBovino)
class KPIGanadoBovinoAdmin(admin.ModelAdmin):
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
        html = "<div style='padding: 10px; background-color: #f5f5f5; border-radius: 5px;'>"

        # Eficiencia de aprobación
        if obj.porcentaje_aprobacion >= 80:
            color_aprobacion = "#4caf50"
            icon_aprobacion = "✅"
        elif obj.porcentaje_aprobacion >= 60:
            color_aprobacion = "#ff9800"
            icon_aprobacion = "⚠️"
        else:
            color_aprobacion = "#f44336"
            icon_aprobacion = "❌"

        html += f"<p><strong>{icon_aprobacion} Aprobación:</strong> "
        html += f"<span style='color: {color_aprobacion};'>{obj.porcentaje_aprobacion:.1f}%</span></p>"

        # Eficiencia de tiempo
        if obj.tiempo_promedio_procesamiento <= 24:
            color_tiempo = "#4caf50"
            icon_tiempo = "⚡"
        elif obj.tiempo_promedio_procesamiento <= 72:
            color_tiempo = "#ff9800"
            icon_tiempo = "⏰"
        else:
            color_tiempo = "#f44336"
            icon_tiempo = "🐌"

        html += f"<p><strong>{icon_tiempo} Tiempo Promedio:</strong> "
        html += f"<span style='color: {color_tiempo};'>{obj.tiempo_promedio_procesamiento:.1f}h</span></p>"

        # Eficiencia de logos
        if obj.tasa_exito_logos >= 85:
            color_logos = "#4caf50"
            icon_logos = "🎨"
        elif obj.tasa_exito_logos >= 70:
            color_logos = "#ff9800"
            icon_logos = "🖼️"
        else:
            color_logos = "#f44336"
            icon_logos = "🚫"

        html += f"<p><strong>{icon_logos} Logos:</strong> "
        html += f"<span style='color: {color_logos};'>{obj.tasa_exito_logos:.1f}%</span></p>"

        html += "</div>"
        return format_html(html)

    eficiencia_display.short_description = "Resumen de Eficiencia"

    def has_add_permission(self, request):
        return False  # Los KPIs se generan automáticamente

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HistorialEstadoMarca)
class HistorialEstadoMarcaAdmin(admin.ModelAdmin):
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
        return obj.marca.numero_marca

    marca_numero.short_description = "Número de Marca"
    marca_numero.admin_order_field = "marca__numero_marca"

    def marca_productor(self, obj):
        return obj.marca.nombre_productor

    marca_productor.short_description = "Productor"
    marca_productor.admin_order_field = "marca__nombre_productor"

    def cambio_display(self, obj):
        colors = {
            "PENDIENTE": "#ff9800",
            "EN_PROCESO": "#2196f3",
            "APROBADO": "#4caf50",
            "RECHAZADO": "#f44336",
        }

        color_anterior = colors.get(obj.estado_anterior, "#757575")
        color_nuevo = colors.get(obj.estado_nuevo, "#757575")

        return format_html(
            '<span style="color: {};">{}</span> → <span style="color: {}; font-weight: bold;">{}</span>',
            color_anterior,
            obj.estado_anterior or "INICIAL",
            color_nuevo,
            obj.estado_nuevo,
        )

    cambio_display.short_description = "Cambio"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("marca")

    def has_add_permission(self, request):
        return False  # El historial se crea automáticamente

    def has_change_permission(self, request, obj=None):
        return False  # El historial no se debe modificar


# Configuración del sitio administrativo
admin.site.site_header = "🐄 Administración - Sistema de Marcas Ganaderas Bovinas"
admin.site.site_title = "Ganado Bovino Admin"
admin.site.index_title = "Panel de Control - Inteligencia de Negocios Ganadera"
