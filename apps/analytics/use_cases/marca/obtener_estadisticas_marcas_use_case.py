from typing import Dict, Any, List

from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)


class ObtenerEstadisticasMarcasUseCase:
    """Use Case para obtener estadísticas de marcas"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de marcas

        Returns:
            Dict[str, Any]: Estadísticas generales de marcas
        """
        return self.marca_repository.obtener_estadisticas()

    def estadisticas_por_raza(self) -> List[Dict[str, Any]]:
        """
        Obtiene estadísticas agrupadas por raza bovina

        Returns:
            List[Dict[str, Any]]: Estadísticas por raza con totales y promedios
        """
        return self.marca_repository.obtener_estadisticas_por_raza()

    def estadisticas_por_departamento(self) -> List[Dict[str, Any]]:
        """
        Obtiene estadísticas agrupadas por departamento

        Returns:
            List[Dict[str, Any]]: Estadísticas por departamento con totales y promedios
        """
        return self.marca_repository.obtener_estadisticas_por_departamento()

    def estadisticas_procesamiento_hoy(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de marcas procesadas el día de hoy

        Returns:
            Dict[str, Any]: Estadísticas del día con aprobadas, rechazadas y tasa
        """
        return self.marca_repository.obtener_estadisticas_procesamiento_hoy()

    def resumen_pendientes(self) -> Dict[str, Any]:
        """
        Obtiene resumen de marcas pendientes con información adicional

        Returns:
            Dict[str, Any]: Resumen con total de cabezas y promedio de días pendiente
        """
        return self.marca_repository.obtener_resumen_pendientes()

    def alertas_sistema(self) -> Dict[str, Any]:
        """
        Obtiene alertas del sistema de marcas

        Returns:
            Dict[str, Any]: Alertas críticas y advertencias con cantidades
        """
        return self.marca_repository.obtener_alertas_sistema()
