"""
Configuración de compatibilidad para MariaDB 10.4 con Django 5.2
"""

import django
from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.validation import (
    DatabaseValidation as MySQLDatabaseValidation,
)


class MariaDB104DatabaseWrapper(MySQLDatabaseWrapper):
    """Wrapper personalizado para MariaDB 10.4"""

    def check_database_version_supported(self):
        """Sobrescribir la verificación de versión para permitir MariaDB 10.4"""
        pass  # Permitir cualquier versión


class MariaDB104Validation(MySQLDatabaseValidation):
    """Validación personalizada para MariaDB 10.4"""

    def check_field(self, field, **kwargs):
        """Sobrescribir validaciones específicas si es necesario"""
        return super().check_field(field, **kwargs)


# Configurar el wrapper personalizado
from django.db.backends.mysql.base import DatabaseWrapper

DatabaseWrapper.check_database_version_supported = (
    MariaDB104DatabaseWrapper.check_database_version_supported
)
