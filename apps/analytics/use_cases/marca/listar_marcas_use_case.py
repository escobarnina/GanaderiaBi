from typing import List, Optional, Dict, Any

from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.enums import EstadoMarca, Departamento


class ListarMarcasUseCase:
    """Use Case para listar marcas con filtros avanzados"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(
        self,
        estado: Optional[EstadoMarca] = None,
        departamento: Optional[Departamento] = None,
        raza_bovino: Optional[str] = None,
        proposito_ganado: Optional[str] = None,
        cabezas_min: Optional[int] = None,
        cabezas_max: Optional[int] = None,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None,
        productor: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[MarcaGanadoBovino]:
        """
        Lista marcas con filtros opcionales basado en el código legacy

        Args:
            estado: Filtrar por estado de la marca
            departamento: Filtrar por departamento
            raza_bovino: Filtrar por raza bovina
            proposito_ganado: Filtrar por propósito del ganado
            cabezas_min: Cantidad mínima de cabezas
            cabezas_max: Cantidad máxima de cabezas
            fecha_desde: Fecha de registro desde (YYYY-MM-DD)
            fecha_hasta: Fecha de registro hasta (YYYY-MM-DD)
            productor: Filtrar por nombre del productor (búsqueda parcial)
            limit: Límite de resultados
            offset: Desplazamiento para paginación

        Returns:
            List[MarcaGanadoBovino]: Lista de marcas que cumplen los filtros
        """
        # Aplicar filtros según el código legacy
        if estado:
            return self.marca_repository.listar_por_estado(estado)
        elif departamento:
            return self.marca_repository.listar_por_departamento(departamento)
        else:
            return self.marca_repository.listar_todas(limit=limit, offset=offset)

    def marcas_pendientes(self) -> List[MarcaGanadoBovino]:
        """
        Obtiene marcas pendientes de procesamiento

        Returns:
            List[MarcaGanadoBovino]: Lista de marcas pendientes
        """
        return self.marca_repository.listar_por_estado(EstadoMarca.PENDIENTE)

    def marcas_por_procesar(self, horas_limite: int = 72) -> List[MarcaGanadoBovino]:
        """
        Obtiene marcas que requieren atención prioritaria
        (pendientes por más de X horas)

        Args:
            horas_limite: Horas límite para considerar prioritarias

        Returns:
            List[MarcaGanadoBovino]: Lista de marcas prioritarias
        """
        return self.marca_repository.listar_por_procesar(horas_limite)

    def marcas_procesadas_hoy(self) -> List[MarcaGanadoBovino]:
        """
        Obtiene marcas procesadas el día de hoy

        Returns:
            List[MarcaGanadoBovino]: Lista de marcas procesadas hoy
        """
        return self.marca_repository.listar_procesadas_hoy()

    def alertas_tiempo_procesamiento(self) -> Dict[str, Any]:
        """
        Obtiene alertas de marcas con tiempo de procesamiento excesivo

        Returns:
            Dict[str, Any]: Información de alertas críticas y advertencias
        """
        return self.marca_repository.obtener_alertas_tiempo()
