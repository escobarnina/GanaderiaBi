# apps/analytics/infrastructure/models/logo_marca_bovina_model.py
"""
Modelo Django para logos de marcas bovinas - Single Responsibility
Responsabilidad única: Gestionar datos de logos generados por IA
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
from .marca_ganado_bovino_model import MarcaGanadoBovinoModel
from apps.analytics.domain.enums import ModeloIA, CalidadLogo


class LogoMarcaBovinaModel(models.Model):
    """Modelo Django para logos de marcas bovinas - Nueva Arquitectura"""

    marca = models.ForeignKey(
        MarcaGanadoBovinoModel, on_delete=models.CASCADE, related_name="logos"
    )
    url_logo = models.URLField(help_text="URL donde se almacena el logo generado")
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    exito = models.BooleanField(
        default=True, help_text="Indica si la generación fue exitosa"
    )
    tiempo_generacion_segundos = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Tiempo que tomó generar el logo en segundos",
    )
    modelo_ia_usado = models.CharField(
        max_length=100,
        choices=[(choice.value, choice.value) for choice in ModeloIA],
        help_text="Modelo de IA utilizado para generar el logo",
    )
    prompt_usado = models.TextField(
        blank=True, null=True, help_text="Prompt utilizado para generar el logo"
    )
    calidad_logo = models.CharField(
        max_length=20,
        choices=[(choice.value, choice.value) for choice in CalidadLogo],
        default=CalidadLogo.MEDIA.value,
        help_text="Calidad percibida del logo generado",
    )

    class Meta:
        db_table = "logo_marca_bovina"
        verbose_name = "Logo de Marca Bovina"
        verbose_name_plural = "Logos de Marcas Bovinas"
        ordering = ["-fecha_generacion"]

    def __str__(self):
        return f"Logo {self.marca.numero_marca} - {self.modelo_ia_usado}"

    def save(self, *args, **kwargs):
        """Sobrescribir save para registrar cambios en el historial"""
        is_new = self.pk is None
        if not is_new:
            # Obtener el objeto original de la base de datos
            try:
                original = LogoMarcaBovinaModel.objects.get(pk=self.pk)
                # Comparar campos importantes
                changed_fields = []
                if original.url_logo != self.url_logo:
                    changed_fields.append(
                        f"URL del logo: {original.url_logo} → {self.url_logo}"
                    )
                if original.exito != self.exito:
                    changed_fields.append(f"Éxito: {original.exito} → {self.exito}")
                if original.modelo_ia_usado != self.modelo_ia_usado:
                    changed_fields.append(
                        f"Modelo IA: {original.modelo_ia_usado} → {self.modelo_ia_usado}"
                    )
                if original.calidad_logo != self.calidad_logo:
                    changed_fields.append(
                        f"Calidad: {original.calidad_logo} → {self.calidad_logo}"
                    )
                if original.prompt_usado != self.prompt_usado:
                    changed_fields.append(f"Prompt actualizado")
                if (
                    original.tiempo_generacion_segundos
                    != self.tiempo_generacion_segundos
                ):
                    changed_fields.append(
                        f"Tiempo: {original.tiempo_generacion_segundos}s → {self.tiempo_generacion_segundos}s"
                    )

                # Registrar cambios en el historial
                if changed_fields:
                    self._log_change(changed_fields)
            except LogoMarcaBovinaModel.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Registrar creación
        if is_new:
            self._log_creation()

    def delete(self, *args, **kwargs):
        """Sobrescribir delete para registrar eliminación en el historial"""
        self._log_deletion()
        super().delete(*args, **kwargs)

    def _log_creation(self):
        """Registrar creación en el historial"""
        LogEntry.objects.log_action(
            user_id=3,  # Usuario existente (melina)
            content_type_id=ContentType.objects.get_for_model(self).pk,
            object_id=self.pk,
            object_repr=str(self),
            action_flag=ADDITION,
            change_message="Logo creado automáticamente",
        )

    def _log_change(self, changed_fields):
        """Registrar cambios en el historial"""
        change_message = "; ".join(changed_fields)
        LogEntry.objects.log_action(
            user_id=3,  # Usuario existente (melina)
            content_type_id=ContentType.objects.get_for_model(self).pk,
            object_id=self.pk,
            object_repr=str(self),
            action_flag=CHANGE,
            change_message=change_message,
        )

    def _log_deletion(self):
        """Registrar eliminación en el historial"""
        LogEntry.objects.log_action(
            user_id=3,  # Usuario existente (melina)
            content_type_id=ContentType.objects.get_for_model(self).pk,
            object_id=self.pk,
            object_repr=str(self),
            action_flag=DELETION,
            change_message="Logo eliminado",
        )
