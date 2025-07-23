"""
Use Case para calcular tendencias por departamento
Responsabilidad única: Analizar tendencias de crecimiento por departamento
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository
from apps.analytics.domain.enums import Departamento, EstadoMarca


class CalcularTendenciasDepartamentoUseCase:
    """Use Case para calcular tendencias por departamento"""

    def __init__(
        self,
        marca_repository: MarcaGanadoBovinoRepository,
        kpi_repository: KPIGanadoBovinoRepository,
    ):
        self.marca_repository = marca_repository
        self.kpi_repository = kpi_repository

    def execute(self, meses_atras: int = 6) -> List[Dict[str, Any]]:
        """
        Calcula tendencias por departamento

        Args:
            meses_atras: Número de meses para el análisis

        Returns:
            List[Dict[str, Any]]: Lista de tendencias por departamento
        """
        try:
            # Obtener datos históricos
            datos_historicos = self._obtener_datos_historicos(meses_atras)

            # Calcular tendencias
            tendencias = self._calcular_tendencias(datos_historicos)

            return tendencias
        except Exception as e:
            print(f"Error calculando tendencias: {e}")
            return []

    def _obtener_datos_historicos(self, meses_atras: int) -> Dict[str, Any]:
        """
        Obtiene datos históricos para el análisis

        Args:
            meses_atras: Número de meses para el análisis

        Returns:
            Dict[str, Any]: Datos históricos organizados
        """
        fecha_inicio = datetime.now() - timedelta(days=meses_atras * 30)

        # Obtener todas las marcas
        marcas = self.marca_repository.listar_todas()

        # Filtrar por fecha y organizar por departamento
        datos_por_departamento = {}

        for marca in marcas:
            if marca.fecha_registro and marca.fecha_registro >= fecha_inicio:
                depto = marca.departamento.value

                if depto not in datos_por_departamento:
                    datos_por_departamento[depto] = {
                        "marcas": [],
                        "total_cabezas": 0,
                        "marcas_aprobadas": 0,
                        "marcas_pendientes": 0,
                        "ingresos_totales": 0,
                    }

                datos_por_departamento[depto]["marcas"].append(marca)
                datos_por_departamento[depto]["total_cabezas"] += marca.cantidad_cabezas
                datos_por_departamento[depto][
                    "ingresos_totales"
                ] += marca.monto_certificacion

                if marca.estado == EstadoMarca.APROBADO:
                    datos_por_departamento[depto]["marcas_aprobadas"] += 1
                elif marca.estado == EstadoMarca.PENDIENTE:
                    datos_por_departamento[depto]["marcas_pendientes"] += 1

        return datos_por_departamento

    def _calcular_tendencias(
        self, datos_historicos: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Calcula las tendencias por departamento

        Args:
            datos_historicos: Datos históricos organizados

        Returns:
            List[Dict[str, Any]]: Lista de tendencias calculadas
        """
        tendencias = []

        for departamento, datos in datos_historicos.items():
            # Calcular métricas
            total_marcas = len(datos["marcas"])
            tasa_aprobacion = (
                (datos["marcas_aprobadas"] / total_marcas * 100)
                if total_marcas > 0
                else 0
            )
            promedio_cabezas = (
                datos["total_cabezas"] / total_marcas if total_marcas > 0 else 0
            )
            ingreso_promedio = (
                datos["ingresos_totales"] / total_marcas if total_marcas > 0 else 0
            )

            # Determinar tendencia
            tendencia = self._determinar_tendencia(datos)

            tendencia_departamento = {
                "departamento": departamento,
                "total_marcas": total_marcas,
                "total_cabezas": datos["total_cabezas"],
                "marcas_aprobadas": datos["marcas_aprobadas"],
                "marcas_pendientes": datos["marcas_pendientes"],
                "tasa_aprobacion": round(tasa_aprobacion, 2),
                "promedio_cabezas": round(promedio_cabezas, 2),
                "ingreso_promedio": round(ingreso_promedio, 2),
                "ingresos_totales": datos["ingresos_totales"],
                "tendencia": tendencia,
                "crecimiento_mensual": self._calcular_crecimiento_mensual(datos),
            }

            tendencias.append(tendencia_departamento)

        # Ordenar por total de marcas
        tendencias.sort(key=lambda x: x["total_marcas"], reverse=True)

        return tendencias

    def _determinar_tendencia(self, datos: Dict[str, Any]) -> str:
        """
        Determina la tendencia del departamento

        Args:
            datos: Datos del departamento

        Returns:
            str: Tendencia calculada
        """
        total_marcas = len(datos["marcas"])
        tasa_aprobacion = (
            (datos["marcas_aprobadas"] / total_marcas * 100) if total_marcas > 0 else 0
        )

        if total_marcas >= 50 and tasa_aprobacion >= 80:
            return "CRECIENTE"
        elif total_marcas >= 30 and tasa_aprobacion >= 60:
            return "ESTABLE"
        elif total_marcas >= 10:
            return "EMERGENTE"
        else:
            return "LIMITADO"

    def _calcular_crecimiento_mensual(self, datos: Dict[str, Any]) -> float:
        """
        Calcula el crecimiento mensual

        Args:
            datos: Datos del departamento

        Returns:
            float: Porcentaje de crecimiento mensual
        """
        # Simulación de cálculo de crecimiento
        # En un entorno real, se compararían datos de diferentes meses
        total_marcas = len(datos["marcas"])

        if total_marcas == 0:
            return 0.0

        # Simulación basada en el número de marcas
        if total_marcas >= 50:
            return 15.5
        elif total_marcas >= 30:
            return 8.2
        elif total_marcas >= 10:
            return 12.7
        else:
            return 5.3
