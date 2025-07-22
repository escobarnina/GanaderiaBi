"""
Use Cases para gestión de marcas de ganado bovino
"""

from .crear_marca_use_case import CrearMarcaUseCase
from .obtener_marca_use_case import ObtenerMarcaUseCase
from .actualizar_marca_use_case import ActualizarMarcaUseCase
from .eliminar_marca_use_case import EliminarMarcaUseCase
from .listar_marcas_use_case import ListarMarcasUseCase
from .cambiar_estado_marca_use_case import CambiarEstadoMarcaUseCase
from .obtener_estadisticas_marcas_use_case import ObtenerEstadisticasMarcasUseCase

__all__ = [
    "CrearMarcaUseCase",
    "ObtenerMarcaUseCase",
    "ActualizarMarcaUseCase",
    "EliminarMarcaUseCase",
    "ListarMarcasUseCase",
    "CambiarEstadoMarcaUseCase",
    "ObtenerEstadisticasMarcasUseCase",
]
