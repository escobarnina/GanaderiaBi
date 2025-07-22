from typing import Optional, Dict, Any
from decimal import Decimal

from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.enums import (
    EstadoMarca,
    RazaBovino,
    PropositoGanado,
    Departamento,
)


class ActualizarMarcaUseCase:
    """Use Case para actualizar una marca existente"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(
        self, marca_id: int, data: Dict[str, Any]
    ) -> Optional[MarcaGanadoBovino]:
        """
        Actualiza una marca existente con los datos proporcionados

        Args:
            marca_id: ID de la marca a actualizar
            data: Diccionario con los campos a actualizar

        Returns:
            MarcaGanadoBovino: La marca actualizada o None si no existe
        """
        # Obtener marca existente
        marca = self.marca_repository.obtener_por_id(marca_id)
        if not marca:
            return None

        # Actualizar campos según los datos proporcionados
        if "nombre_productor" in data:
            marca.nombre_productor = data["nombre_productor"]

        if "estado" in data:
            marca.estado = EstadoMarca(data["estado"])

        if "monto_certificacion" in data:
            marca.monto_certificacion = Decimal(str(data["monto_certificacion"]))

        if "raza_bovino" in data:
            marca.raza_bovino = RazaBovino(data["raza_bovino"])

        if "proposito_ganado" in data:
            marca.proposito_ganado = PropositoGanado(data["proposito_ganado"])

        if "cantidad_cabezas" in data:
            marca.cantidad_cabezas = data["cantidad_cabezas"]

        if "departamento" in data:
            marca.departamento = Departamento(data["departamento"])

        if "municipio" in data:
            marca.municipio = data["municipio"]

        if "comunidad" in data:
            marca.comunidad = data["comunidad"]

        if "ci_productor" in data:
            marca.ci_productor = data["ci_productor"]

        if "telefono_productor" in data:
            marca.telefono_productor = data["telefono_productor"]

        if "observaciones" in data:
            marca.observaciones = data["observaciones"]

        if "fecha_procesamiento" in data:
            marca.fecha_procesamiento = data["fecha_procesamiento"]

        if "tiempo_procesamiento_horas" in data:
            marca.tiempo_procesamiento_horas = data["tiempo_procesamiento_horas"]

        # Guardar cambios usando el repositorio
        return self.marca_repository.actualizar(marca)
