# apps/analytics/domain/repositories/historial_repository.py
"""
Interfaz para repositorio de historial de estados
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.historial_estado_marca import HistorialEstadoMarca


class HistorialEstadoMarcaRepository(ABC):
    """Interfaz para repositorio de historial de estados"""

    @abstractmethod
    def get_by_id(self, historial_id: int) -> Optional[HistorialEstadoMarca]:
        """Obtiene un registro de historial por ID"""
        pass

    @abstractmethod
    def get_by_marca_id(self, marca_id: int) -> List[HistorialEstadoMarca]:
        """Obtiene historial por ID de marca"""
        pass

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[HistorialEstadoMarca]:
        """Lista todo el historial con paginación"""
        pass

    @abstractmethod
    def save(self, historial: HistorialEstadoMarca) -> HistorialEstadoMarca:
        """Guarda un registro de historial"""
        pass

    @abstractmethod
    def delete(self, historial_id: int) -> bool:
        """Elimina un registro de historial por ID"""
        pass
