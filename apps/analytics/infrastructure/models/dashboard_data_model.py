# apps/analytics/infrastructure/models/dashboard_data_model.py
"""
Modelo Django para datos del dashboard - Single Responsibility
Responsabilidad única: Gestionar datos agregados para visualización
"""

from django.db import models


class DashboardDataModel(models.Model):
    """Modelo Django para datos del dashboard - Nueva Arquitectura"""

    fecha_actualizacion = models.DateTimeField(auto_now_add=True)

    # KPIs principales
    marcas_registradas_mes_actual = models.IntegerField(default=0)
    tiempo_promedio_procesamiento = models.FloatField(default=0)
    porcentaje_aprobacion = models.FloatField(default=0)
    porcentaje_rechazo = models.FloatField(default=0)
    ingresos_mes_actual = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )

    # KPIs específicos bovinos
    total_cabezas_bovinas = models.IntegerField(default=0)
    promedio_cabezas_por_marca = models.FloatField(default=0)

    # Distribución por propósito
    porcentaje_carne = models.FloatField(default=0)
    porcentaje_leche = models.FloatField(default=0)
    porcentaje_doble_proposito = models.FloatField(default=0)
    porcentaje_reproduccion = models.FloatField(default=0)

    # Distribución por raza más común
    raza_mas_comun = models.CharField(max_length=100, default="")
    porcentaje_raza_principal = models.FloatField(default=0)

    # KPIs de logos
    tasa_exito_logos = models.FloatField(default=0)
    total_marcas_sistema = models.IntegerField(default=0)
    marcas_pendientes = models.IntegerField(default=0)

    # Alertas (JSON field)
    alertas = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "dashboard_data"
        verbose_name = "Datos del Dashboard"
        verbose_name_plural = "Datos del Dashboard"
        ordering = ["-fecha_actualizacion"]

    def __str__(self):
        return f"Dashboard {self.fecha_actualizacion} - {self.marcas_registradas_mes_actual} marcas"
