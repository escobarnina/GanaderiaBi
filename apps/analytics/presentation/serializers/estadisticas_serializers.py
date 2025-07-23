"""
Serializers para Estadísticas de ganado bovino
Trabajan con entidades de dominio, no con modelos Django
"""

from rest_framework import serializers
from typing import Dict, Any, List


class EstadisticasPorRazaSerializer(serializers.Serializer):
    """Serializer para estadísticas por raza"""

    raza = serializers.CharField()
    total_marcas = serializers.IntegerField()
    porcentaje = serializers.FloatField()
    departamentos = serializers.ListField(child=serializers.CharField())
    tendencia = serializers.CharField()
    eficiencia_promedio = serializers.FloatField()


class EstadisticasPorDepartamentoSerializer(serializers.Serializer):
    """Serializer para estadísticas por departamento"""

    departamento = serializers.CharField()
    total_marcas = serializers.IntegerField()
    porcentaje = serializers.FloatField()
    razas_principales = serializers.ListField(child=serializers.CharField())
    densidad_ganadera = serializers.FloatField()
    crecimiento_anual = serializers.FloatField()


class EstadisticasPorPropositoSerializer(serializers.Serializer):
    """Serializer para estadísticas por propósito"""

    proposito = serializers.CharField()
    total_marcas = serializers.IntegerField()
    porcentaje = serializers.FloatField()
    departamentos_principales = serializers.ListField(child=serializers.CharField())
    valor_economico_promedio = serializers.FloatField()
    tendencia_crecimiento = serializers.CharField()


class ComparativaTemporalSerializer(serializers.Serializer):
    """Serializer para comparativa temporal"""

    periodo_analisis = serializers.CharField()
    comparativa_mensual = serializers.DictField()
    comparativa_trimestral = serializers.DictField()
    comparativa_anual = serializers.DictField()
    tendencias = serializers.ListField()
    crecimiento_anual = serializers.FloatField()
    estacionalidad = serializers.DictField()
    volatilidad = serializers.FloatField()


class PrediccionesDemandaSerializer(serializers.Serializer):
    """Serializer para predicciones de demanda"""

    periodo_prediccion = serializers.CharField()
    predicciones_base = serializers.DictField()
    recomendaciones_planificacion = serializers.ListField()
    corredores_ganaderos = serializers.ListField()
    migracion_razas = serializers.DictField()
    concentracion_mercado = serializers.DictField()
    mapa_razas_departamentos = serializers.DictField()
    recomendaciones_diversificacion = serializers.ListField()


class TendenciasGeograficasSerializer(serializers.Serializer):
    """Serializer para tendencias geográficas"""

    periodo_analisis = serializers.CharField()
    diversificacion_geografica = serializers.DictField()
    evolucion_tecnologica = serializers.DictField()
    profesionalizacion = serializers.DictField()
    gini_departamental = serializers.FloatField()


class RendimientoModelosIASerializer(serializers.Serializer):
    """Serializer para rendimiento de modelos IA"""

    año = serializers.IntegerField()
    tendencias_ia = serializers.DictField()
    recomendaciones_ia = serializers.ListField()
    correlaciones_marca_logo = serializers.DictField()
    analisis_tamaño_operacion = serializers.DictField()


class AnalisisEficienciaSerializer(serializers.Serializer):
    """Serializer para análisis de eficiencia"""

    periodo_analisis = serializers.CharField()
    metricas_eficiencia = serializers.DictField()
    tendencias_rendimiento = serializers.DictField()
    optimizaciones_recomendadas = serializers.ListField()


class DistribucionRazasSerializer(serializers.Serializer):
    """Serializer para distribución de razas"""

    año = serializers.IntegerField()
    distribucion_razas = serializers.DictField()
    mapa_razas_departamentos = serializers.DictField()
    recomendaciones_diversificacion = serializers.ListField()
    tendencias_razas = serializers.DictField()
