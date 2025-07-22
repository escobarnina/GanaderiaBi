# apps/analytics/domain/repositories/marca_repository.py
"""
Interfaz para repositorio de marcas de ganado bovino
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from ..entities.marca_ganado_bovino import MarcaGanadoBovino
from ..enums import EstadoMarca, RazaBovino, PropositoGanado, Departamento


class MarcaGanadoBovinoRepository(ABC):
    """Interfaz para repositorio de marcas de ganado bovino"""

    @abstractmethod
    def get_by_id(self, marca_id: int) -> Optional[MarcaGanadoBovino]:
        """Obtiene una marca por su ID"""
        pass

    @abstractmethod
    def get_by_numero_marca(self, numero_marca: str) -> Optional[MarcaGanadoBovino]:
        """Obtiene una marca por su número único"""
        pass

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[MarcaGanadoBovino]:
        """Lista todas las marcas con paginación"""
        pass

    @abstractmethod
    def list_by_estado(self, estado: EstadoMarca) -> List[MarcaGanadoBovino]:
        """Lista marcas por estado"""
        pass

    @abstractmethod
    def list_by_departamento(
        self, departamento: Departamento
    ) -> List[MarcaGanadoBovino]:
        """Lista marcas por departamento"""
        pass

    @abstractmethod
    def list_by_raza(self, raza: RazaBovino) -> List[MarcaGanadoBovino]:
        """Lista marcas por raza bovina"""
        pass

    @abstractmethod
    def list_by_proposito(self, proposito: PropositoGanado) -> List[MarcaGanadoBovino]:
        """Lista marcas por propósito ganadero"""
        pass

    @abstractmethod
    def list_pendientes(self) -> List[MarcaGanadoBovino]:
        """Lista marcas pendientes de procesamiento"""
        pass

    @abstractmethod
    def list_por_procesar(self) -> List[MarcaGanadoBovino]:
        """Lista marcas que están en proceso"""
        pass

    @abstractmethod
    def list_procesadas_hoy(self) -> List[MarcaGanadoBovino]:
        """Lista marcas procesadas hoy"""
        pass

    @abstractmethod
    def count_by_estado(self, estado: EstadoMarca) -> int:
        """Cuenta marcas por estado"""
        pass

    @abstractmethod
    def count_by_departamento(self, departamento: Departamento) -> int:
        """Cuenta marcas por departamento"""
        pass

    @abstractmethod
    def save(self, marca: MarcaGanadoBovino) -> MarcaGanadoBovino:
        """Guarda una marca (crear o actualizar)"""
        pass

    @abstractmethod
    def delete(self, marca_id: int) -> bool:
        """Elimina una marca por ID"""
        pass

    @abstractmethod
    def get_estadisticas_por_raza(self) -> Dict[str, Any]:
        """Obtiene estadísticas agrupadas por raza"""
        pass

    @abstractmethod
    def get_estadisticas_por_departamento(self) -> Dict[str, Any]:
        """Obtiene estadísticas agrupadas por departamento"""
        pass

    @abstractmethod
    def get_estadisticas_por_proposito(self) -> Dict[str, Any]:
        """Obtiene estadísticas agrupadas por propósito"""
        pass
