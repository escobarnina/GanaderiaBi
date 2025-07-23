"""
Serializers de Clean Architecture para historial de estados
Trabajan con entidades de dominio, no con modelos Django
"""

from rest_framework import serializers
from typing import Dict, Any, List
from datetime import datetime

from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca


class HistorialEstadoMarcaSerializer(serializers.Serializer):
    """Serializer para entidad HistorialEstadoMarca"""

    # Campos principales
    id = serializers.IntegerField(read_only=True)
    marca_id = serializers.IntegerField()
    estado_anterior = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    estado_nuevo = serializers.CharField()
    fecha_cambio = serializers.DateTimeField(read_only=True)
    usuario_responsable = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    observaciones_cambio = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    # Campos calculados
    tiempo_transcurrido = serializers.CharField(read_only=True)

    # Información de la marca relacionada
    marca_numero = serializers.CharField(read_only=True)
    marca_productor = serializers.CharField(read_only=True)

    def to_entity(self, validated_data: Dict[str, Any]) -> HistorialEstadoMarca:
        """Convierte datos validados a entidad de dominio"""
        return HistorialEstadoMarca(
            id=validated_data.get("id"),
            marca_id=validated_data["marca_id"],
            estado_anterior=validated_data.get("estado_anterior"),
            estado_nuevo=validated_data["estado_nuevo"],
            fecha_cambio=validated_data.get("fecha_cambio"),
            usuario_responsable=validated_data.get("usuario_responsable"),
            observaciones_cambio=validated_data.get("observaciones_cambio"),
        )

    def to_representation(self, entity: HistorialEstadoMarca) -> Dict[str, Any]:
        """Convierte entidad de dominio a representación JSON"""
        return {
            "id": entity.id,
            "marca_id": entity.marca_id,
            "estado_anterior": entity.estado_anterior,
            "estado_nuevo": entity.estado_nuevo,
            "fecha_cambio": entity.fecha_cambio,
            "usuario_responsable": entity.usuario_responsable,
            "observaciones_cambio": entity.observaciones_cambio,
            "tiempo_transcurrido": self._calcular_tiempo_transcurrido(
                entity.fecha_cambio
            ),
            # Campos de marca (se llenan desde el use case)
            "marca_numero": getattr(entity, "marca_numero", ""),
            "marca_productor": getattr(entity, "marca_productor", ""),
        }

    def _calcular_tiempo_transcurrido(self, fecha_cambio: datetime) -> str:
        """Calcula el tiempo transcurrido desde el cambio"""
        now = datetime.now().replace(tzinfo=fecha_cambio.tzinfo)
        delta = now - fecha_cambio

        if delta.days > 0:
            return f"Hace {delta.days} días"
        elif delta.seconds > 3600:
            horas = delta.seconds // 3600
            return f"Hace {horas} horas"
        elif delta.seconds > 60:
            minutos = delta.seconds // 60
            return f"Hace {minutos} minutos"
        else:
            return "Hace pocos segundos"


class HistorialEstadoMarcaListSerializer(serializers.Serializer):
    """Serializer simplificado para listados de historial"""

    id = serializers.IntegerField()
    marca_id = serializers.IntegerField()
    estado_anterior = serializers.CharField()
    estado_nuevo = serializers.CharField()
    fecha_cambio = serializers.DateTimeField()
    usuario_responsable = serializers.CharField()
    tiempo_transcurrido = serializers.CharField()

    def to_representation(self, entity: HistorialEstadoMarca) -> Dict[str, Any]:
        """Convierte entidad a representación para listado"""
        return {
            "id": entity.id,
            "marca_id": entity.marca_id,
            "estado_anterior": entity.estado_anterior,
            "estado_nuevo": entity.estado_nuevo,
            "fecha_cambio": entity.fecha_cambio,
            "usuario_responsable": entity.usuario_responsable,
            "tiempo_transcurrido": self._calcular_tiempo_transcurrido(
                entity.fecha_cambio
            ),
        }

    def _calcular_tiempo_transcurrido(self, fecha_cambio: datetime) -> str:
        """Calcula el tiempo transcurrido desde el cambio"""
        now = datetime.now().replace(tzinfo=fecha_cambio.tzinfo)
        delta = now - fecha_cambio

        if delta.days > 0:
            return f"Hace {delta.days} días"
        elif delta.seconds > 3600:
            horas = delta.seconds // 3600
            return f"Hace {horas} horas"
        elif delta.seconds > 60:
            minutos = delta.seconds // 60
            return f"Hace {minutos} minutos"
        else:
            return "Hace pocos segundos"


class ActividadRecienteSerializer(serializers.Serializer):
    """Serializer para actividad reciente del sistema"""

    fecha = serializers.DateField()
    total_cambios = serializers.IntegerField()
    cambios_aprobacion = serializers.IntegerField()
    cambios_rechazo = serializers.IntegerField()
    usuarios_activos = serializers.IntegerField()
    tiempo_promedio_cambio = serializers.FloatField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "fecha": data.get("fecha"),
            "total_cambios": data.get("total_cambios", 0),
            "cambios_aprobacion": data.get("cambios_aprobacion", 0),
            "cambios_rechazo": data.get("cambios_rechazo", 0),
            "usuarios_activos": data.get("usuarios_activos", 0),
            "tiempo_promedio_cambio": data.get("tiempo_promedio_cambio", 0.0),
        }


class AuditoriaUsuarioSerializer(serializers.Serializer):
    """Serializer para auditoría de usuarios"""

    usuario = serializers.CharField()
    total_cambios = serializers.IntegerField()
    cambios_aprobacion = serializers.IntegerField()
    cambios_rechazo = serializers.IntegerField()
    ultima_actividad = serializers.DateTimeField()
    tiempo_promedio_cambio = serializers.FloatField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "usuario": data.get("usuario", ""),
            "total_cambios": data.get("total_cambios", 0),
            "cambios_aprobacion": data.get("cambios_aprobacion", 0),
            "cambios_rechazo": data.get("cambios_rechazo", 0),
            "ultima_actividad": data.get("ultima_actividad"),
            "tiempo_promedio_cambio": data.get("tiempo_promedio_cambio", 0.0),
        }


class PatronesCambioSerializer(serializers.Serializer):
    """Serializer para patrones de cambio"""

    patron = serializers.CharField()
    frecuencia = serializers.IntegerField()
    tiempo_promedio = serializers.FloatField()
    usuarios_principales = serializers.ListField(child=serializers.CharField())
    departamentos_afectados = serializers.ListField(child=serializers.CharField())

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "patron": data.get("patron", ""),
            "frecuencia": data.get("frecuencia", 0),
            "tiempo_promedio": data.get("tiempo_promedio", 0.0),
            "usuarios_principales": data.get("usuarios_principales", []),
            "departamentos_afectados": data.get("departamentos_afectados", []),
        }


class EficienciaEvaluadoresSerializer(serializers.Serializer):
    """Serializer para eficiencia de evaluadores"""

    evaluador = serializers.CharField()
    total_evaluaciones = serializers.IntegerField()
    aprobaciones = serializers.IntegerField()
    rechazos = serializers.IntegerField()
    tiempo_promedio_evaluacion = serializers.FloatField()
    tasa_aprobacion = serializers.FloatField()

    def to_representation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte datos a representación JSON"""
        return {
            "evaluador": data.get("evaluador", ""),
            "total_evaluaciones": data.get("total_evaluaciones", 0),
            "aprobaciones": data.get("aprobaciones", 0),
            "rechazos": data.get("rechazos", 0),
            "tiempo_promedio_evaluacion": data.get("tiempo_promedio_evaluacion", 0.0),
            "tasa_aprobacion": data.get("tasa_aprobacion", 0.0),
        }
