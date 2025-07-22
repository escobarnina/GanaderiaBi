from typing import Optional
from datetime import datetime

from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)
from apps.analytics.domain.enums import EstadoMarca


class CrearHistorialUseCase:
    """Use Case para crear un registro de historial"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(
        self,
        marca_id: int,
        estado_anterior: EstadoMarca,
        estado_nuevo: EstadoMarca,
        usuario_responsable: str,
        observaciones: Optional[str] = None,
    ) -> HistorialEstadoMarca:
        """
        Crea un registro de historial de cambio de estado

        Args:
            marca_id: ID de la marca
            estado_anterior: Estado anterior
            estado_nuevo: Estado nuevo
            usuario_responsable: Usuario que realiza el cambio
            observaciones: Observaciones del cambio

        Returns:
            HistorialEstadoMarca: El registro de historial creado
        """
        historial = HistorialEstadoMarca(
            marca_id=marca_id,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            fecha_cambio=datetime.now(),
            usuario_responsable=usuario_responsable,
            observaciones_cambio=observaciones,
        )

        return self.historial_repository.crear(historial)
