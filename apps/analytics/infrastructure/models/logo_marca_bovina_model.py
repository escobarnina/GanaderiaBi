# apps/analytics/infrastructure/models/logo_marca_bovina_model.py
"""
Modelo Django para logos de marcas bovinas - Single Responsibility
Responsabilidad única: Gestionar datos de logos generados por IA
"""

from django.db import models
from django.core.validators import MinValueValidator
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
