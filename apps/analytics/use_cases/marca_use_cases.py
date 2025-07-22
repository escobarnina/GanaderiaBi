# apps/analytics/use_cases/marca_use_cases.py
"""
Use Cases para gestión de marcas de ganado bovino
Responsabilidad: Orquestar operaciones de negocio relacionadas con marcas
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal

from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.enums import (
    EstadoMarca,
    RazaBovino,
    PropositoGanado,
    Departamento,
)


class CrearMarcaUseCase:
    """Use Case para crear una nueva marca de ganado bovino"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, data: Dict[str, Any]) -> MarcaGanadoBovino:
        """
        Crea una nueva marca de ganado bovino

        Args:
            data: Diccionario con los datos de la marca

        Returns:
            MarcaGanadoBovino: La marca creada

        Raises:
            ValueError: Si los datos son inválidos
        """
        # Validar datos requeridos
        if not data.get("numero_marca"):
            raise ValueError("El número de marca es requerido")

        if not data.get("nombre_productor"):
            raise ValueError("El nombre del productor es requerido")

        # Crear entidad de dominio
        marca = MarcaGanadoBovino(
            numero_marca=data["numero_marca"],
            nombre_productor=data["nombre_productor"],
            fecha_registro=data.get("fecha_registro", datetime.now()),
            estado=EstadoMarca(data.get("estado", EstadoMarca.PENDIENTE.value)),
            monto_certificacion=Decimal(str(data.get("monto_certificacion", 0))),
            raza_bovino=RazaBovino(data.get("raza_bovino", RazaBovino.CRIOLLO.value)),
            proposito_ganado=PropositoGanado(
                data.get("proposito_ganado", PropositoGanado.CARNE.value)
            ),
            cantidad_cabezas=data.get("cantidad_cabezas", 0),
            departamento=Departamento(
                data.get("departamento", Departamento.SANTA_CRUZ.value)
            ),
            municipio=data.get("municipio", ""),
            comunidad=data.get("comunidad"),
            ci_productor=data.get("ci_productor", ""),
            telefono_productor=data.get("telefono_productor"),
            observaciones=data.get("observaciones"),
            creado_por=data.get("creado_por"),
        )

        # Guardar usando repositorio
        return self.marca_repository.crear(marca)


class ObtenerMarcaUseCase:
    """Use Case para obtener una marca por ID"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, marca_id: int) -> Optional[MarcaGanadoBovino]:
        """
        Obtiene una marca por su ID

        Args:
            marca_id: ID de la marca

        Returns:
            MarcaGanadoBovino: La marca encontrada o None
        """
        return self.marca_repository.obtener_por_id(marca_id)


class ActualizarMarcaUseCase:
    """Use Case para actualizar una marca existente"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(
        self, marca_id: int, data: Dict[str, Any]
    ) -> Optional[MarcaGanadoBovino]:
        """
        Actualiza una marca existente

        Args:
            marca_id: ID de la marca a actualizar
            data: Datos a actualizar

        Returns:
            MarcaGanadoBovino: La marca actualizada o None si no existe
        """
        # Obtener marca existente
        marca = self.marca_repository.obtener_por_id(marca_id)
        if not marca:
            return None

        # Actualizar campos
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

        # Guardar cambios
        return self.marca_repository.actualizar(marca)


class EliminarMarcaUseCase:
    """Use Case para eliminar una marca"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, marca_id: int) -> bool:
        """
        Elimina una marca

        Args:
            marca_id: ID de la marca a eliminar

        Returns:
            bool: True si se eliminó correctamente
        """
        return self.marca_repository.eliminar(marca_id)


class ListarMarcasUseCase:
    """Use Case para listar marcas con filtros"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(
        self,
        estado: Optional[EstadoMarca] = None,
        departamento: Optional[Departamento] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[MarcaGanadoBovino]:
        """
        Lista marcas con filtros opcionales

        Args:
            estado: Filtrar por estado
            departamento: Filtrar por departamento
            limit: Límite de resultados
            offset: Desplazamiento para paginación

        Returns:
            List[MarcaGanadoBovino]: Lista de marcas
        """
        if estado:
            return self.marca_repository.listar_por_estado(estado)
        elif departamento:
            return self.marca_repository.listar_por_departamento(departamento)
        else:
            return self.marca_repository.listar_todas(limit=limit, offset=offset)


class CambiarEstadoMarcaUseCase:
    """Use Case para cambiar el estado de una marca"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(
        self,
        marca_id: int,
        nuevo_estado: EstadoMarca,
        usuario: Optional[str] = None,
        observaciones: Optional[str] = None,
    ) -> Optional[HistorialEstadoMarca]:
        """
        Cambia el estado de una marca y registra el historial

        Args:
            marca_id: ID de la marca
            nuevo_estado: Nuevo estado
            usuario: Usuario que realiza el cambio
            observaciones: Observaciones del cambio

        Returns:
            HistorialEstadoMarca: El registro de cambio o None si no existe la marca
        """
        # Obtener marca
        marca = self.marca_repository.obtener_por_id(marca_id)
        if not marca:
            return None

        # Cambiar estado y crear historial
        historial = marca.cambiar_estado(nuevo_estado, usuario)
        if observaciones:
            historial.observaciones_cambio = observaciones

        # Guardar marca actualizada
        self.marca_repository.actualizar(marca)

        # Registrar historial
        return self.marca_repository.registrar_cambio_estado(historial)


class ObtenerEstadisticasMarcasUseCase:
    """Use Case para obtener estadísticas de marcas"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de marcas

        Returns:
            Dict[str, Any]: Estadísticas de marcas
        """
        return self.marca_repository.obtener_estadisticas()
