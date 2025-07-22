"""
Serializers de Clean Architecture para marcas de ganado bovino
Trabajan con entidades de dominio, no con modelos Django
"""

from rest_framework import serializers
from typing import Dict, Any, List

from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.enums import (
    EstadoMarca,
    RazaBovino,
    PropositoGanado,
    Departamento,
)


class MarcaGanadoBovinoSerializer(serializers.Serializer):
    """Serializer para entidad MarcaGanadoBovino"""

    # Campos principales
    id = serializers.IntegerField(read_only=True)
    numero_marca = serializers.CharField(max_length=50)
    nombre_productor = serializers.CharField(max_length=200)
    fecha_registro = serializers.DateTimeField(read_only=True)
    fecha_procesamiento = serializers.DateTimeField(required=False, allow_null=True)
    estado = serializers.ChoiceField(choices=EstadoMarca.choices())
    monto_certificacion = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0
    )

    # Campos específicos bovinos
    raza_bovino = serializers.ChoiceField(choices=RazaBovino.choices())
    proposito_ganado = serializers.ChoiceField(choices=PropositoGanado.choices())
    cantidad_cabezas = serializers.IntegerField(min_value=1, max_value=10000)

    # Ubicación geográfica
    departamento = serializers.ChoiceField(choices=Departamento.choices())
    municipio = serializers.CharField(max_length=100)
    comunidad = serializers.CharField(
        max_length=150, required=False, allow_blank=True, allow_null=True
    )

    # Datos del propietario
    ci_productor = serializers.CharField(max_length=20)
    telefono_productor = serializers.CharField(
        max_length=20, required=False, allow_blank=True, allow_null=True
    )

    # Métricas de procesamiento
    tiempo_procesamiento_horas = serializers.IntegerField(
        required=False, allow_null=True, min_value=0
    )

    # Observaciones
    observaciones = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    # Metadatos
    creado_por = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True
    )
    actualizado_en = serializers.DateTimeField(read_only=True)

    # Campos calculados
    esta_procesado = serializers.BooleanField(read_only=True)
    dias_desde_registro = serializers.IntegerField(read_only=True)

    # Campos con display names
    raza_bovino_display = serializers.CharField(read_only=True)
    proposito_ganado_display = serializers.CharField(read_only=True)
    estado_display = serializers.CharField(read_only=True)
    departamento_display = serializers.CharField(read_only=True)

    def to_entity(self, validated_data: Dict[str, Any]) -> MarcaGanadoBovino:
        """Convierte datos validados a entidad de dominio"""
        return MarcaGanadoBovino(
            id=validated_data.get("id"),
            numero_marca=validated_data["numero_marca"],
            nombre_productor=validated_data["nombre_productor"],
            fecha_registro=validated_data.get("fecha_registro"),
            fecha_procesamiento=validated_data.get("fecha_procesamiento"),
            estado=EstadoMarca(validated_data["estado"]),
            monto_certificacion=validated_data["monto_certificacion"],
            raza_bovino=RazaBovino(validated_data["raza_bovino"]),
            proposito_ganado=PropositoGanado(validated_data["proposito_ganado"]),
            cantidad_cabezas=validated_data["cantidad_cabezas"],
            departamento=Departamento(validated_data["departamento"]),
            municipio=validated_data["municipio"],
            comunidad=validated_data.get("comunidad"),
            ci_productor=validated_data["ci_productor"],
            telefono_productor=validated_data.get("telefono_productor"),
            tiempo_procesamiento_horas=validated_data.get("tiempo_procesamiento_horas"),
            observaciones=validated_data.get("observaciones"),
            creado_por=validated_data.get("creado_por"),
            actualizado_en=validated_data.get("actualizado_en"),
        )

    def to_representation(self, entity: MarcaGanadoBovino) -> Dict[str, Any]:
        """Convierte entidad de dominio a representación JSON"""
        return {
            "id": entity.id,
            "numero_marca": entity.numero_marca,
            "nombre_productor": entity.nombre_productor,
            "fecha_registro": entity.fecha_registro,
            "fecha_procesamiento": entity.fecha_procesamiento,
            "estado": entity.estado.value,
            "estado_display": entity.estado.display_name(),
            "monto_certificacion": str(entity.monto_certificacion),
            "raza_bovino": entity.raza_bovino.value,
            "raza_bovino_display": entity.raza_bovino.display_name(),
            "proposito_ganado": entity.proposito_ganado.value,
            "proposito_ganado_display": entity.proposito_ganado.display_name(),
            "cantidad_cabezas": entity.cantidad_cabezas,
            "departamento": entity.departamento.value,
            "departamento_display": entity.departamento.display_name(),
            "municipio": entity.municipio,
            "comunidad": entity.comunidad,
            "ci_productor": entity.ci_productor,
            "telefono_productor": entity.telefono_productor,
            "tiempo_procesamiento_horas": entity.tiempo_procesamiento_horas,
            "observaciones": entity.observaciones,
            "creado_por": entity.creado_por,
            "actualizado_en": entity.actualizado_en,
            "esta_procesado": entity.esta_procesado,
            "dias_desde_registro": entity.dias_desde_registro,
        }

    def validate_ci_productor(self, value: str) -> str:
        """Validación para cédula de identidad"""
        if value and len(value) < 6:
            raise serializers.ValidationError(
                "La cédula de identidad debe tener al menos 6 caracteres"
            )
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validaciones a nivel de objeto"""
        if data.get("fecha_procesamiento") and data.get("fecha_registro"):
            if data["fecha_procesamiento"] < data["fecha_registro"]:
                raise serializers.ValidationError(
                    "La fecha de procesamiento no puede ser anterior a la fecha de registro"
                )
        return data


class MarcaGanadoBovinoListSerializer(serializers.Serializer):
    """Serializer simplificado para listados de marcas"""

    id = serializers.IntegerField()
    numero_marca = serializers.CharField()
    nombre_productor = serializers.CharField()
    raza_bovino = serializers.CharField()
    raza_bovino_display = serializers.CharField()
    proposito_ganado = serializers.CharField()
    proposito_ganado_display = serializers.CharField()
    cantidad_cabezas = serializers.IntegerField()
    departamento = serializers.CharField()
    departamento_display = serializers.CharField()
    municipio = serializers.CharField()
    estado = serializers.CharField()
    estado_display = serializers.CharField()
    monto_certificacion = serializers.CharField()
    fecha_registro = serializers.DateTimeField()
    dias_desde_registro = serializers.IntegerField()
    total_logos = serializers.IntegerField(required=False)

    def to_representation(self, entity: MarcaGanadoBovino) -> Dict[str, Any]:
        """Convierte entidad a representación para listado"""
        return {
            "id": entity.id,
            "numero_marca": entity.numero_marca,
            "nombre_productor": entity.nombre_productor,
            "raza_bovino": entity.raza_bovino.value,
            "raza_bovino_display": entity.raza_bovino.display_name(),
            "proposito_ganado": entity.proposito_ganado.value,
            "proposito_ganado_display": entity.proposito_ganado.display_name(),
            "cantidad_cabezas": entity.cantidad_cabezas,
            "departamento": entity.departamento.value,
            "departamento_display": entity.departamento.display_name(),
            "municipio": entity.municipio,
            "estado": entity.estado.value,
            "estado_display": entity.estado.display_name(),
            "monto_certificacion": str(entity.monto_certificacion),
            "fecha_registro": entity.fecha_registro,
            "dias_desde_registro": entity.dias_desde_registro,
        }


class HistorialEstadoMarcaSerializer(serializers.Serializer):
    """Serializer para entidad HistorialEstadoMarca"""

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
    tiempo_transcurrido = serializers.CharField(read_only=True)

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
        }

    def _calcular_tiempo_transcurrido(self, fecha_cambio: datetime) -> str:
        """Calcula el tiempo transcurrido desde el cambio"""
        from datetime import datetime

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
