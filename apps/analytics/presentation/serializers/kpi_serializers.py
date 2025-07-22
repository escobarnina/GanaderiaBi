"""
Serializers de Clean Architecture para KPIs de ganado bovino
Trabajan con entidades de dominio, no con modelos Django
"""

from rest_framework import serializers
from typing import Dict, Any

from apps.analytics.domain.entities.kpi_ganado_bovino import KPIGanadoBovino


class KPIGanadoBovinoSerializer(serializers.Serializer):
    """Serializer para entidad KPIGanadoBovino"""

    # Campos principales
    id = serializers.IntegerField(read_only=True)
    fecha = serializers.DateField()

    # KPIs principales
    marcas_registradas_mes = serializers.IntegerField(default=0)
    tiempo_promedio_procesamiento = serializers.FloatField(default=0.0)
    porcentaje_aprobacion = serializers.FloatField(default=0.0)
    ingresos_mes = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)

    # KPIs específicos para bovinos
    total_cabezas_registradas = serializers.IntegerField(default=0)
    promedio_cabezas_por_marca = serializers.FloatField(default=0.0)

    # Distribución por propósito
    marcas_carne = serializers.IntegerField(default=0)
    marcas_leche = serializers.IntegerField(default=0)
    marcas_doble_proposito = serializers.IntegerField(default=0)
    marcas_reproduccion = serializers.IntegerField(default=0)

    # Distribución por departamentos
    marcas_santa_cruz = serializers.IntegerField(default=0)
    marcas_beni = serializers.IntegerField(default=0)
    marcas_la_paz = serializers.IntegerField(default=0)
    marcas_otros_departamentos = serializers.IntegerField(default=0)

    # KPIs de logos
    tasa_exito_logos = serializers.FloatField(default=0.0)
    total_logos_generados = serializers.IntegerField(default=0)
    tiempo_promedio_generacion_logos = serializers.FloatField(default=0.0)

    # Campos calculados adicionales
    eficiencia_aprobacion = serializers.DictField(read_only=True)
    eficiencia_tiempo = serializers.DictField(read_only=True)
    eficiencia_logos = serializers.DictField(read_only=True)
    distribucion_proposito = serializers.DictField(read_only=True)
    distribucion_geografica = serializers.DictField(read_only=True)
    tendencia_mensual = serializers.DictField(read_only=True)

    def to_entity(self, validated_data: Dict[str, Any]) -> KPIGanadoBovino:
        """Convierte datos validados a entidad de dominio"""
        return KPIGanadoBovino(
            id=validated_data.get("id"),
            fecha=validated_data["fecha"],
            marcas_registradas_mes=validated_data.get("marcas_registradas_mes", 0),
            tiempo_promedio_procesamiento=validated_data.get(
                "tiempo_promedio_procesamiento", 0.0
            ),
            porcentaje_aprobacion=validated_data.get("porcentaje_aprobacion", 0.0),
            ingresos_mes=validated_data.get("ingresos_mes", 0),
            total_cabezas_registradas=validated_data.get(
                "total_cabezas_registradas", 0
            ),
            promedio_cabezas_por_marca=validated_data.get(
                "promedio_cabezas_por_marca", 0.0
            ),
            marcas_carne=validated_data.get("marcas_carne", 0),
            marcas_leche=validated_data.get("marcas_leche", 0),
            marcas_doble_proposito=validated_data.get("marcas_doble_proposito", 0),
            marcas_reproduccion=validated_data.get("marcas_reproduccion", 0),
            marcas_santa_cruz=validated_data.get("marcas_santa_cruz", 0),
            marcas_beni=validated_data.get("marcas_beni", 0),
            marcas_la_paz=validated_data.get("marcas_la_paz", 0),
            marcas_otros_departamentos=validated_data.get(
                "marcas_otros_departamentos", 0
            ),
            tasa_exito_logos=validated_data.get("tasa_exito_logos", 0.0),
            total_logos_generados=validated_data.get("total_logos_generados", 0),
            tiempo_promedio_generacion_logos=validated_data.get(
                "tiempo_promedio_generacion_logos", 0.0
            ),
        )

    def to_representation(self, entity: KPIGanadoBovino) -> Dict[str, Any]:
        """Convierte entidad de dominio a representación JSON"""
        return {
            "id": entity.id,
            "fecha": entity.fecha,
            "marcas_registradas_mes": entity.marcas_registradas_mes,
            "tiempo_promedio_procesamiento": entity.tiempo_promedio_procesamiento,
            "porcentaje_aprobacion": entity.porcentaje_aprobacion,
            "ingresos_mes": str(entity.ingresos_mes),
            "total_cabezas_registradas": entity.total_cabezas_registradas,
            "promedio_cabezas_por_marca": entity.promedio_cabezas_por_marca,
            "marcas_carne": entity.marcas_carne,
            "marcas_leche": entity.marcas_leche,
            "marcas_doble_proposito": entity.marcas_doble_proposito,
            "marcas_reproduccion": entity.marcas_reproduccion,
            "marcas_santa_cruz": entity.marcas_santa_cruz,
            "marcas_beni": entity.marcas_beni,
            "marcas_la_paz": entity.marcas_la_paz,
            "marcas_otros_departamentos": entity.marcas_otros_departamentos,
            "tasa_exito_logos": entity.tasa_exito_logos,
            "total_logos_generados": entity.total_logos_generados,
            "tiempo_promedio_generacion_logos": entity.tiempo_promedio_generacion_logos,
            "eficiencia_aprobacion": self._calcular_eficiencia_aprobacion(
                entity.porcentaje_aprobacion
            ),
            "eficiencia_tiempo": self._calcular_eficiencia_tiempo(
                entity.tiempo_promedio_procesamiento
            ),
            "eficiencia_logos": self._calcular_eficiencia_logos(
                entity.tasa_exito_logos
            ),
            "distribucion_proposito": self._calcular_distribucion_proposito(entity),
            "distribucion_geografica": self._calcular_distribucion_geografica(entity),
            "tendencia_mensual": self._calcular_tendencia_mensual(entity),
        }

    def _calcular_eficiencia_aprobacion(self, porcentaje: float) -> Dict[str, Any]:
        """Califica la eficiencia de aprobación"""
        if porcentaje >= 80:
            return {"nivel": "alta", "color": "#4caf50", "descripcion": "Excelente"}
        elif porcentaje >= 60:
            return {"nivel": "media", "color": "#ff9800", "descripcion": "Aceptable"}
        else:
            return {
                "nivel": "baja",
                "color": "#f44336",
                "descripcion": "Requiere atención",
            }

    def _calcular_eficiencia_tiempo(self, tiempo: float) -> Dict[str, Any]:
        """Califica la eficiencia de tiempo de procesamiento"""
        if tiempo <= 24:
            return {"nivel": "alta", "color": "#4caf50", "descripcion": "Rápido"}
        elif tiempo <= 72:
            return {"nivel": "media", "color": "#ff9800", "descripcion": "Normal"}
        else:
            return {"nivel": "baja", "color": "#f44336", "descripcion": "Lento"}

    def _calcular_eficiencia_logos(self, tasa: float) -> Dict[str, Any]:
        """Califica la eficiencia de generación de logos"""
        if tasa >= 85:
            return {"nivel": "alta", "color": "#4caf50", "descripcion": "Óptima"}
        elif tasa >= 70:
            return {"nivel": "media", "color": "#ff9800", "descripcion": "Aceptable"}
        else:
            return {"nivel": "baja", "color": "#f44336", "descripcion": "Problemática"}

    def _calcular_distribucion_proposito(
        self, entity: KPIGanadoBovino
    ) -> Dict[str, float]:
        """Retorna la distribución porcentual por propósito"""
        total = (
            entity.marcas_carne
            + entity.marcas_leche
            + entity.marcas_doble_proposito
            + entity.marcas_reproduccion
        )

        if total == 0:
            return {"carne": 0, "leche": 0, "doble_proposito": 0, "reproduccion": 0}

        return {
            "carne": round((entity.marcas_carne / total) * 100, 1),
            "leche": round((entity.marcas_leche / total) * 100, 1),
            "doble_proposito": round((entity.marcas_doble_proposito / total) * 100, 1),
            "reproduccion": round((entity.marcas_reproduccion / total) * 100, 1),
        }

    def _calcular_distribucion_geografica(
        self, entity: KPIGanadoBovino
    ) -> Dict[str, float]:
        """Retorna la distribución porcentual por departamento"""
        total = (
            entity.marcas_santa_cruz
            + entity.marcas_beni
            + entity.marcas_la_paz
            + entity.marcas_otros_departamentos
        )

        if total == 0:
            return {"santa_cruz": 0, "beni": 0, "la_paz": 0, "otros": 0}

        return {
            "santa_cruz": round((entity.marcas_santa_cruz / total) * 100, 1),
            "beni": round((entity.marcas_beni / total) * 100, 1),
            "la_paz": round((entity.marcas_la_paz / total) * 100, 1),
            "otros": round((entity.marcas_otros_departamentos / total) * 100, 1),
        }

    def _calcular_tendencia_mensual(self, entity: KPIGanadoBovino) -> Dict[str, Any]:
        """Calcula la tendencia respecto al mes anterior"""
        # Esta lógica se implementaría en el use case
        return {"disponible": False}


class KPIGanadoBovinoListSerializer(serializers.Serializer):
    """Serializer simplificado para listados de KPIs"""

    id = serializers.IntegerField()
    fecha = serializers.DateField()
    marcas_registradas_mes = serializers.IntegerField()
    tiempo_promedio_procesamiento = serializers.FloatField()
    porcentaje_aprobacion = serializers.FloatField()
    ingresos_mes = serializers.CharField()
    total_cabezas_registradas = serializers.IntegerField()
    promedio_cabezas_por_marca = serializers.FloatField()

    def to_representation(self, entity: KPIGanadoBovino) -> Dict[str, Any]:
        """Convierte entidad a representación para listado"""
        return {
            "id": entity.id,
            "fecha": entity.fecha,
            "marcas_registradas_mes": entity.marcas_registradas_mes,
            "tiempo_promedio_procesamiento": entity.tiempo_promedio_procesamiento,
            "porcentaje_aprobacion": entity.porcentaje_aprobacion,
            "ingresos_mes": str(entity.ingresos_mes),
            "total_cabezas_registradas": entity.total_cabezas_registradas,
            "promedio_cabezas_por_marca": entity.promedio_cabezas_por_marca,
        }
