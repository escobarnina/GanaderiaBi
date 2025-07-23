"""
Serializers de Clean Architecture para reportes
Trabajan con entidades de dominio, no con modelos Django
"""

from rest_framework import serializers
from typing import Dict, Any, List

from apps.analytics.domain.entities.reporte_data import ReporteData


class ReporteDataSerializer(serializers.Serializer):
    """Serializer para entidad ReporteData"""

    # Campos principales
    periodo = serializers.CharField()
    tipo_reporte = serializers.CharField()
    datos = serializers.DictField()
    filtros = serializers.DictField()
    formato = serializers.CharField(default="json")

    def to_entity(self, validated_data: Dict[str, Any]) -> ReporteData:
        """Convierte datos validados a entidad de dominio"""
        return ReporteData(
            periodo=validated_data["periodo"],
            tipo_reporte=validated_data["tipo_reporte"],
            datos=validated_data.get("datos", {}),
            filtros=validated_data.get("filtros", {}),
            formato=validated_data.get("formato", "json"),
        )

    def to_representation(self, entity: ReporteData) -> Dict[str, Any]:
        """Convierte entidad de dominio a representación JSON"""
        return {
            "periodo": entity.periodo,
            "tipo_reporte": entity.tipo_reporte,
            "datos": entity.datos,
            "filtros": entity.filtros,
            "formato": entity.formato,
        }


class ReporteMensualSerializer(serializers.Serializer):
    """Serializer para reporte mensual"""

    mes = serializers.CharField()
    año = serializers.IntegerField()
    total_marcas = serializers.IntegerField()
    marcas_aprobadas = serializers.IntegerField()
    marcas_rechazadas = serializers.IntegerField()
    marcas_pendientes = serializers.IntegerField()
    ingresos_totales = serializers.DecimalField(max_digits=15, decimal_places=2)
    tiempo_promedio_procesamiento = serializers.FloatField()

    # Distribución por propósito
    marcas_carne = serializers.IntegerField()
    marcas_leche = serializers.IntegerField()
    marcas_doble_proposito = serializers.IntegerField()
    marcas_reproduccion = serializers.IntegerField()

    # Distribución por departamento
    marcas_santa_cruz = serializers.IntegerField()
    marcas_beni = serializers.IntegerField()
    marcas_la_paz = serializers.IntegerField()
    marcas_otros_departamentos = serializers.IntegerField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "mes": data.get("mes", ""),
            "año": data.get("año", 0),
            "total_marcas": data.get("total_marcas", 0),
            "marcas_aprobadas": data.get("marcas_aprobadas", 0),
            "marcas_rechazadas": data.get("marcas_rechazadas", 0),
            "marcas_pendientes": data.get("marcas_pendientes", 0),
            "ingresos_totales": str(data.get("ingresos_totales", 0)),
            "tiempo_promedio_procesamiento": data.get(
                "tiempo_promedio_procesamiento", 0.0
            ),
            "marcas_carne": data.get("marcas_carne", 0),
            "marcas_leche": data.get("marcas_leche", 0),
            "marcas_doble_proposito": data.get("marcas_doble_proposito", 0),
            "marcas_reproduccion": data.get("marcas_reproduccion", 0),
            "marcas_santa_cruz": data.get("marcas_santa_cruz", 0),
            "marcas_beni": data.get("marcas_beni", 0),
            "marcas_la_paz": data.get("marcas_la_paz", 0),
            "marcas_otros_departamentos": data.get("marcas_otros_departamentos", 0),
        }


class ReporteAnualSerializer(serializers.Serializer):
    """Serializer para reporte anual"""

    año = serializers.IntegerField()
    total_marcas = serializers.IntegerField()
    marcas_aprobadas = serializers.IntegerField()
    marcas_rechazadas = serializers.IntegerField()
    ingresos_totales = serializers.DecimalField(max_digits=15, decimal_places=2)
    crecimiento_anual = serializers.FloatField()

    # Tendencias mensuales
    tendencias_mensuales = serializers.ListField(child=serializers.DictField())

    # Top departamentos
    top_departamentos = serializers.ListField(child=serializers.DictField())

    # Top razas
    top_razas = serializers.ListField(child=serializers.DictField())

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "año": data.get("año", 0),
            "total_marcas": data.get("total_marcas", 0),
            "marcas_aprobadas": data.get("marcas_aprobadas", 0),
            "marcas_rechazadas": data.get("marcas_rechazadas", 0),
            "ingresos_totales": str(data.get("ingresos_totales", 0)),
            "crecimiento_anual": data.get("crecimiento_anual", 0.0),
            "tendencias_mensuales": data.get("tendencias_mensuales", []),
            "top_departamentos": data.get("top_departamentos", []),
            "top_razas": data.get("top_razas", []),
        }


class ReporteComparativoDepartamentosSerializer(serializers.Serializer):
    """Serializer para reporte comparativo entre departamentos"""

    periodo = serializers.CharField()
    departamentos = serializers.ListField(child=serializers.DictField())
    metricas_comparativas = serializers.DictField()
    ranking_eficiencia = serializers.ListField(child=serializers.DictField())

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "periodo": data.get("periodo", ""),
            "departamentos": data.get("departamentos", []),
            "metricas_comparativas": data.get("metricas_comparativas", {}),
            "ranking_eficiencia": data.get("ranking_eficiencia", []),
        }


class ReportePersonalizadoSerializer(serializers.Serializer):
    """Serializer para reporte personalizado"""

    nombre_reporte = serializers.CharField()
    fecha_generacion = serializers.DateTimeField()
    filtros_aplicados = serializers.DictField()
    metricas_incluidas = serializers.ListField(child=serializers.CharField())
    datos_resultado = serializers.DictField()
    formato_exportacion = serializers.CharField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "nombre_reporte": data.get("nombre_reporte", ""),
            "fecha_generacion": data.get("fecha_generacion"),
            "filtros_aplicados": data.get("filtros_aplicados", {}),
            "metricas_incluidas": data.get("metricas_incluidas", []),
            "datos_resultado": data.get("datos_resultado", {}),
            "formato_exportacion": data.get("formato_exportacion", "json"),
        }


class ReporteProductorSerializer(serializers.Serializer):
    """Serializer para reporte de productor específico"""

    productor_id = serializers.CharField()
    nombre_productor = serializers.CharField()
    periodo = serializers.CharField()
    total_marcas = serializers.IntegerField()
    marcas_aprobadas = serializers.IntegerField()
    marcas_pendientes = serializers.IntegerField()
    marcas_rechazadas = serializers.IntegerField()
    total_cabezas = serializers.IntegerField()
    ingresos_totales = serializers.DecimalField(max_digits=15, decimal_places=2)

    # Distribución por propósito
    marcas_carne = serializers.IntegerField()
    marcas_leche = serializers.IntegerField()
    marcas_doble_proposito = serializers.IntegerField()
    marcas_reproduccion = serializers.IntegerField()

    # Historial de actividad
    historial_actividad = serializers.ListField(child=serializers.DictField())

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "productor_id": data.get("productor_id", ""),
            "nombre_productor": data.get("nombre_productor", ""),
            "periodo": data.get("periodo", ""),
            "total_marcas": data.get("total_marcas", 0),
            "marcas_aprobadas": data.get("marcas_aprobadas", 0),
            "marcas_pendientes": data.get("marcas_pendientes", 0),
            "marcas_rechazadas": data.get("marcas_rechazadas", 0),
            "total_cabezas": data.get("total_cabezas", 0),
            "ingresos_totales": str(data.get("ingresos_totales", 0)),
            "marcas_carne": data.get("marcas_carne", 0),
            "marcas_leche": data.get("marcas_leche", 0),
            "marcas_doble_proposito": data.get("marcas_doble_proposito", 0),
            "marcas_reproduccion": data.get("marcas_reproduccion", 0),
            "historial_actividad": data.get("historial_actividad", []),
        }


class ReporteImpactoEconomicoSerializer(serializers.Serializer):
    """Serializer para reporte de impacto económico"""

    periodo = serializers.CharField()
    ingresos_totales = serializers.DecimalField(max_digits=15, decimal_places=2)
    crecimiento_ingresos = serializers.FloatField()
    contribucion_por_departamento = serializers.ListField(child=serializers.DictField())
    proyeccion_futura = serializers.DictField()
    indicadores_economicos = serializers.DictField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "periodo": data.get("periodo", ""),
            "ingresos_totales": str(data.get("ingresos_totales", 0)),
            "crecimiento_ingresos": data.get("crecimiento_ingresos", 0.0),
            "contribucion_por_departamento": data.get(
                "contribucion_por_departamento", []
            ),
            "proyeccion_futura": data.get("proyeccion_futura", {}),
            "indicadores_economicos": data.get("indicadores_economicos", {}),
        }


class ReporteInnovacionTecnologicaSerializer(serializers.Serializer):
    """Serializer para reporte de innovación tecnológica"""

    periodo = serializers.CharField()
    total_logos_generados = serializers.IntegerField()
    tasa_exito_ia = serializers.FloatField()
    modelos_utilizados = serializers.ListField(child=serializers.DictField())
    tiempo_promedio_generacion = serializers.FloatField()
    calidad_promedio = serializers.FloatField()
    tendencias_tecnologicas = serializers.ListField(child=serializers.DictField())

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "periodo": data.get("periodo", ""),
            "total_logos_generados": data.get("total_logos_generados", 0),
            "tasa_exito_ia": data.get("tasa_exito_ia", 0.0),
            "modelos_utilizados": data.get("modelos_utilizados", []),
            "tiempo_promedio_generacion": data.get("tiempo_promedio_generacion", 0.0),
            "calidad_promedio": data.get("calidad_promedio", 0.0),
            "tendencias_tecnologicas": data.get("tendencias_tecnologicas", []),
        }


class ReporteSostenibilidadSerializer(serializers.Serializer):
    """Serializer para reporte de sostenibilidad"""

    periodo = serializers.CharField()
    total_cabezas_registradas = serializers.IntegerField()
    distribucion_por_proposito = serializers.DictField()
    impacto_ambiental = serializers.DictField()
    metricas_sostenibilidad = serializers.DictField()
    recomendaciones = serializers.ListField(child=serializers.CharField())

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "periodo": data.get("periodo", ""),
            "total_cabezas_registradas": data.get("total_cabezas_registradas", 0),
            "distribucion_por_proposito": data.get("distribucion_por_proposito", {}),
            "impacto_ambiental": data.get("impacto_ambiental", {}),
            "metricas_sostenibilidad": data.get("metricas_sostenibilidad", {}),
            "recomendaciones": data.get("recomendaciones", []),
        }


class ExportacionReporteSerializer(serializers.Serializer):
    """Serializer para exportación de reportes"""

    nombre_archivo = serializers.CharField()
    formato = serializers.CharField()
    contenido = serializers.CharField()
    fecha_exportacion = serializers.DateTimeField()
    tamano_archivo = serializers.IntegerField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "nombre_archivo": data.get("nombre_archivo", ""),
            "formato": data.get("formato", ""),
            "contenido": data.get("contenido", ""),
            "fecha_exportacion": data.get("fecha_exportacion"),
            "tamano_archivo": data.get("tamano_archivo", 0),
        }
