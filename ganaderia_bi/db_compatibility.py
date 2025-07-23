"""
Configuración de compatibilidad para MariaDB 10.4 y 10.5+ con Django 5.2
"""

import pymysql
from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper

# Configurar PyMySQL para MariaDB
pymysql.install_as_MySQLdb()


# Configuración específica para MariaDB
class DatabaseWrapper(MySQLDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar RETURNING para compatibilidad con MariaDB 10.4
        self.features.supports_returning = False


# Configurar el wrapper de base de datos
from django.db.backends.mysql.base import DatabaseWrapper

DatabaseWrapper = DatabaseWrapper
