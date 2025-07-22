"""
Serializers de Clean Architecture para logos de marcas bovinas
Trabajan con entidades de dominio, no con modelos Django
"""

from rest_framework import serializers
from typing import Dict, Any

from apps.analytics.domain.entities.logo_marca_bovina import LogoMarcaBovina
from apps.analytics.domain.enums import ModeloIA, CalidadLogo


class LogoMarcaBovinaSerializer(serializers.Serializer):
    """Serializer para entidad LogoMarcaBovina"""

    # Campos principales
    id = serializers.IntegerField(read_only=True)
    marca_id = serializers.IntegerField()
    url_logo = serializers.URLField()
    fecha_generacion = serializers.DateTimeField(read_only=True)
    exito = serializers.BooleanField(default=True)
    tiempo_generacion_segundos = serializers.IntegerField(min_value=0)
    modelo_ia_usado = serializers.ChoiceField(choices=ModeloIA.choices())
    prompt_usado = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    calidad_logo = serializers.ChoiceField(choices=CalidadLogo.choices())

    # Información de la marca relacionada
    marca_numero = serializers.CharField(read_only=True)
    marca_productor = serializers.CharField(read_only=True)
    marca_raza = serializers.CharField(read_only=True)

    # Campos con display names
    modelo_ia_display = serializers.CharField(read_only=True)
    calidad_logo_display = serializers.CharField(read_only=True)

    # Campos calculados
    tiempo_generacion_formateado = serializers.CharField(read_only=True)

    def to_entity(self, validated_data: Dict[str, Any]) -> LogoMarcaBovina:
        """Convierte datos validados a entidad de dominio"""
        return LogoMarcaBovina(
            id=validated_data.get("id"),
            marca_id=validated_data["marca_id"],
            url_logo=validated_data["url_logo"],
            fecha_generacion=validated_data.get("fecha_generacion"),
            exito=validated_data.get("exito", True),
            tiempo_generacion_segundos=validated_data["tiempo_generacion_segundos"],
            modelo_ia_usado=ModeloIA(validated_data["modelo_ia_usado"]),
            prompt_usado=validated_data.get("prompt_usado"),
            calidad_logo=CalidadLogo(validated_data["calidad_logo"]),
        )

    def to_representation(self, entity: LogoMarcaBovina) -> Dict[str, Any]:
        """Convierte entidad de dominio a representación JSON"""
        return {
            "id": entity.id,
            "marca_id": entity.marca_id,
            "url_logo": entity.url_logo,
            "fecha_generacion": entity.fecha_generacion,
            "exito": entity.exito,
            "tiempo_generacion_segundos": entity.tiempo_generacion_segundos,
            "modelo_ia_usado": entity.modelo_ia_usado.value,
            "modelo_ia_display": entity.modelo_ia_usado.display_name(),
            "prompt_usado": entity.prompt_usado,
            "calidad_logo": entity.calidad_logo.value,
            "calidad_logo_display": entity.calidad_logo.display_name(),
            "tiempo_generacion_formateado": self._formatear_tiempo(
                entity.tiempo_generacion_segundos
            ),
            # Campos de marca (se llenan desde el use case)
            "marca_numero": getattr(entity, "marca_numero", ""),
            "marca_productor": getattr(entity, "marca_productor", ""),
            "marca_raza": getattr(entity, "marca_raza", ""),
        }

    def _formatear_tiempo(self, segundos: int) -> str:
        """Formatea el tiempo de generación en formato legible"""
        if segundos < 60:
            return f"{segundos} segundos"
        else:
            minutos = segundos // 60
            seg_restantes = segundos % 60
            return f"{minutos}m {seg_restantes}s"

    def validate_tiempo_generacion_segundos(self, value: int) -> int:
        """Validación para tiempo de generación"""
        if value < 0:
            raise serializers.ValidationError(
                "El tiempo de generación no puede ser negativo"
            )
        if value > 3600:  # 1 hora máximo
            raise serializers.ValidationError(
                "El tiempo de generación no puede exceder 1 hora"
            )
        return value


class LogoMarcaBovinaListSerializer(serializers.Serializer):
    """Serializer simplificado para listados de logos"""

    id = serializers.IntegerField()
    marca_id = serializers.IntegerField()
    url_logo = serializers.CharField()
    fecha_generacion = serializers.DateTimeField()
    exito = serializers.BooleanField()
    modelo_ia_usado = serializers.CharField()
    modelo_ia_display = serializers.CharField()
    calidad_logo = serializers.CharField()
    calidad_logo_display = serializers.CharField()
    tiempo_generacion_formateado = serializers.CharField()

    def to_representation(self, entity: LogoMarcaBovina) -> Dict[str, Any]:
        """Convierte entidad a representación para listado"""
        return {
            "id": entity.id,
            "marca_id": entity.marca_id,
            "url_logo": entity.url_logo,
            "fecha_generacion": entity.fecha_generacion,
            "exito": entity.exito,
            "modelo_ia_usado": entity.modelo_ia_usado.value,
            "modelo_ia_display": entity.modelo_ia_usado.display_name(),
            "calidad_logo": entity.calidad_logo.value,
            "calidad_logo_display": entity.calidad_logo.display_name(),
            "tiempo_generacion_formateado": self._formatear_tiempo(
                entity.tiempo_generacion_segundos
            ),
        }

    def _formatear_tiempo(self, segundos: int) -> str:
        """Formatea el tiempo de generación en formato legible"""
        if segundos < 60:
            return f"{segundos} segundos"
        else:
            minutos = segundos // 60
            seg_restantes = segundos % 60
            return f"{minutos}m {seg_restantes}s"
