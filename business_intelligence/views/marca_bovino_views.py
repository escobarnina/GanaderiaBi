# business_intelligence/views/marca_bovino_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from ..models import MarcaGanadoBovino, HistorialEstadoMarca
from ..serializers import (
    MarcaGanadoBovinoSerializer,
    MarcaGanadoBovinoListSerializer,
    EstadisticasPorRazaSerializer,
    EstadisticasPorDepartamentoSerializer,
)
from ..services import AnalyticsService, ReportService


class MarcaGanadoBovinoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión completa de marcas de ganado bovino

    Funcionalidades:
    - CRUD completo de marcas
    - Filtros avanzados
    - Acciones de aprobación/rechazo
    - Estadísticas por marca
    - Alertas de tiempo
    """

    queryset = MarcaGanadoBovino.objects.all()
    serializer_class = MarcaGanadoBovinoSerializer

    def get_serializer_class(self):
        """Usar serializer optimizado para listados"""
        if self.action == "list":
            return MarcaGanadoBovinoListSerializer
        return MarcaGanadoBovinoSerializer

    def get_queryset(self):
        """Queryset con filtros avanzados"""
        queryset = MarcaGanadoBovino.objects.select_related().prefetch_related(
            "logos", "historial_estados"
        )

        # Filtros por parámetros de query
        raza = self.request.query_params.get("raza_bovino")
        if raza:
            queryset = queryset.filter(raza_bovino=raza)

        proposito = self.request.query_params.get("proposito_ganado")
        if proposito:
            queryset = queryset.filter(proposito_ganado=proposito)

        departamento = self.request.query_params.get("departamento")
        if departamento:
            queryset = queryset.filter(departamento=departamento)

        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)

        # Filtro por rango de cabezas
        cabezas_min = self.request.query_params.get("cabezas_min")
        if cabezas_min:
            queryset = queryset.filter(cantidad_cabezas__gte=cabezas_min)

        cabezas_max = self.request.query_params.get("cabezas_max")
        if cabezas_max:
            queryset = queryset.filter(cantidad_cabezas__lte=cabezas_max)

        # Filtro por rango de fechas
        fecha_desde = self.request.query_params.get("fecha_desde")
        if fecha_desde:
            queryset = queryset.filter(fecha_registro__date__gte=fecha_desde)

        fecha_hasta = self.request.query_params.get("fecha_hasta")
        if fecha_hasta:
            queryset = queryset.filter(fecha_registro__date__lte=fecha_hasta)

        # Filtro por productor
        productor = self.request.query_params.get("productor")
        if productor:
            queryset = queryset.filter(nombre_productor__icontains=productor)

        # Ordenamiento
        ordering = self.request.query_params.get("ordering", "-fecha_registro")
        queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        """Crear marca con usuario responsable y historial inicial"""
        marca = serializer.save(
            creado_por=(
                self.request.user.username
                if self.request.user.is_authenticated
                else "anonimo"
            )
        )

        # Crear entrada inicial en historial
        HistorialEstadoMarca.objects.create(
            marca=marca,
            estado_anterior=None,
            estado_nuevo="PENDIENTE",
            usuario_responsable=(
                self.request.user.username
                if self.request.user.is_authenticated
                else "sistema"
            ),
            observaciones_cambio=f"Registro inicial de marca {marca.numero_marca}",
        )

    @action(detail=False, methods=["get"])
    def marcas_pendientes(self, request):
        """Obtiene marcas pendientes de procesamiento"""
        pendientes = self.get_queryset().filter(estado="PENDIENTE")

        # Agregar información de días transcurridos
        for marca in pendientes:
            marca.dias_pendiente = marca.dias_desde_registro

        serializer = self.get_serializer(pendientes, many=True)
        return Response(
            {
                "count": pendientes.count(),
                "results": serializer.data,
                "resumen": {
                    "total_cabezas": pendientes.aggregate(Sum("cantidad_cabezas"))[
                        "cantidad_cabezas__sum"
                    ]
                    or 0,
                    "promedio_dias_pendiente": pendientes.aggregate(
                        Avg("dias_desde_registro")
                    )["dias_desde_registro__avg"]
                    or 0,
                },
            }
        )

    @action(detail=False, methods=["get"])
    def marcas_por_procesar(self, request):
        """Marcas que requieren atención prioritaria"""
        # Marcas pendientes por más de 72 horas
        limite_tiempo = timezone.now() - timedelta(hours=72)

        por_procesar = (
            self.get_queryset()
            .filter(
                estado__in=["PENDIENTE", "EN_PROCESO"], fecha_registro__lt=limite_tiempo
            )
            .order_by("fecha_registro")
        )

        serializer = self.get_serializer(por_procesar, many=True)
        return Response(
            {
                "count": por_procesar.count(),
                "results": serializer.data,
                "mensaje": f"{por_procesar.count()} marcas requieren atención prioritaria",
            }
        )

    @action(detail=False, methods=["get"])
    def marcas_procesadas_hoy(self, request):
        """Marcas procesadas el día de hoy"""
        hoy = timezone.now().date()
        procesadas_hoy = (
            self.get_queryset()
            .filter(fecha_procesamiento__date=hoy)
            .order_by("-fecha_procesamiento")
        )

        serializer = self.get_serializer(procesadas_hoy, many=True)

        # Estadísticas del día
        aprobadas_hoy = procesadas_hoy.filter(estado="APROBADO").count()
        rechazadas_hoy = procesadas_hoy.filter(estado="RECHAZADO").count()

        return Response(
            {
                "fecha": hoy,
                "count": procesadas_hoy.count(),
                "results": serializer.data,
                "estadisticas_dia": {
                    "aprobadas": aprobadas_hoy,
                    "rechazadas": rechazadas_hoy,
                    "tasa_aprobacion": round(
                        (
                            (aprobadas_hoy / procesadas_hoy.count() * 100)
                            if procesadas_hoy.count() > 0
                            else 0
                        ),
                        2,
                    ),
                },
            }
        )

    @action(detail=False, methods=["get"])
    def alertas_tiempo_procesamiento(self, request):
        """Alertas de marcas con tiempo de procesamiento excesivo"""
        alertas = []

        # Marcas pendientes por más de 7 días
        limite_critico = timezone.now() - timedelta(days=7)
        limite_advertencia = timezone.now() - timedelta(days=3)

        criticas = (
            self.get_queryset()
            .filter(
                estado__in=["PENDIENTE", "EN_PROCESO"],
                fecha_registro__lt=limite_critico,
            )
            .count()
        )

        advertencias = (
            self.get_queryset()
            .filter(
                estado__in=["PENDIENTE", "EN_PROCESO"],
                fecha_registro__lt=limite_advertencia,
                fecha_registro__gte=limite_critico,
            )
            .count()
        )

        if criticas > 0:
            alertas.append(
                {
                    "tipo": "critica",
                    "cantidad": criticas,
                    "mensaje": f"{criticas} marcas pendientes por más de 7 días",
                    "color": "#f44336",
                }
            )

        if advertencias > 0:
            alertas.append(
                {
                    "tipo": "advertencia",
                    "cantidad": advertencias,
                    "mensaje": f"{advertencias} marcas pendientes por más de 3 días",
                    "color": "#ff9800",
                }
            )

        return Response(
            {
                "alertas": alertas,
                "total_alertas": len(alertas),
                "estado_sistema": (
                    "critico"
                    if criticas > 0
                    else "advertencia" if advertencias > 0 else "normal"
                ),
            }
        )

    @action(detail=True, methods=["post"])
    def aprobar_marca(self, request, pk=None):
        """Aprobar una marca específica"""
        marca = self.get_object()

        if marca.estado not in ["PENDIENTE", "EN_PROCESO"]:
            return Response(
                {"error": f"No se puede aprobar una marca en estado {marca.estado}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        estado_anterior = marca.estado
        marca.estado = "APROBADO"
        marca.fecha_procesamiento = timezone.now()

        # Calcular tiempo de procesamiento
        tiempo_horas = int(
            (marca.fecha_procesamiento - marca.fecha_registro).total_seconds() / 3600
        )
        marca.tiempo_procesamiento_horas = tiempo_horas

        marca.save()

        # Registrar en historial
        HistorialEstadoMarca.objects.create(
            marca=marca,
            estado_anterior=estado_anterior,
            estado_nuevo="APROBADO",
            usuario_responsable=(
                request.user.username if request.user.is_authenticated else "sistema"
            ),
            observaciones_cambio=request.data.get(
                "observaciones", f"Marca aprobada manualmente"
            ),
        )

        serializer = self.get_serializer(marca)
        return Response(
            {
                "mensaje": f"Marca {marca.numero_marca} aprobada exitosamente",
                "marca": serializer.data,
                "tiempo_procesamiento": f"{tiempo_horas} horas",
            }
        )

    @action(detail=True, methods=["post"])
    def rechazar_marca(self, request, pk=None):
        """Rechazar una marca específica"""
        marca = self.get_object()

        if marca.estado not in ["PENDIENTE", "EN_PROCESO"]:
            return Response(
                {"error": f"No se puede rechazar una marca en estado {marca.estado}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        motivo_rechazo = request.data.get("motivo", "No especificado")

        estado_anterior = marca.estado
        marca.estado = "RECHAZADO"
        marca.fecha_procesamiento = timezone.now()

        # Calcular tiempo de procesamiento
        tiempo_horas = int(
            (marca.fecha_procesamiento - marca.fecha_registro).total_seconds() / 3600
        )
        marca.tiempo_procesamiento_horas = tiempo_horas

        marca.save()

        # Registrar en historial
        HistorialEstadoMarca.objects.create(
            marca=marca,
            estado_anterior=estado_anterior,
            estado_nuevo="RECHAZADO",
            usuario_responsable=(
                request.user.username if request.user.is_authenticated else "sistema"
            ),
            observaciones_cambio=f"Marca rechazada. Motivo: {motivo_rechazo}",
        )

        serializer = self.get_serializer(marca)
        return Response(
            {
                "mensaje": f"Marca {marca.numero_marca} rechazada",
                "marca": serializer.data,
                "motivo": motivo_rechazo,
            }
        )

    @action(detail=True, methods=["get"])
    def ver_historial(self, request, pk=None):
        """Ver historial completo de cambios de una marca"""
        marca = self.get_object()
        historial = HistorialEstadoMarca.objects.filter(marca=marca).order_by(
            "-fecha_cambio"
        )

        from ..serializers import HistorialEstadoMarcaSerializer

        serializer = HistorialEstadoMarcaSerializer(historial, many=True)

        return Response(
            {
                "marca": marca.numero_marca,
                "productor": marca.nombre_productor,
                "estado_actual": marca.estado,
                "historial": serializer.data,
                "total_cambios": historial.count(),
            }
        )

    @action(detail=False, methods=["get"])
    def estadisticas_por_raza(self, request):
        """Estadísticas agrupadas por raza bovina"""
        stats = (
            MarcaGanadoBovino.objects.values("raza_bovino")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                promedio_cabezas=Avg("cantidad_cabezas"),
                monto_promedio=Avg("monto_certificacion"),
                tiempo_promedio_procesamiento=Avg("tiempo_procesamiento_horas"),
                aprobadas=Count("id", filter=Q(estado="APROBADO")),
                rechazadas=Count("id", filter=Q(estado="RECHAZADO")),
            )
            .order_by("-total_marcas")
        )

        # Calcular porcentaje de aprobación para cada raza
        for stat in stats:
            total_procesadas = stat["aprobadas"] + stat["rechazadas"]
            stat["porcentaje_aprobacion"] = round(
                (
                    (stat["aprobadas"] / total_procesadas * 100)
                    if total_procesadas > 0
                    else 0
                ),
                2,
            )
            # Agregar display name
            stat["raza_display"] = dict(
                MarcaGanadoBovino._meta.get_field("raza_bovino").choices
            ).get(stat["raza_bovino"], stat["raza_bovino"])

        serializer = EstadisticasPorRazaSerializer(stats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def estadisticas_por_departamento(self, request):
        """Estadísticas agrupadas por departamento"""
        stats = (
            MarcaGanadoBovino.objects.values("departamento")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                aprobadas=Count("id", filter=Q(estado="APROBADO")),
                rechazadas=Count("id", filter=Q(estado="RECHAZADO")),
                pendientes=Count(
                    "id", filter=Q(estado__in=["PENDIENTE", "EN_PROCESO"])
                ),
                ingresos_total=Sum("monto_certificacion", filter=Q(estado="APROBADO")),
                tiempo_promedio_procesamiento=Avg("tiempo_procesamiento_horas"),
            )
            .order_by("-total_cabezas")
        )

        # Agregar información adicional
        for stat in stats:
            # Propósito principal
            proposito_principal = (
                MarcaGanadoBovino.objects.filter(departamento=stat["departamento"])
                .values("proposito_ganado")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            stat["proposito_principal"] = (
                proposito_principal["proposito_ganado"] if proposito_principal else None
            )

            # Raza principal
            raza_principal = (
                MarcaGanadoBovino.objects.filter(departamento=stat["departamento"])
                .values("raza_bovino")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            stat["raza_principal"] = (
                raza_principal["raza_bovino"] if raza_principal else None
            )

            # Display name
            stat["departamento_display"] = dict(
                MarcaGanadoBovino._meta.get_field("departamento").choices
            ).get(stat["departamento"], stat["departamento"])

        serializer = EstadisticasPorDepartamentoSerializer(stats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def procesamiento_masivo(self, request):
        """Procesamiento masivo de marcas (aprobar/rechazar múltiples)"""
        accion = request.data.get("accion")  # 'aprobar' o 'rechazar'
        marca_ids = request.data.get("marca_ids", [])
        observaciones = request.data.get("observaciones", "")

        if accion not in ["aprobar", "rechazar"]:
            return Response(
                {"error": 'Acción debe ser "aprobar" o "rechazar"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not marca_ids:
            return Response(
                {"error": "Debe proporcionar al menos una marca"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        marcas = MarcaGanadoBovino.objects.filter(
            id__in=marca_ids, estado__in=["PENDIENTE", "EN_PROCESO"]
        )

        procesadas = []
        errores = []

        for marca in marcas:
            try:
                estado_anterior = marca.estado
                nuevo_estado = "APROBADO" if accion == "aprobar" else "RECHAZADO"

                marca.estado = nuevo_estado
                marca.fecha_procesamiento = timezone.now()

                # Calcular tiempo de procesamiento
                tiempo_horas = int(
                    (marca.fecha_procesamiento - marca.fecha_registro).total_seconds()
                    / 3600
                )
                marca.tiempo_procesamiento_horas = tiempo_horas
                marca.save()

                # Registrar en historial
                HistorialEstadoMarca.objects.create(
                    marca=marca,
                    estado_anterior=estado_anterior,
                    estado_nuevo=nuevo_estado,
                    usuario_responsable=(
                        request.user.username
                        if request.user.is_authenticated
                        else "sistema"
                    ),
                    observaciones_cambio=f"Procesamiento masivo: {accion}. {observaciones}",
                )

                procesadas.append(
                    {
                        "id": marca.id,
                        "numero_marca": marca.numero_marca,
                        "nuevo_estado": nuevo_estado,
                    }
                )

            except Exception as e:
                errores.append(
                    {
                        "id": marca.id,
                        "numero_marca": marca.numero_marca,
                        "error": str(e),
                    }
                )

        return Response(
            {
                "mensaje": f"{len(procesadas)} marcas procesadas exitosamente",
                "procesadas": procesadas,
                "errores": errores,
                "total_procesadas": len(procesadas),
                "total_errores": len(errores),
            }
        )
