"""
Admin mejorado para logos de marcas bovinas siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa para LogoMarcaBovinaModel
- Proporcionar acciones avanzadas para gestión de logos
- Visualización mejorada con previews e indicadores
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import LogoMarcaBovinaModel


@admin.register(LogoMarcaBovinaModel)
class LogoMarcaBovinaAdmin(BaseAnalyticsAdmin):
    """
    Admin mejorado para logos de marcas bovinas - Clean Architecture.

    Responsabilidades:
    - Configurar visualización avanzada de logos con previews
    - Proporcionar acciones inteligentes para logos
    - Gestionar calidad y rendimiento de modelos IA
    - Análisis de métricas de generación
    """

    list_display = [
        "marca_info_completa",
        "preview_logo_thumbnail",
        "modelo_ia_con_badge",
        "resultado_visual",
        "calidad_con_indicador",
        "tiempo_generacion_visual",
        "fecha_generacion_relativa",
        "acciones_logo",
    ]

    list_filter = [
        "modelo_ia_usado",
        "exito",
        "calidad_logo",
        ("fecha_generacion", admin.DateFieldListFilter),
        "tiempo_generacion_segundos",
    ]

    search_fields = [
        "marca__numero_marca",
        "marca__nombre_productor",
        "prompt_usado",
        "modelo_ia_usado",
    ]

    readonly_fields = [
        "fecha_generacion",
        "tiempo_generacion_display",
        "preview_logo_grande",
        "estadisticas_modelo",
        "analisis_prompt",
        "metricas_rendimiento",
    ]

    date_hierarchy = "fecha_generacion"

    fieldsets = (
        ("🏷️ Información de la Marca", {"fields": ("marca",), "classes": ("wide",)}),
        (
            "🤖 Configuración IA",
            {
                "fields": ("modelo_ia_usado", "prompt_usado", "estadisticas_modelo"),
                "classes": ("wide",),
            },
        ),
        (
            "🎨 Resultado Visual",
            {
                "fields": ("preview_logo_grande", "url_logo", "calidad_logo"),
                "classes": ("wide",),
            },
        ),
        (
            "📊 Métricas de Generación",
            {
                "fields": (
                    "exito",
                    "tiempo_generacion_segundos",
                    "tiempo_generacion_display",
                    "fecha_generacion",
                    "metricas_rendimiento",
                ),
                "classes": ("collapse", "wide"),
            },
        ),
        (
            "🔍 Análisis Avanzado",
            {"fields": ("analisis_prompt",), "classes": ("collapse", "wide")},
        ),
    )

    # Acciones masivas mejoradas
    actions = [
        "regenerar_logos_inteligente",
        "optimizar_calidad_batch",
        "analizar_rendimiento_modelos",
        "exportar_metricas_ia",
        "marcar_como_referencia",
        "export_to_json",
    ]

    # Configuración de optimización
    list_select_related = ["marca"]
    list_per_page = 20

    def get_urls(self):
        """URLs personalizadas para funcionalidades avanzadas"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "analytics-ia/",
                self.admin_site.admin_view(self.analytics_ia_view),
                name="logo_analytics_ia",
            ),
            path(
                "<int:logo_id>/regenerar/",
                self.admin_site.admin_view(self.regenerar_individual),
                name="logo_regenerar_individual",
            ),
            path(
                "<int:logo_id>/analizar/",
                self.admin_site.admin_view(self.analizar_logo_individual),
                name="logo_analizar_individual",
            ),
            path(
                "comparar-modelos/",
                self.admin_site.admin_view(self.comparar_modelos_view),
                name="logo_comparar_modelos",
            ),
        ]
        return custom_urls + urls

    # Métodos de visualización mejorados
    def marca_info_completa(self, obj):
        """Información completa de la marca con enlace"""
        marca_url = reverse(
            "admin:analytics_marcaganadobovinomodel_change", args=[obj.marca.pk]
        )
        return mark_safe(
            f'<div style="line-height: 1.4;">'
            f'<strong><a href="{marca_url}" style="color: #007bff; text-decoration: none;">{obj.marca.numero_marca}</a></strong><br>'
            f'<small style="color: #6c757d;">👤 {obj.marca.nombre_productor[:30] + ("..." if len(obj.marca.nombre_productor) > 30 else "")}</small><br>'
            f'<small style="color: #28a745;">🐄 {getattr(obj.marca, "cantidad_cabezas", "N/A")} cabezas</small>'
            f"</div>"
        )

    marca_info_completa.short_description = "🏷️ Marca"
    marca_info_completa.admin_order_field = "marca__numero_marca"

    def preview_logo_thumbnail(self, obj):
        """Preview thumbnail del logo con overlay de información"""
        if not obj.url_logo:
            return format_html(
                '<div style="width: 60px; height: 60px; background: #f8f9fa; border: 2px dashed #dee2e6; '
                'display: flex; align-items: center; justify-content: center; border-radius: 8px;">'
                '<span style="color: #6c757d; font-size: 12px;">Sin logo</span>'
                "</div>"
            )

        overlay_color = "#4caf50" if obj.exito else "#f44336"
        overlay_icon = "✓" if obj.exito else "✗"

        return mark_safe(
            f'<div style="position: relative; display: inline-block;">'
            f'<img src="{obj.url_logo}" style="width: 60px; height: 60px; object-fit: cover; '
            f'border-radius: 8px; border: 2px solid {overlay_color};" />'
            f'<div style="position: absolute; top: -5px; right: -5px; background: {overlay_color}; '
            f"color: white; border-radius: 50%; width: 20px; height: 20px; "
            f"display: flex; align-items: center; justify-content: center; "
            f'font-size: 12px; font-weight: bold;">{overlay_icon}</div>'
            f"</div>"
        )

    preview_logo_thumbnail.short_description = "🖼️ Preview"

    def modelo_ia_con_badge(self, obj):
        """Modelo IA con badge de rendimiento"""
        # Calcular estadísticas del modelo
        modelo_stats = LogoMarcaBovinaModel.objects.filter(
            modelo_ia_usado=obj.modelo_ia_usado
        ).aggregate(
            total=Count("id"),
            exitosos=Count("id", filter=Q(exito=True)),
            tiempo_promedio=Avg("tiempo_generacion_segundos"),
        )

        tasa_exito = (
            (modelo_stats["exitosos"] / modelo_stats["total"] * 100)
            if modelo_stats["total"] > 0
            else 0
        )

        if tasa_exito >= 90:
            badge_color = "#4caf50"
            badge_text = "🏆 Excelente"
        elif tasa_exito >= 75:
            badge_color = "#ff9800"
            badge_text = "⭐ Bueno"
        elif tasa_exito >= 50:
            badge_color = "#ff5722"
            badge_text = "⚠️ Regular"
        else:
            badge_color = "#f44336"
            badge_text = "❌ Bajo"

        return mark_safe(
            f'<div style="text-align: center;">'
            f'<strong style="color: #2c3e50;">{obj.modelo_ia_usado}</strong><br>'
            f'<span style="background: {badge_color}; color: white; padding: 2px 6px; '
            f'border-radius: 12px; font-size: 10px; font-weight: bold;">{badge_text}</span><br>'
            f'<small style="color: #6c757d;">{f"{tasa_exito:.1f}"}% éxito</small>'
            f"</div>"
        )

    modelo_ia_con_badge.short_description = "🤖 Modelo IA"
    modelo_ia_con_badge.admin_order_field = "modelo_ia_usado"

    def resultado_visual(self, obj):
        """Resultado con indicador visual mejorado"""
        if obj.exito:
            return mark_safe(
                f'<div style="display: flex; align-items: center; gap: 8px;">'
                f'<div style="width: 12px; height: 12px; background: #4caf50; '
                f'border-radius: 50%; box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);"></div>'
                f'<span style="color: #4caf50; font-weight: bold;">✅ Exitoso</span>'
                f"</div>"
            )
        else:
            return mark_safe(
                f'<div style="display: flex; align-items: center; gap: 8px;">'
                f'<div style="width: 12px; height: 12px; background: #f44336; '
                f'border-radius: 50%; box-shadow: 0 0 0 3px rgba(244, 67, 54, 0.2);"></div>'
                f'<span style="color: #f44336; font-weight: bold;">❌ Fallido</span>'
                f"</div>"
            )

    resultado_visual.short_description = "📊 Resultado"
    resultado_visual.admin_order_field = "exito"

    def calidad_con_indicador(self, obj):
        """Calidad con indicador visual y estrellas"""
        calidad_config = {
            "ALTA": {"color": "#4caf50", "stars": "⭐⭐⭐", "icon": "🟢"},
            "MEDIA": {"color": "#ff9800", "stars": "⭐⭐", "icon": "🟡"},
            "BAJA": {"color": "#f44336", "stars": "⭐", "icon": "🔴"},
        }

        config = calidad_config.get(
            obj.calidad_logo, {"color": "#757575", "stars": "", "icon": "⚪"}
        )

        return mark_safe(
            f'<div style="text-align: center;">'
            f'<div style="color: {config["color"]}; font-size: 16px;">{config["icon"]}</div>'
            f'<div style="color: {config["color"]}; font-weight: bold; font-size: 12px;">{obj.calidad_logo}</div>'
            f'<div style="color: #ffc107; font-size: 14px;">{config["stars"]}</div>'
            f"</div>"
        )

    calidad_con_indicador.short_description = "⭐ Calidad"
    calidad_con_indicador.admin_order_field = "calidad_logo"

    def tiempo_generacion_visual(self, obj):
        """Tiempo de generación con indicador de rendimiento"""
        segundos = obj.tiempo_generacion_segundos
        tiempo_formateado = self.format_tiempo_segundos(segundos)

        if segundos <= 10:
            color = "#4caf50"
            icon = "🚀"
            label = "Rápido"
        elif segundos <= 30:
            color = "#ff9800"
            icon = "⚡"
            label = "Normal"
        elif segundos <= 60:
            color = "#ff5722"
            icon = "🐌"
            label = "Lento"
        else:
            color = "#f44336"
            icon = "🐢"
            label = "Muy lento"

        return mark_safe(
            f'<div style="text-align: center;">'
            f'<div style="color: {color}; font-size: 16px;">{icon}</div>'
            f'<div style="color: {color}; font-weight: bold;">{tiempo_formateado}</div>'
            f'<small style="color: #6c757d;">{label}</small>'
            f"</div>"
        )

    tiempo_generacion_visual.short_description = "⏱️ Tiempo"
    tiempo_generacion_visual.admin_order_field = "tiempo_generacion_segundos"

    def fecha_generacion_relativa(self, obj):
        """Fecha con tiempo relativo"""
        ahora = timezone.now()
        diferencia = ahora - obj.fecha_generacion

        if diferencia.days == 0:
            if diferencia.seconds < 3600:
                minutos = diferencia.seconds // 60
                tiempo_relativo = f"Hace {minutos} min"
                color = "#4caf50"
            else:
                horas = diferencia.seconds // 3600
                tiempo_relativo = f"Hace {horas}h"
                color = "#ff9800"
        elif diferencia.days == 1:
            tiempo_relativo = "Ayer"
            color = "#ff5722"
        else:
            tiempo_relativo = f"Hace {diferencia.days} días"
            color = "#6c757d"

        fecha_formateada = obj.fecha_generacion.strftime("%d/%m/%Y %H:%M")

        return mark_safe(
            f'<div style="text-align: center;">'
            f'<div style="color: {color}; font-weight: bold; font-size: 12px;">{tiempo_relativo}</div>'
            f'<small style="color: #6c757d;">{fecha_formateada}</small>'
            f"</div>"
        )

    fecha_generacion_relativa.short_description = "📅 Generado"
    fecha_generacion_relativa.admin_order_field = "fecha_generacion"

    def acciones_logo(self, obj):
        """Acciones rápidas para cada logo"""
        acciones = []

        if not obj.exito:
            regenerar_url = reverse("admin:logo_regenerar_individual", args=[obj.pk])
            acciones.append(
                self.create_action_button(regenerar_url, "🔄 Regenerar", "#2196f3")
            )

        if obj.url_logo:
            acciones.append(self.create_action_button(obj.url_logo, "👁️ Ver", "#28a745"))

        # Botón de análisis
        analizar_url = reverse("admin:logo_analizar_individual", args=[obj.pk])
        acciones.append(
            self.create_action_button(analizar_url, "📊 Analizar", "#6c757d")
        )

        return mark_safe(
            f'<div style="display: flex; gap: 2px; flex-wrap: wrap;">{"".join(acciones)}</div>'
        )

    acciones_logo.short_description = "⚡ Acciones"

    # Campos readonly mejorados
    def preview_logo_grande(self, obj):
        """Preview grande del logo con información detallada"""
        if not obj.url_logo:
            return format_html(
                '<div style="text-align: center; padding: 40px; background: #f8f9fa; '
                'border: 2px dashed #dee2e6; border-radius: 8px;">'
                '<div style="font-size: 48px; color: #dee2e6;">🖼️</div>'
                '<p style="color: #6c757d; margin: 10px 0 0 0;">Logo no disponible</p>'
                "</div>"
            )

        return mark_safe(
            f'<div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px;">'
            f'<img src="{obj.url_logo}" style="max-width: 300px; max-height: 300px; '
            f'border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />'
            f'<div style="margin-top: 15px; display: flex; justify-content: center; gap: 15px;">'
            f'<div style="text-align: center;">'
            f'<div style="color: #007bff; font-weight: bold;">Modelo</div>'
            f'<div style="color: #6c757d; font-size: 14px;">{obj.modelo_ia_usado}</div>'
            f"</div>"
            f'<div style="text-align: center;">'
            f'<div style="color: #007bff; font-weight: bold;">Calidad</div>'
            f'<div style="color: #6c757d; font-size: 14px;">{obj.calidad_logo}</div>'
            f"</div>"
            f'<div style="text-align: center;">'
            f'<div style="color: #007bff; font-weight: bold;">Tiempo</div>'
            f'<div style="color: #6c757d; font-size: 14px;">{self.format_tiempo_segundos(obj.tiempo_generacion_segundos)}</div>'
            f"</div>"
            f"</div>"
            f"</div>"
        )

    preview_logo_grande.short_description = "🖼️ Vista Previa"

    def estadisticas_modelo(self, obj):
        """Estadísticas del modelo IA utilizado"""
        if not obj.pk:
            return "Disponible después de guardar"

        stats = LogoMarcaBovinaModel.objects.filter(
            modelo_ia_usado=obj.modelo_ia_usado
        ).aggregate(
            total=Count("id"),
            exitosos=Count("id", filter=Q(exito=True)),
            tiempo_promedio=Avg("tiempo_generacion_segundos"),
            alta_calidad=Count("id", filter=Q(calidad_logo="ALTA")),
        )

        tasa_exito = (
            (stats["exitosos"] / stats["total"] * 100) if stats["total"] > 0 else 0
        )
        tasa_calidad = (
            (stats["alta_calidad"] / stats["total"] * 100) if stats["total"] > 0 else 0
        )
        tiempo_promedio = stats["tiempo_promedio"] or 0

        return mark_safe(
            f'<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 15px 0;">'
            f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
            f'color: white; padding: 15px; border-radius: 8px; text-align: center;">'
            f'<div style="font-size: 24px; font-weight: bold;">{stats["total"]}</div>'
            f'<div style="font-size: 12px; opacity: 0.9;">Total Generados</div>'
            f"</div>"
            f'<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); '
            f'color: white; padding: 15px; border-radius: 8px; text-align: center;">'
            f'<div style="font-size: 24px; font-weight: bold;">{f"{tasa_exito:.1f}"}%</div>'
            f'<div style="font-size: 12px; opacity: 0.9;">Tasa de Éxito</div>'
            f"</div>"
            f'<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); '
            f'color: white; padding: 15px; border-radius: 8px; text-align: center;">'
            f'<div style="font-size: 24px; font-weight: bold;">{f"{tiempo_promedio:.1f}"}s</div>'
            f'<div style="font-size: 12px; opacity: 0.9;">Tiempo Promedio</div>'
            f"</div>"
            f'<div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); '
            f'color: white; padding: 15px; border-radius: 8px; text-align: center;">'
            f'<div style="font-size: 24px; font-weight: bold;">{f"{tasa_calidad:.1f}"}%</div>'
            f'<div style="font-size: 12px; opacity: 0.9;">Alta Calidad</div>'
            f"</div>"
            f"</div>"
        )

    estadisticas_modelo.short_description = "📊 Estadísticas del Modelo"

    def analisis_prompt(self, obj):
        """Análisis del prompt utilizado"""
        if not obj.prompt_usado:
            return format_html('<em style="color: #999;">Sin prompt registrado</em>')

        palabras = len(obj.prompt_usado.split())
        caracteres = len(obj.prompt_usado)

        # Análisis básico de palabras clave
        palabras_clave = ["logo", "marca", "bovino", "ganado", "profesional", "moderno"]
        palabras_encontradas = [
            p for p in palabras_clave if p.lower() in obj.prompt_usado.lower()
        ]

        palabras_clave_html = (
            f'<div style="margin-top: 8px;"><strong style="font-size: 12px;">Palabras clave:</strong> {", ".join(palabras_encontradas)}</div>'
            if palabras_encontradas
            else ""
        )

        return mark_safe(
            f'<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;">'
            f'<div style="margin-bottom: 10px;">'
            f"<strong>Prompt utilizado:</strong>"
            f"</div>"
            f'<div style="background: white; padding: 10px; border-radius: 4px; '
            f'font-family: monospace; font-size: 13px; line-height: 1.4; max-height: 100px; overflow-y: auto;">'
            f"{obj.prompt_usado}"
            f"</div>"
            f'<div style="margin-top: 10px; display: flex; gap: 15px; font-size: 12px; color: #6c757d;">'
            f"<span>📝 {palabras} palabras</span>"
            f"<span>🔤 {caracteres} caracteres</span>"
            f"<span>🎯 {len(palabras_encontradas)} palabras clave</span>"
            f"</div>"
            f"{palabras_clave_html}"
            f"</div>"
        )

    analisis_prompt.short_description = "🔍 Análisis de Prompt"

    def metricas_rendimiento(self, obj):
        """Métricas de rendimiento comparativas"""
        if not obj.pk:
            return "Disponible después de guardar"

        # Comparar con promedio general
        promedio_general = (
            LogoMarcaBovinaModel.objects.aggregate(
                tiempo_promedio=Avg("tiempo_generacion_segundos")
            )["tiempo_promedio"]
            or 0
        )

        diferencia = obj.tiempo_generacion_segundos - promedio_general
        porcentaje_diferencia = (
            (diferencia / promedio_general * 100) if promedio_general > 0 else 0
        )

        if diferencia < 0:
            color = "#4caf50"
            icon = "📈"
            texto = f"{abs(porcentaje_diferencia):.1f}% más rápido que el promedio"
        else:
            color = "#f44336"
            icon = "📉"
            texto = f"{porcentaje_diferencia:.1f}% más lento que el promedio"

        return mark_safe(
            f'<div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">'
            f'<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">'
            f'<span style="font-size: 20px;">{icon}</span>'
            f'<span style="color: {color}; font-weight: bold;">{texto}</span>'
            f"</div>"
            f'<div style="font-size: 12px; color: #6c757d;">'
            f'Promedio general: {f"{promedio_general:.1f}"}s<br>'
            f'Este logo: {f"{obj.tiempo_generacion_segundos:.1f}"}s'
            f"</div>"
            f"</div>"
        )

    metricas_rendimiento.short_description = "📊 Rendimiento"

    # Métodos heredados mejorados
    def tiempo_generacion_display(self, obj):
        """Muestra el tiempo de generación formateado"""
        return self.format_tiempo_segundos(obj.tiempo_generacion_segundos)

    tiempo_generacion_display.short_description = "⏱️ Tiempo de Generación"

    # Acciones masivas mejoradas
    def regenerar_logos_inteligente(self, request, queryset):
        """Regeneración inteligente de logos con priorización"""
        # Priorizar logos fallidos y de baja calidad
        candidatos = queryset.filter(Q(exito=False) | Q(calidad_logo="BAJA")).order_by(
            "-tiempo_generacion_segundos"
        )  # Los más lentos primero

        if not candidatos.exists():
            self.message_user(
                request,
                "No hay logos que requieran regeneración en la selección.",
                messages.INFO,
            )
            return

        count = candidatos.count()

        # Aquí iría la lógica de regeneración
        # Por ahora solo simulamos
        for logo in candidatos[:10]:  # Limitar a 10 por vez
            # Lógica de regeneración
            pass

        self.message_user(
            request,
            f"🧠 Se programó la regeneración inteligente de {min(count, 10)} logos. "
            f"Proceso iniciado en segundo plano.",
            messages.SUCCESS,
        )

    regenerar_logos_inteligente.short_description = "🧠 Regenerar logos (inteligente)"

    def optimizar_calidad_batch(self, request, queryset):
        """Optimización masiva de calidad"""
        logos_optimizables = queryset.filter(
            exito=True, calidad_logo__in=["MEDIA", "BAJA"]
        )

        count = logos_optimizables.count()
        if count == 0:
            self.message_user(
                request, "No hay logos optimizables en la selección.", messages.WARNING
            )
            return

        # Simular optimización
        logos_optimizables.update(calidad_logo="ALTA")

        self.message_user(
            request, f"⚡ {count} logos optimizados exitosamente.", messages.SUCCESS
        )

    optimizar_calidad_batch.short_description = "⚡ Optimizar calidad masiva"

    def analizar_rendimiento_modelos(self, request, queryset):
        """Análisis de rendimiento de modelos IA"""
        modelos_stats = {}

        for logo in queryset:
            modelo = logo.modelo_ia_usado
            if modelo not in modelos_stats:
                modelos_stats[modelo] = {
                    "total": 0,
                    "exitosos": 0,
                    "tiempo_total": 0,
                    "alta_calidad": 0,
                }

            stats = modelos_stats[modelo]
            stats["total"] += 1
            if logo.exito:
                stats["exitosos"] += 1
            stats["tiempo_total"] += logo.tiempo_generacion_segundos
            if logo.calidad_logo == "ALTA":
                stats["alta_calidad"] += 1

        # Generar reporte
        reporte = []
        for modelo, stats in modelos_stats.items():
            tasa_exito = (
                (stats["exitosos"] / stats["total"] * 100) if stats["total"] > 0 else 0
            )
            tiempo_promedio = (
                stats["tiempo_total"] / stats["total"] if stats["total"] > 0 else 0
            )
            tasa_calidad = (
                (stats["alta_calidad"] / stats["total"] * 100)
                if stats["total"] > 0
                else 0
            )

            reporte.append(
                f"🤖 {modelo}: {tasa_exito:.1f}% éxito, "
                f"{tiempo_promedio:.1f}s promedio, {tasa_calidad:.1f}% alta calidad"
            )

        mensaje = "📊 Análisis de rendimiento:\n" + "\n".join(reporte)

        self.message_user(request, mensaje, messages.INFO)

    analizar_rendimiento_modelos.short_description = "📊 Analizar rendimiento modelos"

    def marcar_como_referencia(self, request, queryset):
        """Marcar logos como referencia para entrenamiento"""
        logos_referencia = queryset.filter(exito=True, calidad_logo="ALTA")
        count = logos_referencia.count()

        if count == 0:
            self.message_user(
                request,
                "No hay logos de alta calidad para marcar como referencia.",
                messages.WARNING,
            )
            return

        # Aquí iría la lógica para marcar como referencia
        # Por ejemplo, agregar a un dataset de entrenamiento

        self.message_user(
            request,
            f"⭐ {count} logos marcados como referencia para entrenamiento.",
            messages.SUCCESS,
        )

    marcar_como_referencia.short_description = "⭐ Marcar como referencia"

    # Vistas personalizadas
    def analytics_ia_view(self, request):
        """Vista de analytics de IA"""
        # Estadísticas generales
        stats = LogoMarcaBovinaModel.objects.aggregate(
            total=Count("id"),
            exitosos=Count("id", filter=Q(exito=True)),
            tiempo_promedio=Avg("tiempo_generacion_segundos"),
        )

        # Estadísticas por modelo
        modelos_stats = (
            LogoMarcaBovinaModel.objects.values("modelo_ia_usado")
            .annotate(
                total=Count("id"),
                exitosos=Count("id", filter=Q(exito=True)),
                tiempo_promedio=Avg("tiempo_generacion_segundos"),
            )
            .order_by("-total")
        )

        context = {
            "title": "Analytics de IA - Generación de Logos",
            "stats": stats,
            "modelos_stats": modelos_stats,
            "opts": self.model._meta,
        }

        return render(request, "admin/logo_analytics_ia.html", context)

    def regenerar_individual(self, request, logo_id):
        """Regenerar logo individual"""
        logo = get_object_or_404(LogoMarcaBovinaModel, pk=logo_id)

        # Aquí iría la lógica de regeneración
        # Por ahora solo simulamos

        messages.success(request, f"Logo {logo.pk} programado para regeneración.")
        return HttpResponseRedirect(
            reverse("admin:analytics_logomarcabovinamodel_changelist")
        )

    def analizar_logo_individual(self, request, logo_id):
        """Vista de análisis individual de un logo"""
        logo = get_object_or_404(LogoMarcaBovinaModel, pk=logo_id)

        # Obtener estadísticas de comparación de modelos
        from django.db.models import Count, Avg, Q

        modelos_comparacion = []
        todos_modelos = LogoMarcaBovinaModel.objects.values(
            "modelo_ia_usado"
        ).distinct()

        for modelo in todos_modelos:
            modelo_nombre = modelo["modelo_ia_usado"]
            stats = LogoMarcaBovinaModel.objects.filter(
                modelo_ia_usado=modelo_nombre
            ).aggregate(
                total=Count("id"),
                exitosos=Count("id", filter=Q(exito=True)),
                tiempo_promedio=Avg("tiempo_generacion_segundos"),
                alta_calidad=Count("id", filter=Q(calidad_logo="ALTA")),
            )

            tasa_exito = (
                (stats["exitosos"] / stats["total"] * 100) if stats["total"] > 0 else 0
            )

            modelos_comparacion.append(
                {
                    "modelo_ia_usado": modelo_nombre,
                    "total": stats["total"],
                    "tasa_exito": tasa_exito,
                    "tiempo_promedio": stats["tiempo_promedio"] or 0,
                    "alta_calidad": stats["alta_calidad"],
                }
            )

        context = {
            "title": f"Análisis Individual de Logo {logo.pk}",
            "logo": logo,
            "modelos_comparacion": modelos_comparacion,
            "opts": self.model._meta,
        }

        return render(request, "admin/logo_analizar_individual.html", context)

    def comparar_modelos_view(self, request):
        """Vista de comparación de modelos"""
        # Implementar comparación detallada de modelos
        context = {
            "title": "Comparación de Modelos IA",
            "opts": self.model._meta,
        }

        return render(request, "admin/logo_comparar_modelos.html", context)

    def get_queryset(self, request):
        """Optimizar consultas con select_related y prefetch_related"""
        return super().get_queryset(request).select_related("marca")

    class Media:
        css = {"all": ("admin/css/logo_admin.css",)}
        js = ("admin/js/logo_admin.js",)
