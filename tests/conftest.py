"""
Configuración de pytest para el proyecto GanaderiaBi
"""

import pytest
import os
import django
from django.conf import settings

# Configurar Django para testing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Configurar base de datos para testing"""
    with django_db_blocker.unblock():
        from django.core.management import call_command

        call_command("migrate", verbosity=0)


@pytest.fixture
def api_client():
    """Cliente API para testing"""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def db_access_without_rollback_and_truncate(django_db_setup, django_db_blocker):
    """Acceso a base de datos sin rollback"""
    django_db_blocker.unblock()
    yield
    django_db_blocker.restore()


@pytest.fixture
def marca_test_data():
    """Datos de prueba para marcas"""
    return {
        "numero_marca": "M001",
        "nombre_productor": "Juan Pérez",
        "departamento": "SANTA_CRUZ",
        "raza": "HOLSTEIN",
        "cantidad_cabezas": 50,
        "estado": "PENDIENTE",
    }


@pytest.fixture
def marca_aprobada_data():
    """Datos de prueba para marca aprobada"""
    return {
        "numero_marca": "M002",
        "nombre_productor": "María López",
        "departamento": "COCHABAMBA",
        "raza": "JERSEY",
        "cantidad_cabezas": 30,
        "estado": "APROBADO",
    }


@pytest.fixture
def logo_test_data():
    """Datos de prueba para logos"""
    return {
        "marca_id": 1,
        "modelo_ia": "DALL_E_3",
        "prompt": "Logo moderno para marca de ganado bovino",
        "url_logo": "https://example.com/logo.png",
        "tipo_logo": "SIMPLE",
        "calidad_generacion": 0.95,
    }


@pytest.fixture
def kpi_test_data():
    """Datos de prueba para KPIs"""
    return {
        "fecha": "2024-12-19",
        "kpi_tipo": "EFICIENCIA_APROBACION",
        "valor": 85.5,
        "meta": 90.0,
        "departamento": "SANTA_CRUZ",
    }


@pytest.fixture
def dashboard_test_data():
    """Datos de prueba para dashboard"""
    return {
        "fecha": "2024-12-19",
        "total_marcas": 150,
        "marcas_aprobadas": 120,
        "marcas_pendientes": 20,
        "logos_generados": 100,
        "kpi_eficiencia": 85.5,
    }


@pytest.fixture
def historial_test_data():
    """Datos de prueba para historial"""
    return {
        "marca_id": 1,
        "estado_anterior": "PENDIENTE",
        "estado_nuevo": "APROBADO",
        "usuario": "admin",
        "comentario": "Marca aprobada por cumplir requisitos",
    }


@pytest.fixture
def reporte_test_data():
    """Datos de prueba para reportes"""
    return {
        "tipo_reporte": "MENSUAL",
        "fecha_inicio": "2024-12-01",
        "fecha_fin": "2024-12-31",
        "datos_json": {
            "total_marcas": 150,
            "marcas_aprobadas": 120,
            "eficiencia": 85.5,
        },
    }


@pytest.fixture
def mock_repository():
    """Mock de repositorio para testing"""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def mock_use_case():
    """Mock de use case para testing"""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def mock_serializer():
    """Mock de serializer para testing"""
    from unittest.mock import Mock

    return Mock()


@pytest.fixture
def mock_controller():
    """Mock de controller para testing"""
    from unittest.mock import Mock

    return Mock()


# Configuración de pytest
def pytest_configure(config):
    """Configurar pytest"""
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_collection_modifyitems(config, items):
    """Modificar items de colección de tests"""
    for item in items:
        # Marcar tests de unit como unit
        if "test_unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)

        # Marcar tests de integration como integration
        if "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)

        # Marcar tests de API como api
        if "test_api" in item.nodeid:
            item.add_marker(pytest.mark.api)

        # Marcar tests que toman más de 1 segundo como slow
        if "test_slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
