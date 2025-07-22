from typing import List, Optional

from apps.analytics.domain.entities.logo_marca_bovina import LogoMarcaBovina
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository
from apps.analytics.domain.enums import ModeloIA


class ListarLogosUseCase:
    """Use Case para listar logos con filtros"""

    def __init__(self, logo_repository: LogoMarcaBovinaRepository):
        self.logo_repository = logo_repository

    def execute(
        self,
        marca_id: Optional[int] = None,
        modelo_ia: Optional[ModeloIA] = None,
        exito: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[LogoMarcaBovina]:
        """
        Lista logos con filtros opcionales

        Args:
            marca_id: Filtrar por marca
            modelo_ia: Filtrar por modelo de IA
            exito: Filtrar por éxito de generación
            limit: Límite de resultados
            offset: Desplazamiento para paginación

        Returns:
            List[LogoMarcaBovina]: Lista de logos
        """
        return self.logo_repository.listar_con_filtros(
            marca_id=marca_id,
            modelo_ia=modelo_ia,
            exito=exito,
            limit=limit,
            offset=offset,
        )
