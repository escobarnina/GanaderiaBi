from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)


class EliminarMarcaUseCase:
    """Use Case para eliminar una marca"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, marca_id: int) -> bool:
        """
        Elimina una marca por su ID

        Args:
            marca_id: ID de la marca a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existe
        """
        return self.marca_repository.eliminar(marca_id)
