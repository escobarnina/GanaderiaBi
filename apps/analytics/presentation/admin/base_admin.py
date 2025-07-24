"""
Admin base para el sistema de analytics siguiendo Clean Architecture.

Responsabilidades:
- Proporcionar funcionalidades comunes para todos los admins
- Mantener consistencia en la interfaz administrativa
- Implementar utilidades compartidas
- Gestionar estilos y comportamientos base
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import timedelta
import json


class BaseAnalyticsAdmin(admin.ModelAdmin):
    """
    Admin base para todos los modelos de analytics.

    Proporciona funcionalidades comunes y mantiene consistencia
    en toda la interfaz administrativa.
    """

    # Colores para estados (Single Responsibility Principle)
    ESTADO_COLORS = {
        "PENDIENTE": "#ffc107",
        "EN_PROCESO": "#17a2b8",
        "APROBADO": "#28a745",
        "RECHAZADO": "#dc3545",
        "OBSERVADO": "#fd7e14",
    }

    # Iconos para estados
    ESTADO_ICONS = {
        "PENDIENTE": "⏳",
        "EN_PROCESO": "🔄",
        "APROBADO": "✅",
        "RECHAZADO": "❌",
        "OBSERVADO": "👀",
    }

    # Configuración base común
    save_on_top = True
    list_per_page = 25
    show_full_result_count = False

    # Estilos base
    class Media:
        css = {
            "all": (
                "admin/css/analytics_admin.css",
                "admin/css/custom_admin.css",
            )
        }
        js = (
            "admin/js/analytics_admin.js",
            "admin/js/chart-component.js",
        )

    def get_list_display_links(self, request, list_display):
        """Personalizar enlaces en list_display"""
        if list_display and len(list_display) > 0:
            return [list_display[0]]
        return super().get_list_display_links(request, list_display)

    def get_search_results(self, request, queryset, search_term):
        """Mejorar búsqueda con funcionalidades avanzadas"""
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )

        # Agregar lógica de búsqueda personalizada si es necesario
        return queryset, may_have_duplicates

    def get_estado_color(self, estado):
        """Obtiene color para un estado específico"""
        return self.ESTADO_COLORS.get(estado, "#6c757d")

    def get_estado_icon(self, estado):
        """Obtiene el icono para un estado específico"""
        return self.ESTADO_ICONS.get(estado, "●")

    def format_estado_with_color(self, obj, estado_field="estado"):
        """Formatea estado con color e icono"""
        estado = getattr(obj, estado_field)
        color = self.get_estado_color(estado)
        icon = self.get_estado_icon(estado)

        display_value = (
            obj.get_estado_display() if hasattr(obj, "get_estado_display") else estado
        )

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            display_value,
        )

    def format_tiempo_segundos(self, segundos):
        """Formatea tiempo en segundos a formato legible"""
        if segundos is None:
            return "N/A"

        if segundos < 60:
            return f"{segundos:.1f}s"
        elif segundos < 3600:
            minutos = segundos / 60
            return f"{minutos:.1f}min"
        else:
            horas = segundos / 3600
            return f"{horas:.1f}h"

    def format_tiempo_duracion(self, duracion):
        """Formatea duración de tiempo (timedelta)"""
        if duracion is None:
            return "N/A"

        if isinstance(duracion, timedelta):
            total_seconds = int(duracion.total_seconds())
            return self.format_tiempo_segundos(total_seconds)
        return str(duracion)

    def format_dias_con_color(self, dias):
        """Formatea días con color según urgencia"""
        if dias is None:
            return format_html(
                '<span style="color: #999; font-style: italic;">N/A</span>'
            )

        if dias <= 7:
            color = "#28a745"  # Verde
        elif dias <= 30:
            color = "#ffc107"  # Amarillo
        else:
            color = "#dc3545"  # Rojo

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} días</span>', color, dias
        )

    def format_porcentaje_con_color(self, porcentaje, umbral_alto=80, umbral_medio=60):
        """Formatea porcentaje con color según umbrales"""
        if porcentaje is None:
            return format_html(
                '<span style="color: #999; font-style: italic;">N/A</span>'
            )

        try:
            porcentaje_float = float(porcentaje)
        except (ValueError, TypeError):
            return format_html(
                '<span style="color: #999; font-style: italic;">N/A</span>'
            )

        if porcentaje_float >= umbral_alto:
            color = "#28a745"  # Verde
            icon = "📈"
        elif porcentaje_float >= umbral_medio:
            color = "#ffc107"  # Amarillo
            icon = "📊"
        else:
            color = "#dc3545"  # Rojo
            icon = "📉"

        # Formatear el porcentaje antes de pasarlo a format_html
        porcentaje_formateado = f"{porcentaje_float:.1f}%"

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            porcentaje_formateado,
        )

    def format_numero_con_separadores(self, numero):
        """Formatea números con separadores de miles"""
        try:
            return f"{numero:,}".replace(",", ".")
        except (ValueError, TypeError):
            return str(numero)

    def format_tamaño_archivo(self, bytes_size):
        """Formatea tamaño de archivo en formato legible"""
        if bytes_size is None:
            return "N/A"

        if bytes_size < 1024:
            return f"{bytes_size} B"
        elif bytes_size < 1024 * 1024:
            return f"{bytes_size / 1024:.1f} KB"
        elif bytes_size < 1024 * 1024 * 1024:
            return f"{bytes_size / (1024 * 1024):.1f} MB"
        else:
            return f"{bytes_size / (1024 * 1024 * 1024):.1f} GB"

    def create_action_button(self, url, text, color="#007bff"):
        """Crea un botón de acción personalizado"""
        return mark_safe(
            f'<a href="{url}" style="background: {color}; color: white; padding: 4px 8px; '
            f"border-radius: 4px; text-decoration: none; font-size: 11px; "
            f'display: inline-block; margin: 1px;">{text}</a>'
        )

    def show_json_preview(self, json_data, max_items=5):
        """Muestra preview de datos JSON"""
        if not json_data:
            return mark_safe('<em style="color: #999;">Sin datos</em>')

        try:
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data

            # Limitar elementos mostrados
            if isinstance(data, dict):
                limited_data = dict(list(data.items())[:max_items])
                if len(data) > max_items:
                    limited_data["..."] = f"y {len(data) - max_items} elementos más"
            elif isinstance(data, list):
                limited_data = data[:max_items]
                if len(data) > max_items:
                    limited_data.append(f"... y {len(data) - max_items} elementos más")
            else:
                limited_data = data

            json_str = json.dumps(limited_data, indent=2, ensure_ascii=False)

            return mark_safe(
                f'<pre style="background: #f8f9fa; padding: 10px; border-radius: 4px; '
                f'font-size: 12px; max-height: 200px; overflow-y: auto;">{json_str}</pre>'
            )
        except Exception as e:
            return mark_safe(f'<em style="color: #dc3545;">Error: {str(e)}</em>')

    def export_to_json(self, request, queryset):
        """Acción para exportar a JSON"""
        import json
        from django.http import HttpResponse

        data = []
        for obj in queryset:
            # Serializar objeto básico
            item = {
                "id": obj.pk,
                "modelo": obj._meta.model_name,
            }

            # Agregar campos específicos según el modelo
            for field in obj._meta.fields:
                field_name = field.name
                field_value = getattr(obj, field_name, None)

                # Manejar diferentes tipos de campos
                if hasattr(field_value, "isoformat"):  # DateTime
                    item[field_name] = field_value.isoformat()
                elif hasattr(field_value, "__str__"):
                    item[field_name] = str(field_value)
                else:
                    item[field_name] = field_value

            data.append(item)

        response = HttpResponse(
            json.dumps(data, indent=2, ensure_ascii=False),
            content_type="application/json",
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{queryset.model._meta.model_name}_export.json"'
        )

        self.message_user(
            request, f"Se exportaron {len(data)} registros a JSON exitosamente."
        )

        return response

    export_to_json.short_description = "📤 Exportar seleccionados a JSON"

    def get_readonly_fields(self, request, obj=None):
        """Personalizar campos readonly según contexto"""
        readonly_fields = list(super().get_readonly_fields(request, obj))

        # Agregar campos de auditoría como readonly
        audit_fields = ["created_at", "updated_at", "created_by", "updated_by"]
        for field in audit_fields:
            if hasattr(self.model, field) and field not in readonly_fields:
                readonly_fields.append(field)

        return readonly_fields

    def save_model(self, request, obj, form, change):
        """Personalizar guardado con auditoría"""
        if not change:  # Nuevo objeto
            if hasattr(obj, "created_by"):
                obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Optimizar queryset base"""
        qs = super().get_queryset(request)

        # Agregar select_related solo para campos relacionales válidos
        select_related_fields = []

        # Verificar campos relacionales comunes
        for field_name in ["created_by", "updated_by", "user", "owner"]:
            if hasattr(self.model, field_name):
                field = self.model._meta.get_field(field_name)
                if hasattr(field, "related_model") and field.related_model:
                    select_related_fields.append(field_name)

        if select_related_fields:
            qs = qs.select_related(*select_related_fields)

        return qs

    def changelist_view(self, request, extra_context=None):
        """Personalizar vista de lista con contexto adicional"""
        extra_context = extra_context or {}

        # Agregar estadísticas básicas
        total_count = self.get_queryset(request).count()
        extra_context["total_count"] = total_count

        # Agregar información de última actualización
        if hasattr(self.model, "updated_at"):
            try:
                last_updated = (
                    self.get_queryset(request).latest("updated_at").updated_at
                )
                extra_context["last_updated"] = last_updated
            except self.model.DoesNotExist:
                extra_context["last_updated"] = None

        return super().changelist_view(request, extra_context)

    def response_change(self, request, obj):
        """Personalizar respuesta después de cambios"""
        response = super().response_change(request, obj)

        # Agregar mensaje personalizado si es necesario
        if "_continue" not in request.POST and "_addanother" not in request.POST:
            self.message_user(
                request,
                f"El {obj._meta.verbose_name} '{obj}' fue actualizado exitosamente.",
            )

        return response

    def get_form(self, request, obj=None, **kwargs):
        """Personalizar formulario"""
        form = super().get_form(request, obj, **kwargs)

        # Personalizar widgets si es necesario
        for field_name, field in form.base_fields.items():
            if hasattr(field.widget, "attrs"):
                field.widget.attrs.update({"class": "form-control"})

        return form

    # Métodos para generar HTML común
    def generate_status_badge(self, status, text=None):
        """Genera badge de estado"""
        text = text or status
        color = self.get_estado_color(status)

        return format_html(
            '<span class="badge" style="background-color: {}; color: white; '
            'padding: 4px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            color,
            text,
        )

    def generate_progress_bar(self, percentage, color="#007bff"):
        """Genera barra de progreso"""
        return format_html(
            '<div style="width: 100px; height: 20px; background-color: #e9ecef; '
            'border-radius: 10px; overflow: hidden;">'
            '<div style="width: {}%; height: 100%; background-color: {}; '
            'transition: width 0.3s ease;"></div>'
            "</div>",
            percentage,
            color,
        )

    def generate_metric_card(self, title, value, icon="📊", color="#007bff"):
        """Genera tarjeta de métrica"""
        return format_html(
            '<div style="border: 1px solid #dee2e6; border-radius: 8px; '
            'padding: 15px; margin: 5px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
            '<div style="display: flex; align-items: center; margin-bottom: 10px;">'
            '<span style="font-size: 24px; margin-right: 10px;">{}</span>'
            '<h4 style="margin: 0; color: {};">{}</h4>'
            "</div>"
            '<div style="font-size: 24px; font-weight: bold; color: {};">{}</div>'
            "</div>",
            icon,
            color,
            title,
            color,
            value,
        )

    def generate_info_table(self, data_dict):
        """Genera tabla de información"""
        rows = []
        for key, value in data_dict.items():
            rows.append(
                f'<tr><td style="font-weight: bold; padding: 8px;">{key}:</td>'
                f'<td style="padding: 8px;">{value}</td></tr>'
            )

        return format_html(
            '<table style="width: 100%; border-collapse: collapse; '
            'border: 1px solid #dee2e6; border-radius: 4px;">'
            "<tbody>{}</tbody>"
            "</table>",
            "".join(rows),
        )

    # Validaciones comunes
    def validate_date_range(self, start_date, end_date):
        """Valida rango de fechas"""
        if start_date and end_date:
            if start_date > end_date:
                return (
                    False,
                    "La fecha de inicio no puede ser mayor que la fecha de fin",
                )

            # Validar que no sea muy antiguo (más de 5 años)
            five_years_ago = timezone.now().date() - timedelta(days=5 * 365)
            if start_date < five_years_ago:
                return False, "La fecha de inicio no puede ser anterior a 5 años"

        return True, ""

    def validate_positive_number(self, value, field_name="campo"):
        """Valida que un número sea positivo"""
        if value is not None and value < 0:
            return False, f"El {field_name} debe ser un número positivo"
        return True, ""

    # Métodos de análisis común
    def calculate_percentage_change(self, current, previous):
        """Calcula cambio porcentual"""
        if previous == 0:
            return 100 if current > 0 else 0
        return ((current - previous) / previous) * 100

    def get_trend_indicator(self, percentage_change):
        """Obtiene indicador de tendencia"""
        if percentage_change > 5:
            return {"icon": "📈", "color": "#28a745", "text": "Creciendo"}
        elif percentage_change < -5:
            return {"icon": "📉", "color": "#dc3545", "text": "Decreciendo"}
        else:
            return {"icon": "➡️", "color": "#6c757d", "text": "Estable"}

    def format_currency(self, amount, currency="Bs."):
        """Formatea moneda"""
        try:
            return f"{currency} {amount:,.2f}".replace(",", ".")
        except (ValueError, TypeError):
            return f"{currency} 0.00"

    def truncate_text(self, text, max_length=50):
        """Trunca texto con elipsis"""
        if not text:
            return ""
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    # Métodos para manejo de errores
    def handle_admin_error(self, request, error_message, error_type="error"):
        """Maneja errores en admin de forma consistente"""
        from django.contrib import messages

        if error_type == "warning":
            messages.warning(request, error_message)
        elif error_type == "info":
            messages.info(request, error_message)
        else:
            messages.error(request, error_message)

    def safe_execute(
        self, func, default_value=None, error_message="Error en operación"
    ):
        """Ejecuta función de forma segura"""
        try:
            return func()
        except Exception as e:
            # Log del error si es necesario
            print(f"Error en {func.__name__}: {str(e)}")
            return default_value

    def has_add_permission(self, request):
        """Permisos de creación - sobrescribir en subclases"""
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        """Permisos de modificación - sobrescribir en subclases"""
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        """Permisos de eliminación - sobrescribir en subclases"""
        return request.user.is_superuser

    def get_model_stats(self):
        """Obtiene estadísticas básicas del modelo"""
        model = self.model
        return {
            "total": model.objects.count(),
            "created_today": (
                model.objects.filter(fecha_registro__date=timezone.now().date()).count()
                if hasattr(model, "fecha_registro")
                else 0
            ),
        }
