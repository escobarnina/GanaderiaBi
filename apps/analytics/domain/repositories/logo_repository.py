# apps/analytics/domain/repositories/logo_repository.py
"""
Interfaz para repositorio de logos de marcas bovinas
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from ..entities.logo_marca_bovina import LogoMarcaBovina


class LogoMarcaBovinaRepository(ABC):
    """Interfaz para repositorio de logos de marcas bovinas"""

    @abstractmethod
    def get_by_id(self, logo_id: int) -> Optional[LogoMarcaBovina]:
        """Obtiene un logo por su ID"""
        pass

    @abstractmethod
    def get_by_marca_id(self, marca_id: int) -> List[LogoMarcaBovina]:
        """Obtiene logos por ID de marca"""
        pass

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[LogoMarcaBovina]:
        """Lista todos los logos con paginación"""
        pass

    @abstractmethod
    def list_exitosos(self) -> List[LogoMarcaBovina]:
        """Lista logos generados exitosamente"""
        pass

    @abstractmethod
    def list_fallidos(self) -> List[LogoMarcaBovina]:
        """Lista logos que fallaron en la generación"""
        pass

    @abstractmethod
    def save(self, logo: LogoMarcaBovina) -> LogoMarcaBovina:
        """Guarda un logo (crear o actualizar)"""
        pass

    @abstractmethod
    def delete(self, logo_id: int) -> bool:
        """Elimina un logo por ID"""
        pass

    @abstractmethod
    def get_estadisticas_generacion(self) -> Dict[str, Any]:
        """Obtiene estadísticas de generación de logos"""
        pass
