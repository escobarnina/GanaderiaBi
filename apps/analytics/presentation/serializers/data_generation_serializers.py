"""
Serializers para Generación de Datos
Trabajan con entidades de dominio, no con modelos Django
"""

from rest_framework import serializers
from typing import Dict, Any, List


class GenerarDatosMockarooSerializer(serializers.Serializer):
    """Serializer para generación de datos Mockaroo"""

    mensaje = serializers.CharField()
    datos_generados = serializers.IntegerField()
    esquema_utilizado = serializers.ListField(child=serializers.CharField())
    ejemplo_datos = serializers.ListField()


class GenerarDescripcionMarcaSerializer(serializers.Serializer):
    """Serializer para generación de descripción de marca"""

    marca_id = serializers.IntegerField()
    descripcion_generada = serializers.CharField()
    longitud_descripcion = serializers.IntegerField()
    tipo_generacion = serializers.CharField()


class GenerarPromptsLogoSerializer(serializers.Serializer):
    """Serializer para generación de prompts de logo"""

    marca_id = serializers.IntegerField()
    prompts_generados = serializers.IntegerField()
    tipos_prompt = serializers.ListField(child=serializers.CharField())
    prompts = serializers.ListField(child=serializers.CharField())
