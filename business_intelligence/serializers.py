# business_intelligence/serializers.py
from rest_framework import serializers
from django.db.models import Count, Avg, Sum, Q
from datetime import datetime, timedelta
from .models import (
    MarcaGanadoBovino,
    LogoMarcaBovina,
    KPIGanadoBovino,
    HistorialEstadoMarca,
)


class MarcaGanadoBovinoSerializer(serializers.ModelSerializer):
    """Serializer principal para marcas de ganado bovino"""

    # Campos calculados
    dias_desde_registro = serializers.ReadOnlyField()
    esta_procesado = serializers.ReadOnlyField()

    # Campos con display names
    raza_bovino_display = serializers.CharField(
        source="get_raza_bovino_display", read_only=True
    )
    proposito_ganado_display = serializers.CharField(
        source="get_proposito_ganado_display", read_only=True
    )
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    departamento_display = serializers.CharField(
        source="get_departamento_display", read_only=True
    )

    # Información adicional
    total_logos = serializers.SerializerMethodField()
    logos_exitosos = serializers.SerializerMethodField()

    class Meta:
        model = MarcaGanadoBovino
        fields = "__all__"
        read_only_fields = (
            "fecha_registro",
            "actualizado_en",
            "tiempo_procesamiento_horas",
            "dias_desde_registro",
            "esta_procesado",
        )

    def get_total_logos(self, obj):
        """Retorna el total de logos generados para esta marca"""
        return obj.logos.count()

    def get_logos_exitosos(self, obj):
        """Retorna el número de logos exitosos para esta marca"""
        return obj.logos.filter(exito=True).count()

    def validate_cantidad_cabezas(self, value):
        """Validación personalizada para cantidad de cabezas"""
        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad de cabezas debe ser mayor a 0"
            )
        if value > 10000:
            raise serializers.ValidationError(
                "La cantidad de cabezas no puede exceder 10,000"
            )
        return value

    def validate_ci_productor(self, value):
        """Validación para cédula de identidad"""
        if value and len(value) < 6:
            raise serializers.ValidationError(
                "La cédula de identidad debe tener al menos 6 caracteres"
            )
        return value

    def validate(self, data):
        """Validaciones a nivel de objeto"""
        if data.get("fecha_procesamiento") and data.get("fecha_registro"):
            if data["fecha_procesamiento"] < data["fecha_registro"]:
                raise serializers.ValidationError(
                    "La fecha de procesamiento no puede ser anterior a la fecha de registro"
                )
        return data


class MarcaGanadoBovinoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados"""

    raza_bovino_display = serializers.CharField(
        source="get_raza_bovino_display", read_only=True
    )
    proposito_ganado_display = serializers.CharField(
        source="get_proposito_ganado_display", read_only=True
    )
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    departamento_display = serializers.CharField(
        source="get_departamento_display", read_only=True
    )
    dias_desde_registro = serializers.ReadOnlyField()
    total_logos = serializers.SerializerMethodField()

    class Meta:
        model = MarcaGanadoBovino
        fields = [
            "id",
            "numero_marca",
            "nombre_productor",
            "raza_bovino",
            "raza_bovino_display",
            "proposito_ganado",
            "proposito_ganado_display",
            "cantidad_cabezas",
            "departamento",
            "departamento_display",
            "municipio",
            "estado",
            "estado_display",
            "monto_certificacion",
            "fecha_registro",
            "dias_desde_registro",
            "total_logos",
        ]

    def get_total_logos(self, obj):
        return obj.logos.count()


class LogoMarcaBovinaSerializer(serializers.ModelSerializer):
    """Serializer para logos de marcas bovinas"""

    # Información de la marca relacionada
    marca_numero = serializers.CharField(source="marca.numero_marca", read_only=True)
    marca_productor = serializers.CharField(
        source="marca.nombre_productor", read_only=True
    )
    marca_raza = serializers.CharField(
        source="marca.get_raza_bovino_display", read_only=True
    )

    # Campos con display names
    modelo_ia_display = serializers.CharField(
        source="get_modelo_ia_usado_display", read_only=True
    )
    calidad_logo_display = serializers.CharField(
        source="get_calidad_logo_display", read_only=True
    )

    # Campos calculados
    tiempo_generacion_formateado = serializers.SerializerMethodField()

    class Meta:
        model = LogoMarcaBovina
        fields = "__all__"
        read_only_fields = ("fecha_generacion",)

    def get_tiempo_generacion_formateado(self, obj):
        """Retorna el tiempo de generación en formato legible"""
        segundos = obj.tiempo_generacion_segundos
        if segundos < 60:
            return f"{segundos} segundos"
        else:
            minutos = segundos // 60
            seg_restantes = segundos % 60
            return f"{minutos}m {seg_restantes}s"

    def validate_tiempo_generacion_segundos(self, value):
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


class KPIGanadoBovinoSerializer(serializers.ModelSerializer):
    """Serializer para KPIs de ganado bovino"""

    # Campos calculados adicionales
    eficiencia_aprobacion = serializers.SerializerMethodField()
    eficiencia_tiempo = serializers.SerializerMethodField()
    eficiencia_logos = serializers.SerializerMethodField()
    distribucion_proposito = serializers.SerializerMethodField()
    distribucion_geografica = serializers.SerializerMethodField()
    tendencia_mensual = serializers.SerializerMethodField()

    class Meta:
        model = KPIGanadoBovino
        fields = "__all__"
        read_only_fields = "__all__"  # Los KPIs son solo lectura

    def get_eficiencia_aprobacion(self, obj):
        """Califica la eficiencia de aprobación"""
        if obj.porcentaje_aprobacion >= 80:
            return {"nivel": "alta", "color": "#4caf50", "descripcion": "Excelente"}
        elif obj.porcentaje_aprobacion >= 60:
            return {"nivel": "media", "color": "#ff9800", "descripcion": "Aceptable"}
        else:
            return {
                "nivel": "baja",
                "color": "#f44336",
                "descripcion": "Requiere atención",
            }

    def get_eficiencia_tiempo(self, obj):
        """Califica la eficiencia de tiempo de procesamiento"""
        if obj.tiempo_promedio_procesamiento <= 24:
            return {"nivel": "alta", "color": "#4caf50", "descripcion": "Rápido"}
        elif obj.tiempo_promedio_procesamiento <= 72:
            return {"nivel": "media", "color": "#ff9800", "descripcion": "Normal"}
        else:
            return {"nivel": "baja", "color": "#f44336", "descripcion": "Lento"}

    def get_eficiencia_logos(self, obj):
        """Califica la eficiencia de generación de logos"""
        if obj.tasa_exito_logos >= 85:
            return {"nivel": "alta", "color": "#4caf50", "descripcion": "Óptima"}
        elif obj.tasa_exito_logos >= 70:
            return {"nivel": "media", "color": "#ff9800", "descripcion": "Aceptable"}
        else:
            return {"nivel": "baja", "color": "#f44336", "descripcion": "Problemática"}

    def get_distribucion_proposito(self, obj):
        """Retorna la distribución porcentual por propósito"""
        total = (
            obj.marcas_carne
            + obj.marcas_leche
            + obj.marcas_doble_proposito
            + obj.marcas_reproduccion
        )

        if total == 0:
            return {"carne": 0, "leche": 0, "doble_proposito": 0, "reproduccion": 0}

        return {
            "carne": round((obj.marcas_carne / total) * 100, 1),
            "leche": round((obj.marcas_leche / total) * 100, 1),
            "doble_proposito": round((obj.marcas_doble_proposito / total) * 100, 1),
            "reproduccion": round((obj.marcas_reproduccion / total) * 100, 1),
        }

    def get_distribucion_geografica(self, obj):
        """Retorna la distribución porcentual por departamento"""
        total = (
            obj.marcas_santa_cruz
            + obj.marcas_beni
            + obj.marcas_la_paz
            + obj.marcas_otros_departamentos
        )

        if total == 0:
            return {"santa_cruz": 0, "beni": 0, "la_paz": 0, "otros": 0}

        return {
            "santa_cruz": round((obj.marcas_santa_cruz / total) * 100, 1),
            "beni": round((obj.marcas_beni / total) * 100, 1),
            "la_paz": round((obj.marcas_la_paz / total) * 100, 1),
            "otros": round((obj.marcas_otros_departamentos / total) * 100, 1),
        }

    def get_tendencia_mensual(self, obj):
        """Calcula la tendencia respecto al mes anterior"""
        try:
            mes_anterior = (
                KPIGanadoBovino.objects.filter(fecha__lt=obj.fecha)
                .order_by("-fecha")
                .first()
            )

            if not mes_anterior:
                return {"disponible": False}

            cambio_marcas = (
                obj.marcas_registradas_mes - mes_anterior.marcas_registradas_mes
            )
            cambio_ingresos = float(obj.ingresos_mes - mes_anterior.ingresos_mes)

            return {
                "disponible": True,
                "cambio_marcas": cambio_marcas,
                "cambio_ingresos": cambio_ingresos,
                "tendencia_marcas": (
                    "subida"
                    if cambio_marcas > 0
                    else "bajada" if cambio_marcas < 0 else "estable"
                ),
                "tendencia_ingresos": (
                    "subida"
                    if cambio_ingresos > 0
                    else "bajada" if cambio_ingresos < 0 else "estable"
                ),
            }
        except:
            return {"disponible": False}


class HistorialEstadoMarcaSerializer(serializers.ModelSerializer):
    """Serializer para historial de estados"""

    marca_numero = serializers.CharField(source="marca.numero_marca", read_only=True)
    marca_productor = serializers.CharField(
        source="marca.nombre_productor", read_only=True
    )
    tiempo_transcurrido = serializers.SerializerMethodField()

    class Meta:
        model = HistorialEstadoMarca
        fields = "__all__"
        read_only_fields = "__all__"  # El historial es solo lectura

    def get_tiempo_transcurrido(self, obj):
        """Retorna el tiempo transcurrido desde el cambio"""
        now = datetime.now().replace(tzinfo=obj.fecha_cambio.tzinfo)
        delta = now - obj.fecha_cambio

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
