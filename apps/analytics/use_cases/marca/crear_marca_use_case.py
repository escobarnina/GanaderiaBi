from typing import Dict, Any
from datetime import datetime
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


class CrearMarcaUseCase:
    """Use Case para crear una nueva marca de ganado bovino"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, data: Dict[str, Any]) -> MarcaGanadoBovino:
        """
        Ejecuta la creación de una nueva marca de ganado bovino

        Args:
            data: Diccionario con los datos de la marca a crear
                - numero_marca (str, obligatorio): Número único de la marca
                - nombre_productor (str, obligatorio): Nombre del productor
                - cantidad_cabezas (int, opcional): Cantidad de cabezas (default: 0)
                - raza_bovino (str, opcional): Raza del ganado (default: CRIOLLO)
                - proposito_ganado (str, opcional): Propósito del ganado (default: CARNE)
                - departamento (str, opcional): Departamento (default: SANTA_CRUZ)
                - municipio (str, opcional): Municipio
                - comunidad (str, opcional): Comunidad
                - ci_productor (str, opcional): Cédula del productor
                - telefono_productor (str, opcional): Teléfono del productor
                - observaciones (str, opcional): Observaciones adicionales
                - creado_por (str, opcional): Usuario que crea la marca
                - monto_certificacion (Decimal, opcional): Monto de certificación (default: 0)

        Returns:
            MarcaGanadoBovino: La marca creada con ID asignado

        Raises:
            ValueError: Si los datos son inválidos según las reglas de negocio
            Exception: Si hay error en la persistencia o validación del repositorio
        """
        # Validar datos requeridos
        self._validar_datos_requeridos(data)

        # Validar datos opcionales
        self._validar_datos_opcionales(data)

        # Crear entidad de dominio con validaciones
        marca = self._crear_entidad_marca(data)

        # Persistir usando el repositorio
        marca_creada = self.marca_repository.crear(marca)

        return marca_creada

    def _validar_datos_requeridos(self, data: Dict[str, Any]) -> None:
        """
        Valida los datos requeridos para crear una marca

        Args:
            data: Datos a validar

        Raises:
            ValueError: Si algún dato requerido es inválido
        """
        if not data.get("numero_marca"):
            raise ValueError("El número de marca es requerido")

        if not data.get("nombre_productor"):
            raise ValueError("El nombre del productor es requerido")

        # Validar que el número de marca no esté duplicado
        marca_existente = self.marca_repository.obtener_por_numero(data["numero_marca"])
        if marca_existente:
            raise ValueError(
                f"Ya existe una marca con el número: {data['numero_marca']}"
            )

    def _validar_datos_opcionales(self, data: Dict[str, Any]) -> None:
        """
        Valida los datos opcionales de la marca

        Args:
            data: Datos a validar

        Raises:
            ValueError: Si algún dato opcional es inválido
        """
        # Validar cantidad de cabezas
        cantidad_cabezas = data.get("cantidad_cabezas", 0)
        if cantidad_cabezas < 0:
            raise ValueError("La cantidad de cabezas no puede ser negativa")

        # Validar cédula del productor
        ci_productor = data.get("ci_productor", "")
        if ci_productor and len(ci_productor) < 6:
            raise ValueError("La cédula de identidad debe tener al menos 6 caracteres")

        # Validar monto de certificación
        monto_certificacion = data.get("monto_certificacion", 0)
        if monto_certificacion < 0:
            raise ValueError("El monto de certificación no puede ser negativo")

    def _crear_entidad_marca(self, data: Dict[str, Any]) -> MarcaGanadoBovino:
        """
        Crea la entidad de dominio MarcaGanadoBovino

        Args:
            data: Datos para crear la entidad

        Returns:
            MarcaGanadoBovino: Entidad de dominio creada
        """
        return MarcaGanadoBovino(
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
