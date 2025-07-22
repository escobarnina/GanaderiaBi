# apps/analytics/infrastructure/models/reporte_data_model.py
"""
Modelo Django para datos de reportes - Single Responsibility
Responsabilidad única: Gestionar datos de reportes generados
"""

from django.db import models


class ReporteDataModel(models.Model):
    """Modelo Django para datos de reportes - Nueva Arquitectura"""

    fecha_generacion = models.DateTimeField(auto_now_add=True)
    tipo_reporte = models.CharField(max_length=50)
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    formato = models.CharField(max_length=20, default="json")
    datos = models.JSONField()
    usuario_generador = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "reporte_data"
        verbose_name = "Datos de Reporte"
        verbose_name_plural = "Datos de Reportes"
        ordering = ["-fecha_generacion"]

    def __str__(self):
        return f"Reporte {self.tipo_reporte} - {self.fecha_generacion}"
