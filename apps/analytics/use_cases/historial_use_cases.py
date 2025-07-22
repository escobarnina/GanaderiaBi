# apps/analytics/use_cases/historial_use_cases.py
"""
Use Cases para gestión de historial de estados de marcas
Responsabilidad: Orquestar operaciones de negocio relacionadas con historial
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta

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


class ObtenerHistorialUseCase:
    """Use Case para obtener historial por ID"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self, historial_id: int) -> Optional[HistorialEstadoMarca]:
        """
        Obtiene un registro de historial por su ID

        Args:
            historial_id: ID del registro de historial

        Returns:
            HistorialEstadoMarca: El registro encontrado o None
        """
        return self.historial_repository.obtener_por_id(historial_id)


class ListarHistorialMarcaUseCase:
    """Use Case para listar historial de una marca"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self, marca_id: int) -> List[HistorialEstadoMarca]:
        """
        Lista el historial de cambios de una marca

        Args:
            marca_id: ID de la marca

        Returns:
            List[HistorialEstadoMarca]: Lista de registros de historial
        """
        return self.historial_repository.obtener_por_marca(marca_id)


class ObtenerActividadRecienteUseCase:
    """Use Case para obtener actividad reciente del sistema"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self, dias: int = 7) -> List[HistorialEstadoMarca]:
        """
        Obtiene la actividad reciente del sistema

        Args:
            dias: Número de días hacia atrás para buscar

        Returns:
            List[HistorialEstadoMarca]: Lista de actividad reciente
        """
        return self.historial_repository.listar_por_fecha(
            fecha_inicio=datetime.now() - timedelta(days=dias),
            fecha_fin=datetime.now(),
        )


class ObtenerAuditoriaUsuarioUseCase:
    """Use Case para obtener auditoría de un usuario"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self, usuario: str, dias: int = 30) -> List[HistorialEstadoMarca]:
        """
        Obtiene la auditoría de cambios de un usuario

        Args:
            usuario: Nombre del usuario
            dias: Número de días hacia atrás para buscar

        Returns:
            List[HistorialEstadoMarca]: Lista de cambios del usuario
        """
        return self.historial_repository.listar_por_usuario(usuario)


class ObtenerPatronesCambioUseCase:
    """Use Case para obtener patrones de cambio de estado"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self) -> Dict[str, Any]:
        """
        Obtiene patrones de cambio de estado

        Returns:
            Dict[str, Any]: Patrones de cambio identificados
        """
        return self.historial_repository.obtener_estadisticas()


class ObtenerEficienciaEvaluadoresUseCase:
    """Use Case para obtener eficiencia de evaluadores"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self) -> Dict[str, Any]:
        """
        Obtiene métricas de eficiencia de evaluadores

        Returns:
            Dict[str, Any]: Métricas de eficiencia
        """
        return self.historial_repository.obtener_tendencias_cambios()
