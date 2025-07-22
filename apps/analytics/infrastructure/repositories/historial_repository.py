"""
Implementación de repositorio de historial usando Django ORM
Responsabilidad única: Gestionar historial de estados de marcas
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)

# Importar modelo Django de la nueva arquitectura
from apps.analytics.infrastructure.models import HistorialEstadoMarcaModel


class DjangoHistorialRepository(HistorialEstadoMarcaRepository):
    """Implementación de repositorio de historial usando Django ORM
    Responsabilidad única: Gestionar historial de estados de marcas"""

    def _to_entity(self, model: HistorialEstadoMarcaModel) -> HistorialEstadoMarca:
        """Conversión de modelo Django a entidad de dominio"""
        return HistorialEstadoMarca(
            id=model.id,
            marca_id=model.marca_id,
            estado_anterior=model.estado_anterior,
            estado_nuevo=model.estado_nuevo,
            fecha_cambio=model.fecha_cambio,
            usuario_responsable=model.usuario_responsable,
            observaciones_cambio=model.observaciones_cambio,
        )

    def _to_model(self, entity: HistorialEstadoMarca) -> HistorialEstadoMarcaModel:
        """Conversión de entidad de dominio a modelo Django"""
        model_data = {
            "marca_id": entity.marca_id,
            "estado_anterior": entity.estado_anterior,
            "estado_nuevo": entity.estado_nuevo,
            "fecha_cambio": entity.fecha_cambio,
            "usuario_responsable": entity.usuario_responsable,
            "observaciones_cambio": entity.observaciones_cambio,
        }

        if entity.id:
            model = HistorialEstadoMarcaModel.objects.get(id=entity.id)
            for key, value in model_data.items():
                setattr(model, key, value)
            return model
        else:
            return HistorialEstadoMarcaModel(**model_data)

    def crear(self, historial: HistorialEstadoMarca) -> HistorialEstadoMarca:
        """Implementa HistorialEstadoMarcaRepository.save (crear)"""
        model = self._to_model(historial)
        model.save()
        return self._to_entity(model)

    def obtener_por_id(self, historial_id: int) -> Optional[HistorialEstadoMarca]:
        """Implementa HistorialEstadoMarcaRepository.get_by_id"""
        try:
            model = HistorialEstadoMarcaModel.objects.get(id=historial_id)
            return self._to_entity(model)
        except HistorialEstadoMarcaModel.DoesNotExist:
            return None

    def obtener_por_marca(self, marca_id: int) -> List[HistorialEstadoMarca]:
        """Implementa HistorialEstadoMarcaRepository.get_by_marca_id"""
        models = HistorialEstadoMarcaModel.objects.filter(marca_id=marca_id).order_by(
            "-fecha_cambio"
        )
        return [self._to_entity(model) for model in models]

    def actualizar(self, historial: HistorialEstadoMarca) -> HistorialEstadoMarca:
        """Implementa HistorialEstadoMarcaRepository.save (actualizar)"""
        model = self._to_model(historial)
        model.save()
        return self._to_entity(model)

    def eliminar(self, historial_id: int) -> bool:
        """Implementa HistorialEstadoMarcaRepository.delete"""
        try:
            model = HistorialEstadoMarcaModel.objects.get(id=historial_id)
            model.delete()
            return True
        except HistorialEstadoMarcaModel.DoesNotExist:
            return False

    def listar_todos(
        self, limit: int = 100, offset: int = 0
    ) -> List[HistorialEstadoMarca]:
        """Implementa HistorialEstadoMarcaRepository.list_all"""
        models = HistorialEstadoMarcaModel.objects.all()[offset : offset + limit]
        return [self._to_entity(model) for model in models]

    def listar_por_estado(self, estado: str) -> List[HistorialEstadoMarca]:
        """Implementa método adicional para filtrar por estado"""
        models = HistorialEstadoMarcaModel.objects.filter(estado_nuevo=estado).order_by(
            "-fecha_cambio"
        )
        return [self._to_entity(model) for model in models]

    def listar_por_usuario(self, usuario: str) -> List[HistorialEstadoMarca]:
        """Implementa método adicional para filtrar por usuario"""
        models = HistorialEstadoMarcaModel.objects.filter(
            usuario_responsable=usuario
        ).order_by("-fecha_cambio")
        return [self._to_entity(model) for model in models]

    def listar_por_fecha(
        self, fecha_inicio: datetime, fecha_fin: datetime
    ) -> List[HistorialEstadoMarca]:
        """Implementa método adicional para filtrar por rango de fechas"""
        models = HistorialEstadoMarcaModel.objects.filter(
            fecha_cambio__gte=fecha_inicio, fecha_cambio__lte=fecha_fin
        ).order_by("-fecha_cambio")
        return [self._to_entity(model) for model in models]

    def obtener_ultimo_cambio(self, marca_id: int) -> Optional[HistorialEstadoMarca]:
        """Implementa método adicional para obtener último cambio"""
        try:
            model = HistorialEstadoMarcaModel.objects.filter(marca_id=marca_id).latest(
                "fecha_cambio"
            )
            return self._to_entity(model)
        except HistorialEstadoMarcaModel.DoesNotExist:
            return None

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Implementa método adicional para estadísticas del historial"""
        total_cambios = HistorialEstadoMarcaModel.objects.count()

        # Cambios por estado
        cambios_por_estado = HistorialEstadoMarcaModel.objects.values(
            "estado_nuevo"
        ).annotate(total=Count("id"))

        # Cambios por usuario
        cambios_por_usuario = (
            HistorialEstadoMarcaModel.objects.values("usuario_responsable")
            .annotate(total=Count("id"))
            .exclude(usuario_responsable__isnull=True)
        )

        # Cambios recientes (últimos 7 días)
        fecha_limite = timezone.now() - timedelta(days=7)
        cambios_recientes = HistorialEstadoMarcaModel.objects.filter(
            fecha_cambio__gte=fecha_limite
        ).count()

        return {
            "total_cambios": total_cambios,
            "cambios_recientes": cambios_recientes,
            "por_estado": {
                item["estado_nuevo"]: item["total"] for item in cambios_por_estado
            },
            "por_usuario": {
                item["usuario_responsable"]: item["total"]
                for item in cambios_por_usuario
            },
        }

    def obtener_tendencias_cambios(self, dias: int = 30) -> List[Dict[str, Any]]:
        """Implementa método adicional para tendencias de cambios"""
        fecha_limite = timezone.now() - timedelta(days=dias)

        tendencias = (
            HistorialEstadoMarcaModel.objects.filter(fecha_cambio__gte=fecha_limite)
            .annotate(fecha=TruncDate("fecha_cambio"))
            .values("fecha")
            .annotate(total_cambios=Count("id"))
            .order_by("fecha")
        )

        return [
            {
                "fecha": item["fecha"],
                "total_cambios": item["total_cambios"],
            }
            for item in tendencias
        ]
