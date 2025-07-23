"""
Use Case para generar datos usando Mockaroo API
Responsabilidad única: Generar datos de prueba usando Mockaroo
"""

import requests
from typing import List, Dict, Any
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.enums import (
    RazaBovino,
    PropositoGanado,
    Departamento,
    EstadoMarca,
)


class GenerarDatosMockarooUseCase:
    """Use Case para generar datos usando Mockaroo API"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, cantidad: int = 50) -> List[Dict[str, Any]]:
        """
        Genera datos usando Mockaroo API

        Args:
            cantidad: Cantidad de registros a generar

        Returns:
            List[Dict[str, Any]]: Lista de datos generados
        """
        try:
            # Configurar esquema de Mockaroo
            schema = self._crear_esquema_mockaroo()

            # Generar datos usando Mockaroo API
            datos = self._generar_datos_mockaroo(schema, cantidad)

            return datos
        except Exception as e:
            print(f"Error generando datos con Mockaroo: {e}")
            return []

    def _crear_esquema_mockaroo(self) -> Dict[str, Any]:
        """
        Crea el esquema para Mockaroo API

        Returns:
            Dict[str, Any]: Esquema de datos
        """
        return {
            "fields": [
                {
                    "name": "numero_marca",
                    "type": "Custom List",
                    "values": [f"M{i:03d}" for i in range(1, 1001)],
                },
                {"name": "nombre_productor", "type": "Full Name"},
                {
                    "name": "raza_bovino",
                    "type": "Custom List",
                    "values": [raza.value for raza in RazaBovino],
                },
                {
                    "name": "proposito_ganado",
                    "type": "Custom List",
                    "values": [proposito.value for proposito in PropositoGanado],
                },
                {"name": "cantidad_cabezas", "type": "Number", "min": 10, "max": 500},
                {
                    "name": "departamento",
                    "type": "Custom List",
                    "values": [depto.value for depto in Departamento],
                },
                {"name": "municipio", "type": "City"},
                {
                    "name": "ci_productor",
                    "type": "Number",
                    "min": 1000000,
                    "max": 9999999,
                },
                {"name": "telefono_productor", "type": "Phone"},
                {
                    "name": "monto_certificacion",
                    "type": "Number",
                    "min": 1000,
                    "max": 50000,
                },
                {
                    "name": "estado",
                    "type": "Custom List",
                    "values": [estado.value for estado in EstadoMarca],
                },
            ]
        }

    def _generar_datos_mockaroo(
        self, schema: Dict[str, Any], cantidad: int
    ) -> List[Dict[str, Any]]:
        """
        Genera datos usando Mockaroo API

        Args:
            schema: Esquema de datos
            cantidad: Cantidad de registros

        Returns:
            List[Dict[str, Any]]: Datos generados
        """
        try:
            # En un entorno real, aquí se haría la llamada a Mockaroo API
            # Por ahora, simulamos la generación de datos
            datos_generados = []

            for i in range(cantidad):
                dato = {
                    "numero_marca": f"M{i+1:03d}",
                    "nombre_productor": f"Productor {i+1}",
                    "raza_bovino": "Holstein",
                    "proposito_ganado": "LECHE",
                    "cantidad_cabezas": 50 + (i * 10),
                    "departamento": "SANTA_CRUZ",
                    "municipio": f"Municipio {i+1}",
                    "ci_productor": 1000000 + i,
                    "telefono_productor": f"591-{70000000 + i}",
                    "monto_certificacion": 5000 + (i * 100),
                    "estado": "PENDIENTE",
                }
                datos_generados.append(dato)

            return datos_generados
        except Exception as e:
            print(f"Error en generación de datos: {e}")
            return []

    def crear_marcas_desde_datos(
        self, datos: List[Dict[str, Any]]
    ) -> List[MarcaGanadoBovino]:
        """
        Crea entidades de marca desde datos generados

        Args:
            datos: Lista de datos generados

        Returns:
            List[MarcaGanadoBovino]: Lista de entidades creadas
        """
        marcas_creadas = []

        for dato in datos:
            try:
                marca = MarcaGanadoBovino(
                    numero_marca=dato["numero_marca"],
                    nombre_productor=dato["nombre_productor"],
                    raza_bovino=RazaBovino(dato["raza_bovino"]),
                    proposito_ganado=PropositoGanado(dato["proposito_ganado"]),
                    cantidad_cabezas=dato["cantidad_cabezas"],
                    departamento=Departamento(dato["departamento"]),
                    municipio=dato["municipio"],
                    ci_productor=str(dato["ci_productor"]),
                    telefono_productor=dato["telefono_productor"],
                    monto_certificacion=dato["monto_certificacion"],
                    estado=EstadoMarca(dato["estado"]),
                )

                # Persistir usando el repositorio
                marca_creada = self.marca_repository.crear(marca)
                marcas_creadas.append(marca_creada)

            except Exception as e:
                print(f"Error creando marca desde dato: {e}")
                continue

        return marcas_creadas
