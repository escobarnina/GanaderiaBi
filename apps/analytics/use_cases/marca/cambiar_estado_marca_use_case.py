from typing import Optional, Dict, Any
from datetime import datetime

from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.enums import EstadoMarca


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
            marca_id: ID de la marca a cambiar
            nuevo_estado: Nuevo estado a asignar
            usuario: Usuario que realiza el cambio
            observaciones: Observaciones del cambio

        Returns:
            HistorialEstadoMarca: El registro de cambio o None si no existe la marca
        """
        # Obtener marca existente
        marca = self.marca_repository.obtener_por_id(marca_id)
        if not marca:
            return None

        # Validar que el cambio de estado sea válido
        if not self._es_cambio_estado_valido(marca.estado, nuevo_estado):
            raise ValueError(
                f"No se puede cambiar de {marca.estado.value} a {nuevo_estado.value}"
            )

        # Cambiar estado y crear historial
        historial = marca.cambiar_estado(nuevo_estado, usuario)
        if observaciones:
            historial.observaciones_cambio = observaciones

        # Actualizar fecha de procesamiento si es aprobado/rechazado
        if nuevo_estado in [EstadoMarca.APROBADO, EstadoMarca.RECHAZADO]:
            marca.fecha_procesamiento = datetime.now()
            # Calcular tiempo de procesamiento
            if marca.fecha_registro:
                tiempo_horas = int(
                    (marca.fecha_procesamiento - marca.fecha_registro).total_seconds()
                    / 3600
                )
                marca.tiempo_procesamiento_horas = tiempo_horas

        # Guardar marca actualizada
        self.marca_repository.actualizar(marca)

        # Registrar historial
        return self.marca_repository.registrar_cambio_estado(historial)

    def aprobar_marca(
        self,
        marca_id: int,
        usuario: Optional[str] = None,
        observaciones: Optional[str] = None,
    ) -> Optional[HistorialEstadoMarca]:
        """
        Aprueba una marca específica

        Args:
            marca_id: ID de la marca a aprobar
            usuario: Usuario que aprueba la marca
            observaciones: Observaciones de la aprobación

        Returns:
            HistorialEstadoMarca: El registro de aprobación
        """
        return self.execute(
            marca_id, EstadoMarca.APROBADO, usuario, observaciones or "Marca aprobada"
        )

    def rechazar_marca(
        self, marca_id: int, motivo: str, usuario: Optional[str] = None
    ) -> Optional[HistorialEstadoMarca]:
        """
        Rechaza una marca específica

        Args:
            marca_id: ID de la marca a rechazar
            motivo: Motivo del rechazo
            usuario: Usuario que rechaza la marca

        Returns:
            HistorialEstadoMarca: El registro de rechazo
        """
        observaciones = f"Marca rechazada. Motivo: {motivo}"
        return self.execute(marca_id, EstadoMarca.RECHAZADO, usuario, observaciones)

    def procesamiento_masivo(
        self,
        marca_ids: list,
        accion: str,
        usuario: Optional[str] = None,
        observaciones: str = "",
    ) -> Dict[str, Any]:
        """
        Procesamiento masivo de marcas (aprobar/rechazar múltiples)

        Args:
            marca_ids: Lista de IDs de marcas a procesar
            accion: 'aprobar' o 'rechazar'
            usuario: Usuario que realiza el procesamiento
            observaciones: Observaciones generales del procesamiento

        Returns:
            Dict[str, Any]: Resultado del procesamiento masivo
        """
        if accion not in ["aprobar", "rechazar"]:
            raise ValueError('Acción debe ser "aprobar" o "rechazar"')

        nuevo_estado = (
            EstadoMarca.APROBADO if accion == "aprobar" else EstadoMarca.RECHAZADO
        )
        procesadas = []
        errores = []

        for marca_id in marca_ids:
            try:
                historial = self.execute(
                    marca_id,
                    nuevo_estado,
                    usuario,
                    f"Procesamiento masivo: {accion}. {observaciones}",
                )
                if historial:
                    procesadas.append(
                        {
                            "id": marca_id,
                            "nuevo_estado": nuevo_estado.value,
                        }
                    )
            except Exception as e:
                errores.append(
                    {
                        "id": marca_id,
                        "error": str(e),
                    }
                )

        return {
            "procesadas": procesadas,
            "errores": errores,
            "total_procesadas": len(procesadas),
            "total_errores": len(errores),
        }

    def _es_cambio_estado_valido(
        self, estado_actual: EstadoMarca, nuevo_estado: EstadoMarca
    ) -> bool:
        """
        Valida si el cambio de estado es válido según las reglas de negocio

        Args:
            estado_actual: Estado actual de la marca
            nuevo_estado: Nuevo estado propuesto

        Returns:
            bool: True si el cambio es válido
        """
        # Reglas de transición de estados
        transiciones_validas = {
            EstadoMarca.PENDIENTE: [
                EstadoMarca.EN_PROCESO,
                EstadoMarca.APROBADO,
                EstadoMarca.RECHAZADO,
            ],
            EstadoMarca.EN_PROCESO: [EstadoMarca.APROBADO, EstadoMarca.RECHAZADO],
            EstadoMarca.APROBADO: [],  # No se puede cambiar desde aprobado
            EstadoMarca.RECHAZADO: [],  # No se puede cambiar desde rechazado
        }

        return nuevo_estado in transiciones_validas.get(estado_actual, [])
