# apps/analytics/infrastructure/models/marca_ganado_bovino_model.py
"""
Modelo Django para marca de ganado bovino - Single Responsibility
Responsabilidad única: Gestionar datos de marcas bovinas en la base de datos
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from apps.analytics.domain.enums import (
    EstadoMarca,
    RazaBovino,
    PropositoGanado,
    Departamento,
)


class MarcaGanadoBovinoModel(models.Model):
    """Modelo Django para marca de ganado bovino - Nueva Arquitectura"""

    numero_marca = models.CharField(
        max_length=50,
        unique=True,
        help_text="Número único de identificación de la marca",
    )
    nombre_productor = models.CharField(
        max_length=200, help_text="Nombre completo del productor ganadero"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True, help_text="Fecha y hora de registro de la solicitud"
    )
    fecha_procesamiento = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha y hora cuando se procesó la certificación",
    )
    estado = models.CharField(
        max_length=20,
        choices=[(choice.value, choice.value) for choice in EstadoMarca],
        default=EstadoMarca.PENDIENTE.value,
        help_text="Estado actual del proceso de certificación",
    )
    monto_certificacion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Costo de la certificación en bolivianos",
    )

    # Campos específicos para ganado bovino
    raza_bovino = models.CharField(
        max_length=100,
        choices=[(choice.value, choice.value) for choice in RazaBovino],
        default=RazaBovino.CRIOLLO.value,
        help_text="Raza del ganado bovino",
    )

    proposito_ganado = models.CharField(
        max_length=50,
        choices=[(choice.value, choice.value) for choice in PropositoGanado],
        default=PropositoGanado.CARNE.value,
        help_text="Propósito principal del ganado",
    )

    cantidad_cabezas = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        help_text="Número de cabezas de ganado bovino registradas",
    )

    # Ubicación geográfica
    departamento = models.CharField(
        max_length=100,
        choices=[(choice.value, choice.value) for choice in Departamento],
        help_text="Departamento donde se encuentra el ganado",
    )
    municipio = models.CharField(
        max_length=100, help_text="Municipio donde se encuentra el ganado"
    )
    comunidad = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Comunidad o zona específica (opcional)",
    )

    # Datos del propietario
    ci_productor = models.CharField(
        max_length=20, help_text="Cédula de identidad del productor"
    )
    telefono_productor = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Teléfono de contacto del productor",
    )

    # Métricas de procesamiento
    tiempo_procesamiento_horas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Tiempo total de procesamiento en horas",
    )

    # Observaciones
    observaciones = models.TextField(
        blank=True,
        null=True,
        help_text="Observaciones adicionales sobre la marca o el proceso",
    )

    # Metadatos
    creado_por = models.CharField(
        max_length=100, blank=True, null=True, help_text="Usuario que registró la marca"
    )
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "marca_ganado_bovino"
        ordering = ["-fecha_registro"]
        verbose_name = "Marca de Ganado Bovino"
        verbose_name_plural = "Marcas de Ganado Bovino"
        indexes = [
            models.Index(fields=["numero_marca"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["departamento"]),
            models.Index(fields=["fecha_registro"]),
        ]

    def __str__(self):
        return f"{self.numero_marca} - {self.nombre_productor} ({self.get_raza_bovino_display()})"

    def clean(self):
        """Validaciones personalizadas"""
        from django.core.exceptions import ValidationError

        if self.fecha_procesamiento and self.fecha_procesamiento < self.fecha_registro:
            raise ValidationError(
                "La fecha de procesamiento no puede ser anterior a la fecha de registro"
            )

    @property
    def esta_procesado(self):
        """Retorna True si la marca ya fue procesada"""
        return self.estado in ["APROBADO", "RECHAZADO"]

    @property
    def dias_desde_registro(self):
        """Retorna los días transcurridos desde el registro"""
        if self.fecha_registro:
            return (datetime.now().date() - self.fecha_registro.date()).days
        return 0
