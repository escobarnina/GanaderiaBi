# apps/analytics/infrastructure/models/historial_estado_marca_model.py
"""
Modelo Django para historial de estados de marcas - Single Responsibility
Responsabilidad única: Gestionar auditoría de cambios de estado
"""

from django.db import models
from .marca_ganado_bovino_model import MarcaGanadoBovinoModel


class HistorialEstadoMarcaModel(models.Model):
    """Modelo Django para historial de estados - Nueva Arquitectura"""

    marca = models.ForeignKey(
        MarcaGanadoBovinoModel,
        on_delete=models.CASCADE,
        related_name="historial_estados",
    )
    estado_anterior = models.CharField(max_length=20, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=20)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    usuario_responsable = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Usuario que realizó el cambio de estado",
    )
    observaciones_cambio = models.TextField(
        blank=True, null=True, help_text="Observaciones sobre el cambio de estado"
    )

    class Meta:
        db_table = "historial_estado_marca"
        verbose_name = "Historial de Estado"
        verbose_name_plural = "Historiales de Estados"
        ordering = ["-fecha_cambio"]

    def __str__(self):
        return (
            f"{self.marca.numero_marca}: {self.estado_anterior} → {self.estado_nuevo}"
        )
