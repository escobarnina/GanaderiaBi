"""
Serializers de Clean Architecture para dashboard
Trabajan con entidades de dominio, no con modelos Django
"""

from rest_framework import serializers
from typing import Dict, Any, List

from apps.analytics.domain.entities.dashboard_data import DashboardData


class DashboardDataSerializer(serializers.Serializer):
    """Serializer para entidad DashboardData"""

    # KPIs principales
    kpis_principales = serializers.DictField()
    tendencias_mensuales = serializers.ListField(child=serializers.DictField())
    metricas_tiempo_real = serializers.DictField()
    resumen_ejecutivo = serializers.DictField()

    def to_entity(self, validated_data: Dict[str, Any]) -> DashboardData:
        """Convierte datos validados a entidad de dominio"""
        return DashboardData(
            kpis_principales=validated_data.get("kpis_principales", {}),
            tendencias_mensuales=validated_data.get("tendencias_mensuales", []),
            metricas_tiempo_real=validated_data.get("metricas_tiempo_real", {}),
            resumen_ejecutivo=validated_data.get("resumen_ejecutivo", {}),
        )

    def to_representation(self, entity: DashboardData) -> Dict[str, Any]:
        """Convierte entidad de dominio a representación JSON"""
        return {
            "kpis_principales": entity.kpis_principales,
            "tendencias_mensuales": entity.tendencias_mensuales,
            "metricas_tiempo_real": entity.metricas_tiempo_real,
            "resumen_ejecutivo": entity.resumen_ejecutivo,
        }


class DashboardKPIBovinoSerializer(serializers.Serializer):
    """Serializer para KPIs del dashboard específicos para bovinos"""

    # KPIs principales
    marcas_registradas_mes_actual = serializers.IntegerField()
    tiempo_promedio_procesamiento = serializers.FloatField()
    porcentaje_aprobacion = serializers.FloatField()
    porcentaje_rechazo = serializers.FloatField()
    ingresos_mes_actual = serializers.DecimalField(max_digits=15, decimal_places=2)

    # KPIs específicos bovinos
    total_cabezas_bovinas = serializers.IntegerField()
    promedio_cabezas_por_marca = serializers.FloatField()

    # Distribución por propósito
    porcentaje_carne = serializers.FloatField()
    porcentaje_leche = serializers.FloatField()
    porcentaje_doble_proposito = serializers.FloatField()
    porcentaje_reproduccion = serializers.FloatField()

    # Distribución por raza más común
    raza_mas_comun = serializers.CharField()
    porcentaje_raza_principal = serializers.FloatField()

    # KPIs de logos
    tasa_exito_logos = serializers.FloatField()
    total_marcas_sistema = serializers.IntegerField()
    marcas_pendientes = serializers.IntegerField()

    # Indicadores de alerta
    alertas = serializers.ListField(child=serializers.DictField(), required=False)

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "marcas_registradas_mes_actual": data.get(
                "marcas_registradas_mes_actual", 0
            ),
            "tiempo_promedio_procesamiento": data.get(
                "tiempo_promedio_procesamiento", 0.0
            ),
            "porcentaje_aprobacion": data.get("porcentaje_aprobacion", 0.0),
            "porcentaje_rechazo": data.get("porcentaje_rechazo", 0.0),
            "ingresos_mes_actual": str(data.get("ingresos_mes_actual", 0)),
            "total_cabezas_bovinas": data.get("total_cabezas_bovinas", 0),
            "promedio_cabezas_por_marca": data.get("promedio_cabezas_por_marca", 0.0),
            "porcentaje_carne": data.get("porcentaje_carne", 0.0),
            "porcentaje_leche": data.get("porcentaje_leche", 0.0),
            "porcentaje_doble_proposito": data.get("porcentaje_doble_proposito", 0.0),
            "porcentaje_reproduccion": data.get("porcentaje_reproduccion", 0.0),
            "raza_mas_comun": data.get("raza_mas_comun", ""),
            "porcentaje_raza_principal": data.get("porcentaje_raza_principal", 0.0),
            "tasa_exito_logos": data.get("tasa_exito_logos", 0.0),
            "total_marcas_sistema": data.get("total_marcas_sistema", 0),
            "marcas_pendientes": data.get("marcas_pendientes", 0),
            "alertas": data.get("alertas", []),
        }


class EstadisticasMensualesBovinoSerializer(serializers.Serializer):
    """Serializer para estadísticas mensuales de ganado bovino"""

    mes = serializers.CharField()
    año = serializers.IntegerField()
    marcas_registradas = serializers.IntegerField()
    cabezas_registradas = serializers.IntegerField()
    ingresos = serializers.DecimalField(max_digits=15, decimal_places=2)
    tiempo_promedio = serializers.FloatField()

    # Distribución por propósito en el mes
    marcas_carne = serializers.IntegerField()
    marcas_leche = serializers.IntegerField()
    marcas_doble_proposito = serializers.IntegerField()
    marcas_reproduccion = serializers.IntegerField()

    # Departamentos más activos
    departamento_principal = serializers.CharField()
    marcas_departamento_principal = serializers.IntegerField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "mes": data.get("mes", ""),
            "año": data.get("año", 0),
            "marcas_registradas": data.get("marcas_registradas", 0),
            "cabezas_registradas": data.get("cabezas_registradas", 0),
            "ingresos": str(data.get("ingresos", 0)),
            "tiempo_promedio": data.get("tiempo_promedio", 0.0),
            "marcas_carne": data.get("marcas_carne", 0),
            "marcas_leche": data.get("marcas_leche", 0),
            "marcas_doble_proposito": data.get("marcas_doble_proposito", 0),
            "marcas_reproduccion": data.get("marcas_reproduccion", 0),
            "departamento_principal": data.get("departamento_principal", ""),
            "marcas_departamento_principal": data.get(
                "marcas_departamento_principal", 0
            ),
        }


class EstadisticasPorRazaSerializer(serializers.Serializer):
    """Serializer para estadísticas por raza bovina"""

    raza_bovino = serializers.CharField()
    raza_display = serializers.CharField()
    total_marcas = serializers.IntegerField()
    total_cabezas = serializers.IntegerField()
    promedio_cabezas = serializers.FloatField()
    monto_promedio = serializers.DecimalField(max_digits=10, decimal_places=2)
    tiempo_promedio_procesamiento = serializers.FloatField()
    porcentaje_aprobacion = serializers.FloatField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "raza_bovino": data.get("raza_bovino", ""),
            "raza_display": data.get("raza_display", ""),
            "total_marcas": data.get("total_marcas", 0),
            "total_cabezas": data.get("total_cabezas", 0),
            "promedio_cabezas": data.get("promedio_cabezas", 0.0),
            "monto_promedio": str(data.get("monto_promedio", 0)),
            "tiempo_promedio_procesamiento": data.get(
                "tiempo_promedio_procesamiento", 0.0
            ),
            "porcentaje_aprobacion": data.get("porcentaje_aprobacion", 0.0),
        }


class EstadisticasPorDepartamentoSerializer(serializers.Serializer):
    """Serializer para estadísticas por departamento"""

    departamento = serializers.CharField()
    departamento_display = serializers.CharField()
    total_marcas = serializers.IntegerField()
    total_cabezas = serializers.IntegerField()
    aprobadas = serializers.IntegerField()
    rechazadas = serializers.IntegerField()
    pendientes = serializers.IntegerField()
    ingresos_total = serializers.DecimalField(max_digits=15, decimal_places=2)
    tiempo_promedio_procesamiento = serializers.FloatField()

    # Propósito predominante en el departamento
    proposito_principal = serializers.CharField()
    raza_principal = serializers.CharField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "departamento": data.get("departamento", ""),
            "departamento_display": data.get("departamento_display", ""),
            "total_marcas": data.get("total_marcas", 0),
            "total_cabezas": data.get("total_cabezas", 0),
            "aprobadas": data.get("aprobadas", 0),
            "rechazadas": data.get("rechazadas", 0),
            "pendientes": data.get("pendientes", 0),
            "ingresos_total": str(data.get("ingresos_total", 0)),
            "tiempo_promedio_procesamiento": data.get(
                "tiempo_promedio_procesamiento", 0.0
            ),
            "proposito_principal": data.get("proposito_principal", ""),
            "raza_principal": data.get("raza_principal", ""),
        }


class RendimientoModelosIASerializer(serializers.Serializer):
    """Serializer para rendimiento de modelos de IA"""

    modelo_ia_usado = serializers.CharField()
    modelo_display = serializers.CharField()
    total_generados = serializers.IntegerField()
    exitosos = serializers.IntegerField()
    fallidos = serializers.IntegerField()
    tasa_exito = serializers.FloatField()
    tiempo_promedio_generacion = serializers.FloatField()
    tiempo_promedio_formateado = serializers.CharField()

    # Calidad de logos
    logos_alta_calidad = serializers.IntegerField()
    logos_media_calidad = serializers.IntegerField()
    logos_baja_calidad = serializers.IntegerField()
    porcentaje_alta_calidad = serializers.FloatField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "modelo_ia_usado": data.get("modelo_ia_usado", ""),
            "modelo_display": data.get("modelo_display", ""),
            "total_generados": data.get("total_generados", 0),
            "exitosos": data.get("exitosos", 0),
            "fallidos": data.get("fallidos", 0),
            "tasa_exito": data.get("tasa_exito", 0.0),
            "tiempo_promedio_generacion": data.get("tiempo_promedio_generacion", 0.0),
            "tiempo_promedio_formateado": data.get("tiempo_promedio_formateado", ""),
            "logos_alta_calidad": data.get("logos_alta_calidad", 0),
            "logos_media_calidad": data.get("logos_media_calidad", 0),
            "logos_baja_calidad": data.get("logos_baja_calidad", 0),
            "porcentaje_alta_calidad": data.get("porcentaje_alta_calidad", 0.0),
        }
