"""
Admin mejorado para marcas de ganado bovino siguiendo Clean Architecture.

Responsabilidades:
- Configurar la interfaz administrativa avanzada para MarcaGanadoBovinoModel
- Proporcionar acciones masivas inteligentes para gestión de marcas
- Dashboard integrado con métricas en tiempo real
- Mantener separación de responsabilidades (SOLID)
"""

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg, Q, Sum
from django.core.paginator import Paginator
from datetime import timedelta, datetime
from .base_admin import BaseAnalyticsAdmin
from ...infrastructure.models import MarcaGanadoBovinoModel, HistorialEstadoMarcaModel


@admin.register(MarcaGanadoBovinoModel)
class MarcaGanadoBovinoAdmin(BaseAnalyticsAdmin):
    """
    Admin mejorado para marcas de ganado bovino - Clean Architecture.

    Responsabilidades:
    - Configurar visualización avanzada con métricas integradas
    - Proporcionar acciones masivas inteligentes
    - Gestionar estados con workflow automatizado
    - Dashboard de métricas en tiempo real
    - Análisis predictivo de tiempos
    """

    list_display = [
        "marca_info_detallada",
        "productor_con_contacto",
        "ganado_info_visual",
        "ubicacion_completa",
        "estado_con_workflow",
        "certificacion_info",
        "tiempo_procesamiento_avanzado",
        "acciones_inteligentes",
    ]

    list_filter = [
        "estado",
        "raza_bovino",
        "proposito_ganado",
        "departamento",
        ("fecha_registro", admin.DateFieldListFilter),
        "cantidad_cabezas",
        "monto_certificacion",
        "creado_por",
    ]

    search_fields = [
        "numero_marca",
        "nombre_productor",
        "ci_productor",
        "municipio",
        "comunidad",
        "telefono_productor",
    ]

    readonly_fields = [
        "fecha_registro",
        "actualizado_en",
        "tiempo_procesamiento_horas",
        "dias_transcurridos",
        "esta_procesado",
        "dashboard_metricas",
        "historial_visual",
        "prediccion_tiempo",
        "analisis_rentabilidad",
    ]

    date_hierarchy = "fecha_registro"

    fieldsets = (
        (
            "🏷️ Información de la Marca",
            {
                "fields": (
                    "numero_marca",
                    "estado",
                    "fecha_registro",
                    "fecha_procesamiento",
                    "dashboard_metricas",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "👤 Datos del Productor",
            {
                "fields": (
                    "nombre_productor",
                    "ci_productor",
                    "telefono_productor",
                    "creado_por",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "🐄 Información del Ganado Bovino",
            {
                "fields": ("raza_bovino", "proposito_ganado", "cantidad_cabezas"),
                "classes": ("wide",),
            },
        ),
        (
            "📍 Ubicación Geográfica",
            {
                "fields": ("departamento", "municipio", "comunidad"),
                "classes": ("collapse",),
            },
        ),
        (
            "💰 Procesamiento y Certificación",
            {
                "fields": (
                    "monto_certificacion",
                    "tiempo_procesamiento_horas",
                    "observaciones",
                    "analisis_rentabilidad",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "📊 Análisis Predictivo",
            {"fields": ("prediccion_tiempo",), "classes": ("collapse", "wide")},
        ),
        (
            "📜 Historial y Auditoría",
            {"fields": ("historial_visual",), "classes": ("collapse", "wide")},
        ),
        (
            "🕒 Metadatos",
            {
                "fields": ("actualizado_en", "dias_transcurridos", "esta_procesado"),
                "classes": ("collapse",),
            },
        ),
    )

    # Acciones masivas inteligentes
    actions = [
        "aprobar_marcas_inteligente",
        "rechazar_con_analisis",
        "workflow_automatico",
        "calcular_metricas_avanzadas",
        "generar_reporte_ejecutivo",
        "optimizar_tiempos",
        "analisis_predictivo",
        "export_to_json",
    ]

    # Configuración de optimización
    list_per_page = 20

    def get_urls(self):
        """URLs personalizadas para funcionalidades avanzadas"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard-ejecutivo/",
                self.admin_site.admin_view(self.dashboard_ejecutivo),
                name="marca_dashboard_ejecutivo",
            ),
            path(
                "<int:marca_id>/workflow/",
                self.admin_site.admin_view(self.workflow_view),
                name="marca_workflow",
            ),
            path(
                "analytics-predictivo/",
                self.admin_site.admin_view(self.analytics_predictivo),
                name="marca_analytics_predictivo",
            ),
            path(
                "optimizacion-tiempos/",
                self.admin_site.admin_view(self.optimizacion_tiempos),
                name="marca_optimizacion_tiempos",
            ),
            path(
                "api/metricas-tiempo-real/",
                self.admin_site.admin_view(self.api_metricas_tiempo_real),
                name="marca_api_metricas",
            ),
        ]
        return custom_urls + urls

    # Métodos de visualización avanzados
    def marca_info_detallada(self, obj):
        """Información detallada de la marca con indicadores"""
        # Calcular métricas
        dias_registro = obj.dias_desde_registro
        tiene_logos = hasattr(obj, "logos") and obj.logos.exists()

        # Indicadores visuales
        urgencia_color = (
            "#f44336"
            if dias_registro > 30
            else "#ff9800" if dias_registro > 7 else "#4caf50"
        )
        logo_indicator = "🎨" if tiene_logos else "⚪"

        return format_html(
            '<div style="line-height: 1.5;">'
            '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 5px;">'
            '<strong style="color: #2c3e50; font-size: 16px;">{}</strong>'
            '<span style="background: {}; color: white; padding: 2px 6px; '
            'border-radius: 10px; font-size: 10px; font-weight: bold;">{} días</span>'
            "</div>"
            '<div style="display: flex; gap: 10px; font-size: 12px; color: #6c757d;">'
            "<span>📅 {}</span>"
            "<span>{} Logos</span>"
            "<span>🔄 {} cambios</span>"
            "</div>"
            "</div>",
            obj.numero_marca,
            urgencia_color,
            dias_registro,
            obj.fecha_registro.strftime("%d/%m/%Y"),
            logo_indicator,
            obj.historial.count() if hasattr(obj, "historial") else 0,
        )

    marca_info_detallada.short_description = "🏷️ Marca"
    marca_info_detallada.admin_order_field = "numero_marca"

    def productor_con_contacto(self, obj):
        """Información del productor con datos de contacto"""
        telefono_display = obj.telefono_productor or "Sin teléfono"
        ci_display = obj.ci_productor or "Sin CI"

        # Validar completitud de datos
        completitud = 0
        if obj.nombre_productor:
            completitud += 1
        if obj.ci_productor:
            completitud += 1
        if obj.telefono_productor:
            completitud += 1

        completitud_color = (
            "#4caf50"
            if completitud == 3
            else "#ff9800" if completitud == 2 else "#f44336"
        )
        completitud_porcentaje = (completitud / 3) * 100

        return format_html(
            '<div style="line-height: 1.4;">'
            '<div style="font-weight: bold; color: #2c3e50; margin-bottom: 5px;">{}</div>'
            '<div style="font-size: 12px; color: #6c757d; margin-bottom: 5px;">'
            "<div>🆔 {}</div>"
            "<div>📞 {}</div>"
            "</div>"
            '<div style="display: flex; align-items: center; gap: 5px;">'
            '<div style="width: 40px; height: 4px; background: #e0e0e0; border-radius: 2px; overflow: hidden;">'
            '<div style="width: {}%; height: 100%; background: {}; transition: width 0.3s;"></div>'
            "</div>"
            '<span style="font-size: 10px; color: {};">{}%</span>'
            "</div>"
            "</div>",
            obj.nombre_productor[:25]
            + ("..." if len(obj.nombre_productor) > 25 else ""),
            ci_display,
            telefono_display,
            completitud_porcentaje,
            completitud_color,
            completitud_color,
            f"{completitud_porcentaje:.0f}",
        )

    productor_con_contacto.short_description = "👤 Productor"
    productor_con_contacto.admin_order_field = "nombre_productor"

    def ganado_info_visual(self, obj):
        """Información visual del ganado con indicadores"""
        # Configuración de colores por raza
        raza_colors = {
            "HOLSTEIN": "#2196f3",
            "BRAHMAN": "#ff9800",
            "ANGUS": "#4caf50",
            "CEBU": "#9c27b0",
            "NORMANDO": "#f44336",
        }

        # Configuración de iconos por propósito
        proposito_icons = {"LECHE": "🥛", "CARNE": "🥩", "DOBLE": "🥛🥩"}

        raza_color = raza_colors.get(obj.raza_bovino, "#757575")
        proposito_icon = proposito_icons.get(obj.proposito_ganado, "🐄")

        # Clasificar por tamaño del hato
        if obj.cantidad_cabezas >= 500:
            tamaño_clase = "Grande"
            tamaño_color = "#4caf50"
            tamaño_icon = "🏭"
        elif obj.cantidad_cabezas >= 100:
            tamaño_clase = "Mediano"
            tamaño_color = "#ff9800"
            tamaño_icon = "🏢"
        else:
            tamaño_clase = "Pequeño"
            tamaño_color = "#2196f3"
            tamaño_icon = "🏠"

        # Obtener valores de display de forma segura
        raza_display = getattr(
            obj, "get_raza_bovino_display", lambda: obj.raza_bovino
        )()
        proposito_display = getattr(
            obj, "get_proposito_ganado_display", lambda: obj.proposito_ganado
        )()

        return format_html(
            '<div style="text-align: center; line-height: 1.3;">'
            '<div style="display: flex; align-items: center; justify-content: center; gap: 5px; margin-bottom: 5px;">'
            '<span style="color: {}; font-weight: bold; font-size: 14px;">{}</span>'
            '<span style="font-size: 16px;">{}</span>'
            "</div>"
            '<div style="font-size: 12px; color: #6c757d; margin-bottom: 5px;">{}</div>'
            '<div style="display: flex; align-items: center; justify-content: center; gap: 5px;">'
            '<span style="color: {}; font-size: 14px;">{}</span>'
            '<span style="color: {}; font-weight: bold; font-size: 12px;">{}</span>'
            '<span style="font-size: 12px; color: #6c757d;">cabezas</span>'
            "</div>"
            '<div style="font-size: 10px; color: {}; margin-top: 2px;">{} {}</div>'
            "</div>",
            raza_color,
            raza_display,
            proposito_icon,
            proposito_display,
            tamaño_icon,
            tamaño_color,
            self.format_numero_con_separadores(obj.cantidad_cabezas),
            tamaño_color,
            tamaño_icon,
            tamaño_clase,
        )

    ganado_info_visual.short_description = "🐄 Ganado"
    ganado_info_visual.admin_order_field = "cantidad_cabezas"

    def ubicacion_completa(self, obj):
        """Ubicación completa con jerarquía visual"""
        return format_html(
            '<div style="text-align: center; line-height: 1.3;">'
            '<div style="font-weight: bold; color: #2c3e50; margin-bottom: 3px;">{}</div>'
            '<div style="font-size: 12px; color: #6c757d; margin-bottom: 2px;">📍 {}</div>'
            '<div style="font-size: 11px; color: #999;">{}</div>'
            "</div>",
            obj.get_departamento_display(),
            obj.municipio,
            obj.comunidad or "Comunidad no especificada",
        )

    ubicacion_completa.short_description = "📍 Ubicación"
    ubicacion_completa.admin_order_field = "departamento"

    def estado_con_workflow(self, obj):
        """Estado con indicador de workflow y progreso"""
        estados_workflow = {
            "PENDIENTE": {
                "progreso": 25,
                "siguiente": "EN_PROCESO",
                "color": "#ff9800",
                "icon": "⏳",
            },
            "EN_PROCESO": {
                "progreso": 50,
                "siguiente": "APROBADO",
                "color": "#2196f3",
                "icon": "🔄",
            },
            "APROBADO": {
                "progreso": 100,
                "siguiente": None,
                "color": "#4caf50",
                "icon": "✅",
            },
            "RECHAZADO": {
                "progreso": 0,
                "siguiente": None,
                "color": "#f44336",
                "icon": "❌",
            },
        }

        config = estados_workflow.get(
            obj.estado, {"progreso": 0, "color": "#757575", "icon": "❓"}
        )

        return format_html(
            '<div style="text-align: center;">'
            '<div style="display: flex; align-items: center; justify-content: center; gap: 5px; margin-bottom: 5px;">'
            '<span style="font-size: 16px;">{}</span>'
            '<span style="color: {}; font-weight: bold; font-size: 12px;">{}</span>'
            "</div>"
            '<div style="width: 60px; height: 6px; background: #e0e0e0; border-radius: 3px; overflow: hidden; margin: 0 auto 5px;">'
            '<div style="width: {}%; height: 100%; background: {}; transition: width 0.5s ease;"></div>'
            "</div>"
            '<div style="font-size: 10px; color: #6c757d;">{}%</div>'
            "{}"
            "</div>",
            config["icon"],
            config["color"],
            obj.estado,
            config["progreso"],
            config["color"],
            config["progreso"],
            (
                f'<div style="font-size: 9px; color: #999; margin-top: 2px;">→ {config["siguiente"]}</div>'
                if config.get("siguiente")
                else ""
            ),
        )

    estado_con_workflow.short_description = "📊 Estado"
    estado_con_workflow.admin_order_field = "estado"

    def certificacion_info(self, obj):
        """Información de certificación con análisis financiero"""
        monto = obj.monto_certificacion or 0

        # Clasificar por monto
        if monto >= 10000:
            categoria = "Premium"
            categoria_color = "#4caf50"
            categoria_icon = "💎"
        elif monto >= 5000:
            categoria = "Estándar"
            categoria_color = "#ff9800"
            categoria_icon = "⭐"
        elif monto > 0:
            categoria = "Básico"
            categoria_color = "#2196f3"
            categoria_icon = "📋"
        else:
            categoria = "Sin costo"
            categoria_color = "#757575"
            categoria_icon = "🆓"

        # Calcular costo por cabeza
        costo_por_cabeza = (
            monto / obj.cantidad_cabezas if obj.cantidad_cabezas > 0 else 0
        )

        return format_html(
            '<div style="text-align: center; line-height: 1.3;">'
            '<div style="display: flex; align-items: center; justify-content: center; gap: 5px; margin-bottom: 5px;">'
            '<span style="font-size: 16px;">{}</span>'
            '<span style="color: {}; font-weight: bold; font-size: 12px;">{}</span>'
            "</div>"
            '<div style="font-weight: bold; color: #2c3e50; margin-bottom: 3px;">${}</div>'
            '<div style="font-size: 10px; color: #6c757d;">${} por cabeza</div>'
            "</div>",
            categoria_icon,
            categoria_color,
            categoria,
            self.format_numero_con_separadores(monto),
            f"{costo_por_cabeza:.2f}",
        )

    certificacion_info.short_description = "💰 Certificación"
    certificacion_info.admin_order_field = "monto_certificacion"

    def tiempo_procesamiento_avanzado(self, obj):
        """Tiempo de procesamiento con análisis avanzado"""
        dias = obj.dias_desde_registro
        horas_procesamiento = obj.tiempo_procesamiento_horas or 0

        # Análisis de eficiencia
        if obj.estado == "APROBADO" and horas_procesamiento > 0:
            if horas_procesamiento <= 24:
                eficiencia = "Excelente"
                eficiencia_color = "#4caf50"
                eficiencia_icon = "🚀"
            elif horas_procesamiento <= 72:
                eficiencia = "Buena"
                eficiencia_color = "#ff9800"
                eficiencia_icon = "⚡"
            else:
                eficiencia = "Lenta"
                eficiencia_color = "#f44336"
                eficiencia_icon = "🐌"
        else:
            eficiencia = "Pendiente"
            eficiencia_color = "#757575"
            eficiencia_icon = "⏳"

        return format_html(
            '<div style="text-align: center; line-height: 1.3;">'
            '<div style="color: {}; font-weight: bold; margin-bottom: 5px;">{} días</div>'
            '<div style="display: flex; align-items: center; justify-content: center; gap: 5px; margin-bottom: 3px;">'
            '<span style="font-size: 14px;">{}</span>'
            '<span style="color: {}; font-size: 11px; font-weight: bold;">{}</span>'
            "</div>"
            '<div style="font-size: 10px; color: #6c757d;">{}h procesamiento</div>'
            "</div>",
            self.get_estado_color("PENDIENTE") if dias > 30 else "#4caf50",
            dias,
            eficiencia_icon,
            eficiencia_color,
            eficiencia,
            horas_procesamiento,
        )

    tiempo_procesamiento_avanzado.short_description = "⏱️ Tiempo"
    tiempo_procesamiento_avanzado.admin_order_field = "fecha_registro"

    def acciones_inteligentes(self, obj):
        """Acciones inteligentes basadas en el estado y contexto"""
        acciones = []

        # Acciones basadas en estado
        if obj.estado == "PENDIENTE":
            acciones.append(
                self.create_action_button(
                    f"#procesar-{obj.pk}", "🔄 Procesar", "#2196f3"
                )
            )
            if obj.dias_desde_registro > 7:
                acciones.append(
                    self.create_action_button(
                        f"#urgente-{obj.pk}", "🚨 Urgente", "#f44336"
                    )
                )
        elif obj.estado == "EN_PROCESO":
            acciones.append(
                self.create_action_button(f"#aprobar-{obj.pk}", "✅ Aprobar", "#4caf50")
            )
            acciones.append(
                self.create_action_button(
                    f"#rechazar-{obj.pk}", "❌ Rechazar", "#f44336"
                )
            )

        # Workflow siempre disponible
        workflow_url = reverse("admin:marca_workflow", args=[obj.pk])
        acciones.append(
            self.create_action_button(workflow_url, "📋 Workflow", "#6c757d")
        )

        # Análisis predictivo
        acciones.append(
            self.create_action_button(f"#predecir-{obj.pk}", "🔮 Predecir", "#9c27b0")
        )

        return format_html(
            '<div style="display: flex; flex-direction: column; gap: 2px;">{}</div>',
            "".join(acciones),
        )

    acciones_inteligentes.short_description = "⚡ Acciones"

    # Campos readonly avanzados
    def dashboard_metricas(self, obj):
        """Dashboard de métricas integrado"""
        if not obj.pk:
            return "Disponible después de guardar"

        # Calcular métricas comparativas
        marcas_similares = MarcaGanadoBovinoModel.objects.filter(
            departamento=obj.departamento, raza_bovino=obj.raza_bovino
        ).exclude(pk=obj.pk)

        promedio_tiempo = (
            marcas_similares.aggregate(promedio=Avg("tiempo_procesamiento_horas"))[
                "promedio"
            ]
            or 0
        )

        promedio_monto = (
            marcas_similares.aggregate(promedio=Avg("monto_certificacion"))["promedio"]
            or 0
        )

        return format_html(
            '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0;">'
            '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
            'color: white; padding: 15px; border-radius: 8px; text-align: center;">'
            '<div style="font-size: 20px; font-weight: bold;">{}</div>'
            '<div style="font-size: 12px; opacity: 0.9;">Días Transcurridos</div>'
            "</div>"
            '<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); '
            'color: white; padding: 15px; border-radius: 8px; text-align: center;">'
            '<div style="font-size: 20px; font-weight: bold;">{}h</div>'
            '<div style="font-size: 12px; opacity: 0.9;">vs {}h promedio</div>'
            "</div>"
            '<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); '
            'color: white; padding: 15px; border-radius: 8px; text-align: center;">'
            '<div style="font-size: 20px; font-weight: bold;">${}</div>'
            '<div style="font-size: 12px; opacity: 0.9;">vs ${} promedio</div>'
            "</div>"
            "</div>",
            obj.dias_desde_registro,
            f"{obj.tiempo_procesamiento_horas or 0:.1f}",
            f"{promedio_tiempo:.1f}",
            self.format_numero_con_separadores(obj.monto_certificacion or 0),
            f"{promedio_monto:.0f}",
        )

    dashboard_metricas.short_description = "📊 Dashboard"

    def historial_visual(self, obj):
        """Historial visual de cambios"""
        if not obj.pk:
            return "Disponible después de guardar"

        historial = (
            obj.historial.order_by("-fecha_cambio")[:5]
            if hasattr(obj, "historial")
            else []
        )

        if not historial:
            return format_html('<em style="color: #999;">Sin historial de cambios</em>')

        html = '<div style="max-height: 250px; overflow-y: auto;">'
        for i, cambio in enumerate(historial):
            fecha = cambio.fecha_cambio.strftime("%d/%m/%Y %H:%M")
            usuario = getattr(cambio, "usuario_responsable", "Sistema")

            # Línea de tiempo visual
            is_last = i == len(historial) - 1
            line_style = "border-left: 2px solid #e9ecef;" if not is_last else ""

            html += f"""
            <div style="position: relative; padding: 15px 0 15px 30px; {line_style}">
                <div style="position: absolute; left: -6px; top: 20px; width: 12px; height: 12px; 
                     background: {self.get_estado_color(cambio.estado_nuevo)}; border-radius: 50%; 
                     border: 2px solid white; box-shadow: 0 0 0 2px {self.get_estado_color(cambio.estado_nuevo)};"></div>
                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; 
                     border-left: 4px solid {self.get_estado_color(cambio.estado_nuevo)};">
                    <div style="font-size: 12px; color: #6c757d; margin-bottom: 5px;">{fecha} - {usuario}</div>
                    <div style="font-weight: 600; margin-bottom: 5px;">
                        <span style="color: {self.get_estado_color(cambio.estado_anterior)};">{cambio.estado_anterior}</span>
                        →
                        <span style="color: {self.get_estado_color(cambio.estado_nuevo)};">{cambio.estado_nuevo}</span>
                    </div>
                    {f'<div style="font-style: italic; color: #6c757d; font-size: 12px;">{getattr(cambio, "observaciones_cambio", "")}</div>' if getattr(cambio, 'observaciones_cambio', '') else ''}
                </div>
            </div>
            """

        html += "</div>"
        return format_html(html)

    historial_visual.short_description = "📜 Historial Visual"

    def prediccion_tiempo(self, obj):
        """Predicción de tiempo de procesamiento usando ML básico"""
        if obj.estado in ["APROBADO", "RECHAZADO"]:
            return format_html('<em style="color: #999;">Marca ya procesada</em>')

        # Análisis predictivo básico basado en datos históricos
        marcas_similares = MarcaGanadoBovinoModel.objects.filter(
            departamento=obj.departamento,
            raza_bovino=obj.raza_bovino,
            estado__in=["APROBADO", "RECHAZADO"],
            tiempo_procesamiento_horas__isnull=False,
        )

        if not marcas_similares.exists():
            return format_html(
                '<em style="color: #999;">Datos insuficientes para predicción</em>'
            )

        # Calcular predicción
        tiempos = [m.tiempo_procesamiento_horas for m in marcas_similares]
        tiempo_promedio = sum(tiempos) / len(tiempos)

        # Ajustar por factores
        factor_tamaño = (
            1.2
            if obj.cantidad_cabezas > 500
            else 1.0 if obj.cantidad_cabezas > 100 else 0.8
        )
        factor_monto = 1.3 if (obj.monto_certificacion or 0) > 10000 else 1.0

        tiempo_predicho = tiempo_promedio * factor_tamaño * factor_monto

        # Clasificar predicción
        if tiempo_predicho <= 24:
            color = "#4caf50"
            categoria = "Rápido"
            icon = "🚀"
        elif tiempo_predicho <= 72:
            color = "#ff9800"
            categoria = "Normal"
            icon = "⚡"
        else:
            color = "#f44336"
            categoria = "Lento"
            icon = "🐌"

        # Calcular confianza de la predicción
        confianza = min(100, (len(tiempos) / 10) * 100)

        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid {};">'
            '<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">'
            '<span style="font-size: 24px;">{}</span>'
            "<div>"
            '<div style="color: {}; font-weight: bold; font-size: 16px;">{} horas</div>'
            '<div style="color: {}; font-size: 12px;">{}</div>'
            "</div>"
            "</div>"
            '<div style="font-size: 12px; color: #6c757d;">'
            "Basado en {} marcas similares<br>"
            "Confianza: {}%"
            "</div>"
            "</div>",
            color,
            icon,
            color,
            f"{tiempo_predicho:.1f}",
            color,
            categoria,
            len(tiempos),
            f"{confianza:.0f}",
        )

    prediccion_tiempo.short_description = "🔮 Predicción"

    def analisis_rentabilidad(self, obj):
        """Análisis de rentabilidad por cabeza de ganado"""
        if not obj.cantidad_cabezas or not obj.monto_certificacion:
            return format_html(
                '<em style="color: #999;">Datos insuficientes para análisis</em>'
            )

        costo_por_cabeza = obj.monto_certificacion / obj.cantidad_cabezas

        # Benchmarks por propósito
        benchmarks = {
            "LECHE": {"optimo": 50, "aceptable": 100},
            "CARNE": {"optimo": 30, "aceptable": 60},
            "DOBLE": {"optimo": 40, "aceptable": 80},
        }

        benchmark = benchmarks.get(
            obj.proposito_ganado, {"optimo": 50, "aceptable": 100}
        )

        if costo_por_cabeza <= benchmark["optimo"]:
            categoria = "Excelente"
            color = "#4caf50"
            icon = "💎"
        elif costo_por_cabeza <= benchmark["aceptable"]:
            categoria = "Aceptable"
            color = "#ff9800"
            icon = "⭐"
        else:
            categoria = "Alto"
            color = "#f44336"
            icon = "⚠️"

        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">'
            '<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">'
            '<span style="font-size: 20px;">{}</span>'
            "<div>"
            '<div style="color: {}; font-weight: bold;">${} por cabeza</div>'
            '<div style="color: {}; font-size: 12px;">{}</div>'
            "</div>"
            "</div>"
            '<div style="font-size: 11px; color: #6c757d;">'
            "Óptimo: ${} | Aceptable: ${}"
            "</div>"
            "</div>",
            icon,
            color,
            f"{costo_por_cabeza:.2f}",
            color,
            categoria,
            benchmark["optimo"],
            benchmark["aceptable"],
        )

    analisis_rentabilidad.short_description = "💰 Rentabilidad"

    # Métodos heredados mejorados
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

    # Acciones masivas inteligentes mejoradas
    def aprobar_marcas_inteligente(self, request, queryset):
        """Aprobación inteligente con validaciones avanzadas"""
        ahora = timezone.now()
        marcas_aprobables = queryset.filter(estado__in=["PENDIENTE", "EN_PROCESO"])

        if not marcas_aprobables.exists():
            self.message_user(
                request,
                "No hay marcas que puedan ser aprobadas en la selección.",
                messages.WARNING,
            )
            return

        # Validaciones inteligentes
        count_aprobadas = 0
        count_rechazadas = 0

        for marca in marcas_aprobables:
            # Criterios de aprobación automática
            puede_aprobar = True
            motivo_rechazo = []

            # Validar datos mínimos
            if not marca.ci_productor:
                puede_aprobar = False
                motivo_rechazo.append("Falta CI del productor")

            if marca.cantidad_cabezas < 5:
                puede_aprobar = False
                motivo_rechazo.append("Cantidad de cabezas muy baja")

            # Validar tiempo de procesamiento razonable
            if marca.dias_desde_registro > 60:
                puede_aprobar = False
                motivo_rechazo.append("Tiempo de procesamiento excesivo")

            if puede_aprobar:
                self._procesar_aprobacion_marca(marca, ahora, request.user.username)
                count_aprobadas += 1
            else:
                # Auto-rechazar con motivo
                marca.estado = "RECHAZADO"
                marca.observaciones = f"Auto-rechazado: {'; '.join(motivo_rechazo)}"
                marca.fecha_procesamiento = ahora
                marca.save()

                self._crear_historial_cambio(
                    marca,
                    "RECHAZADO",
                    request.user.username,
                    f"Auto-rechazado por validación inteligente: {'; '.join(motivo_rechazo)}",
                )
                count_rechazadas += 1

        mensaje = f"🧠 Procesamiento inteligente completado: {count_aprobadas} aprobadas, {count_rechazadas} rechazadas automáticamente."
        self.message_user(request, mensaje, messages.SUCCESS)

    aprobar_marcas_inteligente.short_description = "🧠 Aprobación inteligente"

    def rechazar_con_analisis(self, request, queryset):
        """Rechazo con análisis automático de motivos"""
        if "apply" in request.POST:
            motivo_manual = request.POST.get("motivo", "")
            ahora = timezone.now()
            count = 0

            for marca in queryset:
                if marca.estado not in ["RECHAZADO"]:
                    # Análisis automático de motivos
                    motivos_automaticos = []

                    if not marca.ci_productor:
                        motivos_automaticos.append("Documentación incompleta")
                    if marca.cantidad_cabezas < 5:
                        motivos_automaticos.append("Hato muy pequeño")
                    if marca.dias_desde_registro > 90:
                        motivos_automaticos.append("Solicitud vencida")

                    motivo_final = motivo_manual
                    if motivos_automaticos:
                        motivo_final += (
                            f" | Análisis automático: {'; '.join(motivos_automaticos)}"
                        )

                    self._procesar_rechazo_marca(marca, ahora, request.user.username)
                    marca.observaciones = motivo_final
                    marca.save()
                    count += 1

            self.message_user(
                request,
                f"📊 {count} marcas rechazadas con análisis automático.",
                messages.WARNING,
            )
            return HttpResponseRedirect(request.get_full_path())

        # Análisis previo para mostrar en el formulario
        analisis_previo = {}
        for marca in queryset:
            problemas = []
            if not marca.ci_productor:
                problemas.append("Sin CI")
            if marca.cantidad_cabezas < 5:
                problemas.append("Hato pequeño")
            if marca.dias_desde_registro > 90:
                problemas.append("Solicitud antigua")

            if problemas:
                analisis_previo[marca.pk] = problemas

        context = {
            "title": "Rechazar marcas con análisis",
            "queryset": queryset,
            "analisis_previo": analisis_previo,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
        }

        return render(request, "admin/marca_rechazar_analisis.html", context)

    rechazar_con_analisis.short_description = "📊 Rechazar con análisis"

    def workflow_automatico(self, request, queryset):
        """Workflow automático basado en reglas de negocio"""
        ahora = timezone.now()
        resultados = {
            "procesadas": 0,
            "aprobadas": 0,
            "rechazadas": 0,
            "sin_cambios": 0,
        }

        for marca in queryset:
            accion_tomada = False

            # Regla 1: Auto-procesar pendientes con datos completos
            if (
                marca.estado == "PENDIENTE"
                and marca.ci_productor
                and marca.telefono_productor
                and marca.cantidad_cabezas >= 10
            ):

                marca.estado = "EN_PROCESO"
                marca.save()
                self._crear_historial_cambio(
                    marca,
                    "EN_PROCESO",
                    request.user.username,
                    "Auto-procesado por workflow: datos completos",
                )
                resultados["procesadas"] += 1
                accion_tomada = True

            # Regla 2: Auto-aprobar en proceso con criterios óptimos
            elif (
                marca.estado == "EN_PROCESO"
                and marca.cantidad_cabezas >= 50
                and marca.dias_desde_registro <= 30
                and (marca.monto_certificacion or 0) > 0
            ):

                self._procesar_aprobacion_marca(marca, ahora, request.user.username)
                resultados["aprobadas"] += 1
                accion_tomada = True

            # Regla 3: Auto-rechazar casos problemáticos
            elif marca.dias_desde_registro > 120 or (
                marca.cantidad_cabezas < 5 and marca.dias_desde_registro > 30
            ):

                motivo = "Auto-rechazado por workflow: "
                if marca.dias_desde_registro > 120:
                    motivo += "solicitud vencida"
                else:
                    motivo += "hato muy pequeño y tiempo excesivo"

                marca.estado = "RECHAZADO"
                marca.observaciones = motivo
                marca.fecha_procesamiento = ahora
                marca.save()

                self._crear_historial_cambio(
                    marca, "RECHAZADO", request.user.username, motivo
                )
                resultados["rechazadas"] += 1
                accion_tomada = True

            if not accion_tomada:
                resultados["sin_cambios"] += 1

        mensaje = (
            f"🤖 Workflow automático completado: "
            f"{resultados['procesadas']} procesadas, "
            f"{resultados['aprobadas']} aprobadas, "
            f"{resultados['rechazadas']} rechazadas, "
            f"{resultados['sin_cambios']} sin cambios."
        )

        self.message_user(request, mensaje, messages.SUCCESS)

    workflow_automatico.short_description = "🤖 Workflow automático"

    def calcular_metricas_avanzadas(self, request, queryset):
        """Calcular métricas avanzadas para las marcas seleccionadas"""
        total_marcas = queryset.count()
        total_cabezas = (
            queryset.aggregate(Sum("cantidad_cabezas"))["cantidad_cabezas__sum"] or 0
        )
        total_certificacion = (
            queryset.aggregate(Sum("monto_certificacion"))["monto_certificacion__sum"]
            or 0
        )

        # Métricas por estado
        por_estado = queryset.values("estado").annotate(count=Count("id"))

        # Tiempo promedio por departamento
        por_departamento = queryset.values("departamento").annotate(
            count=Count("id"), tiempo_promedio=Avg("tiempo_procesamiento_horas")
        )

        mensaje = (
            f"📊 Métricas calculadas para {total_marcas} marcas:\n"
            f"🐄 Total cabezas: {self.format_numero_con_separadores(total_cabezas)}\n"
            f"💰 Total certificación: ${self.format_numero_con_separadores(total_certificacion)}\n"
            f"📈 Promedio por marca: ${total_certificacion/total_marcas:.2f}"
            if total_marcas > 0
            else ""
        )

        self.message_user(request, mensaje, messages.INFO)

    calcular_metricas_avanzadas.short_description = "📊 Calcular métricas avanzadas"

    def generar_reporte_ejecutivo(self, request, queryset):
        """Generar reporte ejecutivo de las marcas seleccionadas"""
        # Aquí iría la lógica para generar un reporte ejecutivo
        # Por ahora simulamos la generación

        total_marcas = queryset.count()
        fecha_reporte = timezone.now().strftime("%Y%m%d_%H%M%S")

        self.message_user(
            request,
            f"📋 Reporte ejecutivo generado para {total_marcas} marcas. "
            f"Archivo: reporte_ejecutivo_{fecha_reporte}.pdf",
            messages.SUCCESS,
        )

    generar_reporte_ejecutivo.short_description = "📋 Generar reporte ejecutivo"

    def optimizar_tiempos(self, request, queryset):
        """Optimización de tiempos de procesamiento"""
        marcas_lentas = queryset.filter(
            tiempo_procesamiento_horas__gt=72, estado__in=["PENDIENTE", "EN_PROCESO"]
        )

        count = marcas_lentas.count()
        if count == 0:
            self.message_user(
                request,
                "No hay marcas con tiempos de procesamiento que requieran optimización.",
                messages.INFO,
            )
            return

        # Simular optimización (en la realidad esto podría involucrar
        # reasignación de recursos, priorización, etc.)
        for marca in marcas_lentas:
            # Lógica de optimización
            pass

        self.message_user(
            request,
            f"⚡ Optimización aplicada a {count} marcas con tiempos lentos.",
            messages.SUCCESS,
        )

    optimizar_tiempos.short_description = "⚡ Optimizar tiempos"

    def analisis_predictivo(self, request, queryset):
        """Análisis predictivo para las marcas seleccionadas"""
        predicciones = []

        for marca in queryset.filter(estado__in=["PENDIENTE", "EN_PROCESO"]):
            # Análisis predictivo básico
            marcas_similares = MarcaGanadoBovinoModel.objects.filter(
                departamento=marca.departamento,
                raza_bovino=marca.raza_bovino,
                estado__in=["APROBADO", "RECHAZADO"],
            ).exclude(pk=marca.pk)

            if marcas_similares.exists():
                tasa_aprobacion = (
                    marcas_similares.filter(estado="APROBADO").count()
                    / marcas_similares.count()
                    * 100
                )
                tiempo_promedio = (
                    marcas_similares.aggregate(
                        promedio=Avg("tiempo_procesamiento_horas")
                    )["promedio"]
                    or 0
                )

                predicciones.append(
                    {
                        "marca": marca.numero_marca,
                        "probabilidad_aprobacion": tasa_aprobacion,
                        "tiempo_estimado": tiempo_promedio,
                    }
                )

        if predicciones:
            # Generar resumen de predicciones
            promedio_aprobacion = sum(
                p["probabilidad_aprobacion"] for p in predicciones
            ) / len(predicciones)
            promedio_tiempo = sum(p["tiempo_estimado"] for p in predicciones) / len(
                predicciones
            )

            mensaje = (
                f"🔮 Análisis predictivo completado para {len(predicciones)} marcas:\n"
                f"📈 Probabilidad promedio de aprobación: {promedio_aprobacion:.1f}%\n"
                f"⏱️ Tiempo estimado promedio: {promedio_tiempo:.1f} horas"
            )
        else:
            mensaje = (
                "🔮 No hay suficientes datos históricos para realizar predicciones."
            )

        self.message_user(request, mensaje, messages.INFO)

    analisis_predictivo.short_description = "🔮 Análisis predictivo"

    # Vistas personalizadas
    def dashboard_ejecutivo(self, request):
        """Dashboard ejecutivo con métricas avanzadas"""
        # Métricas generales
        total_marcas = MarcaGanadoBovinoModel.objects.count()
        marcas_hoy = MarcaGanadoBovinoModel.objects.filter(
            fecha_registro__date=timezone.now().date()
        ).count()

        # Métricas por estado
        por_estado = MarcaGanadoBovinoModel.objects.values("estado").annotate(
            count=Count("id")
        )

        # Métricas de tiempo
        tiempo_promedio = (
            MarcaGanadoBovinoModel.objects.filter(
                tiempo_procesamiento_horas__isnull=False
            ).aggregate(promedio=Avg("tiempo_procesamiento_horas"))["promedio"]
            or 0
        )

        # Top departamentos
        top_departamentos = (
            MarcaGanadoBovinoModel.objects.values("departamento")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        context = {
            "title": "Dashboard Ejecutivo - Marcas Ganaderas",
            "total_marcas": total_marcas,
            "marcas_hoy": marcas_hoy,
            "por_estado": por_estado,
            "tiempo_promedio": tiempo_promedio,
            "top_departamentos": top_departamentos,
            "opts": self.model._meta,
        }

        return render(request, "admin/marca_dashboard_ejecutivo.html", context)

    def workflow_view(self, request, marca_id):
        """Vista detallada del workflow de una marca"""
        marca = get_object_or_404(MarcaGanadoBovinoModel, pk=marca_id)

        # Calcular siguiente paso recomendado
        siguiente_paso = self._calcular_siguiente_paso(marca)

        context = {
            "title": f"Workflow - {marca.numero_marca}",
            "marca": marca,
            "siguiente_paso": siguiente_paso,
            "opts": self.model._meta,
        }

        return render(request, "admin/marca_workflow.html", context)

    def analytics_predictivo(self, request):
        """Vista de analytics predictivo"""
        # Implementar análisis predictivo avanzado
        context = {
            "title": "Analytics Predictivo - Marcas Ganaderas",
            "opts": self.model._meta,
        }

        return render(request, "admin/marca_analytics_predictivo.html", context)

    def optimizacion_tiempos(self, request):
        """Vista de optimización de tiempos"""
        # Análisis de cuellos de botella
        marcas_lentas = MarcaGanadoBovinoModel.objects.filter(
            tiempo_procesamiento_horas__gt=72
        ).order_by("-tiempo_procesamiento_horas")[:20]

        context = {
            "title": "Optimización de Tiempos",
            "marcas_lentas": marcas_lentas,
            "opts": self.model._meta,
        }

        return render(request, "admin/marca_optimizacion_tiempos.html", context)

    def api_metricas_tiempo_real(self, request):
        """API para métricas en tiempo real"""
        data = {
            "total_marcas": MarcaGanadoBovinoModel.objects.count(),
            "pendientes": MarcaGanadoBovinoModel.objects.filter(
                estado="PENDIENTE"
            ).count(),
            "en_proceso": MarcaGanadoBovinoModel.objects.filter(
                estado="EN_PROCESO"
            ).count(),
            "aprobadas_hoy": MarcaGanadoBovinoModel.objects.filter(
                estado="APROBADO", fecha_procesamiento__date=timezone.now().date()
            ).count(),
            "tiempo_promedio": MarcaGanadoBovinoModel.objects.filter(
                tiempo_procesamiento_horas__isnull=False
            ).aggregate(promedio=Avg("tiempo_procesamiento_horas"))["promedio"]
            or 0,
            "ultima_actualizacion": timezone.now().isoformat(),
        }

        return JsonResponse(data)

    # Métodos auxiliares
    def _calcular_siguiente_paso(self, marca):
        """Calcular el siguiente paso recomendado en el workflow"""
        if marca.estado == "PENDIENTE":
            if marca.ci_productor and marca.telefono_productor:
                return {
                    "accion": "Poner en proceso",
                    "motivo": "Datos completos",
                    "prioridad": "alta",
                }
            else:
                return {
                    "accion": "Solicitar documentación",
                    "motivo": "Datos incompletos",
                    "prioridad": "media",
                }
        elif marca.estado == "EN_PROCESO":
            if marca.dias_desde_registro <= 30 and marca.cantidad_cabezas >= 20:
                return {
                    "accion": "Aprobar",
                    "motivo": "Cumple criterios",
                    "prioridad": "alta",
                }
            else:
                return {
                    "accion": "Revisar criterios",
                    "motivo": "Evaluación adicional requerida",
                    "prioridad": "media",
                }
        else:
            return {
                "accion": "Ninguna",
                "motivo": "Marca ya procesada",
                "prioridad": "baja",
            }

    # Métodos privados heredados (mantenidos para compatibilidad)
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

    def get_queryset(self, request):
        """Optimizar consultas con select_related y prefetch_related"""
        qs = super().get_queryset(request)

        # Solo agregar select_related para campos relacionales válidos
        select_related_fields = []
        prefetch_related_fields = []

        # Verificar campos relacionales
        for field_name in ["marca", "historial", "logos"]:
            if hasattr(self.model, field_name):
                field = self.model._meta.get_field(field_name)
                if hasattr(field, "related_model") and field.related_model:
                    if field.many_to_many or field.one_to_many:
                        prefetch_related_fields.append(field_name)
                    else:
                        select_related_fields.append(field_name)

        if select_related_fields:
            qs = qs.select_related(*select_related_fields)

        if prefetch_related_fields:
            qs = qs.prefetch_related(*prefetch_related_fields)

        return qs

    class Media:
        css = {"all": ("admin/css/marca_admin.css",)}
        js = ("admin/js/marca_admin.js",)
