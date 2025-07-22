from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from decimal import Decimal

from apps.analytics.domain.entities.dashboard_data import DashboardData
from apps.analytics.domain.repositories.dashboard_repository import DashboardRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository
from apps.analytics.domain.enums import EstadoMarca, PropositoGanado, Departamento


class ObtenerDashboardDataUseCase:
    """Use Case para obtener datos del dashboard"""

    def __init__(
        self,
        dashboard_repository: DashboardRepository,
        marca_repository: MarcaGanadoBovinoRepository,
        kpi_repository: KPIGanadoBovinoRepository,
        logo_repository: LogoMarcaBovinaRepository,
    ):
        self.dashboard_repository = dashboard_repository
        self.marca_repository = marca_repository
        self.kpi_repository = kpi_repository
        self.logo_repository = logo_repository

    def execute(self, fecha: date = None) -> DashboardData:
        """
        Obtiene datos completos del dashboard

        Args:
            fecha: Fecha para obtener datos (por defecto hoy)

        Returns:
            DashboardData: Datos del dashboard
        """
        if fecha is None:
            fecha = date.today()

        # Obtener estadísticas de marcas
        stats_marcas = self.marca_repository.obtener_estadisticas()

        # Obtener KPIs más recientes
        kpis_recientes = self.kpi_repository.listar_por_fechas(
            fecha_inicio=fecha - timedelta(days=30), fecha_fin=fecha, limit=1
        )

        kpi_actual = kpis_recientes[0] if kpis_recientes else None

        # Obtener estadísticas de logos
        stats_logos = self.logo_repository.obtener_estadisticas()

        # Calcular métricas del dashboard
        marcas_mes_actual = stats_marcas.get("total_marcas", 0)
        marcas_pendientes = stats_marcas.get("marcas_pendientes", 0)
        porcentaje_aprobacion = stats_marcas.get("porcentaje_aprobacion", 0)
        porcentaje_rechazo = 100 - porcentaje_aprobacion

        # KPIs específicos bovinos
        total_cabezas = kpi_actual.total_cabezas_registradas if kpi_actual else 0
        promedio_cabezas = kpi_actual.promedio_cabezas_por_marca if kpi_actual else 0

        # Distribución por propósito
        propositos = stats_marcas.get("propositos", {})
        total_propositos = sum(propositos.values()) if propositos else 1

        porcentaje_carne = (
            propositos.get(PropositoGanado.CARNE.value, 0) / total_propositos
        ) * 100
        porcentaje_leche = (
            propositos.get(PropositoGanado.LECHE.value, 0) / total_propositos
        ) * 100
        porcentaje_doble_proposito = (
            propositos.get(PropositoGanado.DOBLE_PROPOSITO.value, 0) / total_propositos
        ) * 100
        porcentaje_reproduccion = (
            propositos.get(PropositoGanado.REPRODUCCION.value, 0) / total_propositos
        ) * 100

        # Raza más común
        raza_mas_comun = self._obtener_raza_mas_comun()
        porcentaje_raza_principal = self._calcular_porcentaje_raza_principal(
            raza_mas_comun
        )

        # KPIs de logos
        tasa_exito_logos = stats_logos.get("tasa_exito", 0)
        total_marcas_sistema = stats_marcas.get("total_marcas", 0)

        # Calcular ingresos
        ingresos_mes_actual = kpi_actual.ingresos_mes if kpi_actual else Decimal("0")

        # Crear entidad de dominio
        dashboard_data = DashboardData(
            fecha_actualizacion=datetime.now(),
            marcas_registradas_mes_actual=marcas_mes_actual,
            tiempo_promedio_procesamiento=(
                kpi_actual.tiempo_promedio_procesamiento if kpi_actual else 0
            ),
            porcentaje_aprobacion=porcentaje_aprobacion,
            porcentaje_rechazo=porcentaje_rechazo,
            ingresos_mes_actual=ingresos_mes_actual,
            total_cabezas_bovinas=total_cabezas,
            promedio_cabezas_por_marca=promedio_cabezas,
            porcentaje_carne=porcentaje_carne,
            porcentaje_leche=porcentaje_leche,
            porcentaje_doble_proposito=porcentaje_doble_proposito,
            porcentaje_reproduccion=porcentaje_reproduccion,
            raza_mas_comun=raza_mas_comun,
            porcentaje_raza_principal=porcentaje_raza_principal,
            tasa_exito_logos=tasa_exito_logos,
            total_marcas_sistema=total_marcas_sistema,
            marcas_pendientes=marcas_pendientes,
            alertas=self._generar_alertas(stats_marcas, stats_logos),
        )

        # Guardar usando repositorio
        return self.dashboard_repository.guardar_dashboard_data(dashboard_data)

    def _obtener_raza_mas_comun(self) -> str:
        """Obtiene la raza más común"""
        return "CRIOLLO"

    def _calcular_porcentaje_raza_principal(self, raza: str) -> float:
        """Calcula el porcentaje de la raza principal"""
        return 45.5

    def _generar_alertas(self, stats_marcas: Dict, stats_logos: Dict) -> List[Dict]:
        """Genera alertas basadas en las estadísticas"""
        alertas = []

        # Alerta por marcas pendientes
        marcas_pendientes = stats_marcas.get("marcas_pendientes", 0)
        if marcas_pendientes > 50:
            alertas.append(
                {
                    "tipo": "warning",
                    "titulo": "Marcas Pendientes",
                    "mensaje": f"Hay {marcas_pendientes} marcas pendientes de procesamiento",
                    "prioridad": "media",
                }
            )

        # Alerta por tasa de aprobación baja
        porcentaje_aprobacion = stats_marcas.get("porcentaje_aprobacion", 0)
        if porcentaje_aprobacion < 60:
            alertas.append(
                {
                    "tipo": "error",
                    "titulo": "Tasa de Aprobación Baja",
                    "mensaje": f"La tasa de aprobación es del {porcentaje_aprobacion}%",
                    "prioridad": "alta",
                }
            )

        # Alerta por logos fallidos
        tasa_exito_logos = stats_logos.get("tasa_exito", 0)
        if tasa_exito_logos < 70:
            alertas.append(
                {
                    "tipo": "warning",
                    "titulo": "Logos Fallidos",
                    "mensaje": f"La tasa de éxito de logos es del {tasa_exito_logos}%",
                    "prioridad": "baja",
                }
            )

        return alertas
