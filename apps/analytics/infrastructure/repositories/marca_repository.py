"""
Implementación de repositorio de marcas usando Django ORM
Responsabilidad única: Gestionar marcas de ganado bovino
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone

from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.enums import (
    EstadoMarca,
    RazaBovino,
    PropositoGanado,
    Departamento,
)

# Importar modelo Django de la nueva arquitectura
from apps.analytics.infrastructure.models import (
    MarcaGanadoBovinoModel,
    HistorialEstadoMarcaModel,
)


class DjangoMarcaRepository(MarcaGanadoBovinoRepository):
    """Implementación de repositorio de marcas usando Django ORM
    Responsabilidad única: Gestionar marcas de ganado bovino"""

    def _to_entity(self, model: MarcaGanadoBovinoModel) -> MarcaGanadoBovino:
        """Convierte modelo Django a entidad de dominio"""
        return MarcaGanadoBovino(
            id=model.id,
            numero_marca=model.numero_marca,
            nombre_productor=model.nombre_productor,
            fecha_registro=model.fecha_registro,
            fecha_procesamiento=model.fecha_procesamiento,
            estado=EstadoMarca(model.estado),
            monto_certificacion=model.monto_certificacion,
            raza_bovino=RazaBovino(model.raza_bovino),
            proposito_ganado=PropositoGanado(model.proposito_ganado),
            cantidad_cabezas=model.cantidad_cabezas,
            departamento=Departamento(model.departamento),
            municipio=model.municipio,
            comunidad=model.comunidad,
            ci_productor=model.ci_productor,
            telefono_productor=model.telefono_productor,
            tiempo_procesamiento_horas=model.tiempo_procesamiento_horas,
            observaciones=model.observaciones,
            creado_por=model.creado_por,
            actualizado_en=model.actualizado_en,
        )

    def _to_model(self, entity: MarcaGanadoBovino) -> MarcaGanadoBovinoModel:
        """Convierte entidad de dominio a modelo Django"""
        model_data = {
            "numero_marca": entity.numero_marca,
            "nombre_productor": entity.nombre_productor,
            "fecha_registro": entity.fecha_registro,
            "fecha_procesamiento": entity.fecha_procesamiento,
            "estado": entity.estado.value,
            "monto_certificacion": entity.monto_certificacion,
            "raza_bovino": entity.raza_bovino.value,
            "proposito_ganado": entity.proposito_ganado.value,
            "cantidad_cabezas": entity.cantidad_cabezas,
            "departamento": entity.departamento.value,
            "municipio": entity.municipio,
            "comunidad": entity.comunidad,
            "ci_productor": entity.ci_productor,
            "telefono_productor": entity.telefono_productor,
            "tiempo_procesamiento_horas": entity.tiempo_procesamiento_horas,
            "observaciones": entity.observaciones,
            "creado_por": entity.creado_por,
        }

        if entity.id:
            model = MarcaGanadoBovinoModel.objects.get(id=entity.id)
            for key, value in model_data.items():
                setattr(model, key, value)
            return model
        else:
            return MarcaGanadoBovinoModel(**model_data)

    def _to_historial_entity(
        self, model: HistorialEstadoMarcaModel
    ) -> HistorialEstadoMarca:
        """Convierte modelo de historial Django a entidad de dominio"""
        return HistorialEstadoMarca(
            id=model.id,
            marca_id=model.marca_id,
            estado_anterior=model.estado_anterior,
            estado_nuevo=model.estado_nuevo,
            fecha_cambio=model.fecha_cambio,
            usuario_responsable=model.usuario_responsable,
            observaciones_cambio=model.observaciones_cambio,
        )

    def crear(self, marca: MarcaGanadoBovino) -> MarcaGanadoBovino:
        """Crea una nueva marca"""
        model = self._to_model(marca)
        model.save()
        return self._to_entity(model)

    def obtener_por_id(self, marca_id: int) -> Optional[MarcaGanadoBovino]:
        """Obtiene una marca por su ID"""
        try:
            model = MarcaGanadoBovinoModel.objects.get(id=marca_id)
            return self._to_entity(model)
        except MarcaGanadoBovinoModel.DoesNotExist:
            return None

    def obtener_por_numero(self, numero_marca: str) -> Optional[MarcaGanadoBovino]:
        """Obtiene una marca por su número"""
        try:
            model = MarcaGanadoBovinoModel.objects.get(numero_marca=numero_marca)
            return self._to_entity(model)
        except MarcaGanadoBovinoModel.DoesNotExist:
            return None

    def actualizar(self, marca: MarcaGanadoBovino) -> MarcaGanadoBovino:
        """Actualiza una marca existente"""
        model = self._to_model(marca)
        model.save()
        return self._to_entity(model)

    def eliminar(self, marca_id: int) -> bool:
        """Elimina una marca"""
        try:
            model = MarcaGanadoBovinoModel.objects.get(id=marca_id)
            model.delete()
            return True
        except MarcaGanadoBovinoModel.DoesNotExist:
            return False

    def listar_todas(
        self, limit: int = 100, offset: int = 0
    ) -> List[MarcaGanadoBovino]:
        """Lista todas las marcas con paginación"""
        models = MarcaGanadoBovinoModel.objects.all()[offset : offset + limit]
        return [self._to_entity(model) for model in models]

    def listar_por_estado(self, estado: EstadoMarca) -> List[MarcaGanadoBovino]:
        """Lista marcas por estado"""
        models = MarcaGanadoBovinoModel.objects.filter(estado=estado.value)
        return [self._to_entity(model) for model in models]

    def listar_por_departamento(
        self, departamento: Departamento
    ) -> List[MarcaGanadoBovino]:
        """Lista marcas por departamento"""
        models = MarcaGanadoBovinoModel.objects.filter(departamento=departamento.value)
        return [self._to_entity(model) for model in models]

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales"""
        from django.db.models import Count, Avg, Sum

        total_marcas = MarcaGanadoBovinoModel.objects.count()
        marcas_aprobadas = MarcaGanadoBovinoModel.objects.filter(
            estado=EstadoMarca.APROBADO.value
        ).count()
        marcas_pendientes = MarcaGanadoBovinoModel.objects.filter(
            estado=EstadoMarca.PENDIENTE.value
        ).count()

        # Estadísticas por propósito
        propositos = MarcaGanadoBovinoModel.objects.values("proposito_ganado").annotate(
            total=Count("id")
        )

        # Estadísticas por departamento
        departamentos = MarcaGanadoBovinoModel.objects.values("departamento").annotate(
            total=Count("id")
        )

        return {
            "total_marcas": total_marcas,
            "marcas_aprobadas": marcas_aprobadas,
            "marcas_pendientes": marcas_pendientes,
            "porcentaje_aprobacion": (
                (marcas_aprobadas / total_marcas * 100) if total_marcas > 0 else 0
            ),
            "propositos": {p["proposito_ganado"]: p["total"] for p in propositos},
            "departamentos": {d["departamento"]: d["total"] for d in departamentos},
        }

    def obtener_historial_estados(self, marca_id: int) -> List[HistorialEstadoMarca]:
        """Obtiene el historial de estados de una marca"""
        models = HistorialEstadoMarcaModel.objects.filter(marca_id=marca_id).order_by(
            "-fecha_cambio"
        )
        return [self._to_historial_entity(model) for model in models]

    def registrar_cambio_estado(
        self, historial: HistorialEstadoMarca
    ) -> HistorialEstadoMarca:
        """Registra un cambio de estado"""
        model = HistorialEstadoMarcaModel(
            marca_id=historial.marca_id,
            estado_anterior=historial.estado_anterior,
            estado_nuevo=historial.estado_nuevo,
            usuario_responsable=historial.usuario_responsable,
            observaciones_cambio=historial.observaciones_cambio,
        )
        model.save()
        return self._to_historial_entity(model)
