"""
Use Cases para gestión de historial de estados de marcas
"""

from .crear_historial_use_case import CrearHistorialUseCase
from .obtener_historial_use_case import ObtenerHistorialUseCase
from .listar_historial_marca_use_case import ListarHistorialMarcaUseCase
from .obtener_actividad_reciente_use_case import ObtenerActividadRecienteUseCase
from .obtener_auditoria_usuario_use_case import ObtenerAuditoriaUsuarioUseCase
from .obtener_patrones_cambio_use_case import ObtenerPatronesCambioUseCase
from .obtener_eficiencia_evaluadores_use_case import ObtenerEficienciaEvaluadoresUseCase

__all__ = [
    "CrearHistorialUseCase",
    "ObtenerHistorialUseCase",
    "ListarHistorialMarcaUseCase",
    "ObtenerActividadRecienteUseCase",
    "ObtenerAuditoriaUsuarioUseCase",
    "ObtenerPatronesCambioUseCase",
    "ObtenerEficienciaEvaluadoresUseCase",
]
