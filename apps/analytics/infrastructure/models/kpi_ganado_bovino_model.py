# apps/analytics/infrastructure/models/kpi_ganado_bovino_model.py
"""
Modelo Django para KPIs de ganado bovino - Single Responsibility
Responsabilidad única: Gestionar datos de indicadores clave de rendimiento
"""

from django.db import models


class KPIGanadoBovinoModel(models.Model):
    """Modelo Django para KPIs de ganado bovino - Nueva Arquitectura"""

    fecha = models.DateField(auto_now_add=True)

    # KPIs principales
    marcas_registradas_mes = models.IntegerField(
        default=0, help_text="Número de marcas bovinas registradas en el mes"
    )
    tiempo_promedio_procesamiento = models.FloatField(
        default=0, help_text="Tiempo promedio de procesamiento en horas"
    )
    porcentaje_aprobacion = models.FloatField(
        default=0, help_text="Porcentaje de marcas aprobadas"
    )
    ingresos_mes = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="Ingresos generados en el mes",
    )

    # KPIs específicos para bovinos
    total_cabezas_registradas = models.IntegerField(
        default=0, help_text="Total de cabezas de ganado bovino registradas"
    )
    promedio_cabezas_por_marca = models.FloatField(
        default=0, help_text="Promedio de cabezas por marca registrada"
    )

    # Distribución por propósito
    marcas_carne = models.IntegerField(default=0)
    marcas_leche = models.IntegerField(default=0)
    marcas_doble_proposito = models.IntegerField(default=0)
    marcas_reproduccion = models.IntegerField(default=0)

    # Distribución por departamentos más importantes
    marcas_santa_cruz = models.IntegerField(default=0)
    marcas_beni = models.IntegerField(default=0)
    marcas_la_paz = models.IntegerField(default=0)
    marcas_otros_departamentos = models.IntegerField(default=0)

    # KPIs de logos
    tasa_exito_logos = models.FloatField(
        default=0, help_text="Porcentaje de logos generados exitosamente"
    )
    total_logos_generados = models.IntegerField(
        default=0, help_text="Total de logos generados en el mes"
    )
    tiempo_promedio_generacion_logos = models.FloatField(
        default=0, help_text="Tiempo promedio de generación de logos en segundos"
    )

    class Meta:
        db_table = "kpi_ganado_bovino"
        unique_together = ["fecha"]
        verbose_name = "KPI Ganado Bovino"
        verbose_name_plural = "KPIs Ganado Bovino"
        ordering = ["-fecha"]

    def __str__(self):
        return f"KPI Bovino {self.fecha} - {self.marcas_registradas_mes} marcas"
