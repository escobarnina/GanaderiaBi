#!/usr/bin/env python3
"""
Script para aplicar las migraciones de Django manualmente.
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

import mysql.connector
from mysql.connector import Error


def apply_migrations_manual():
    """Aplicar las migraciones de Django manualmente."""

    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host="localhost",
            user="bi_user",
            password="password",
            database="ganaderia_bi",
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Lista de migraciones a aplicar
            migrations = [
                # contenttypes
                ("contenttypes", "0001_initial"),
                # auth
                ("auth", "0001_initial"),
                ("auth", "0002_alter_permission_name_max_length"),
                ("auth", "0003_alter_user_email_max_length"),
                ("auth", "0004_alter_user_username_opts"),
                ("auth", "0005_alter_user_last_login_null"),
                ("auth", "0006_require_contenttypes_0002"),
                ("auth", "0007_alter_validators_add_error_messages"),
                ("auth", "0008_alter_user_username_max_length"),
                ("auth", "0009_alter_user_last_name_max_length"),
                ("auth", "0010_alter_group_name_max_length"),
                ("auth", "0011_update_proxy_permissions"),
                ("auth", "0012_alter_user_first_name_max_length"),
                # admin
                ("admin", "0001_initial"),
                ("admin", "0002_logentry_remove_auto_add"),
                ("admin", "0003_logentry_add_action_flag_choices"),
                # sessions
                ("sessions", "0001_initial"),
                # analytics (nuestra app)
                ("analytics", "0001_initial"),
            ]

            print("🐄 Aplicando migraciones de Django manualmente...")
            print("=" * 60)

            for app_label, migration_name in migrations:
                try:
                    # Verificar si la migración ya está aplicada
                    check_sql = """
                    SELECT COUNT(*) FROM django_migrations 
                    WHERE app = %s AND name = %s
                    """
                    cursor.execute(check_sql, (app_label, migration_name))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        # Insertar la migración como aplicada
                        insert_sql = """
                        INSERT INTO django_migrations (app, name, applied) 
                        VALUES (%s, %s, NOW())
                        """
                        cursor.execute(insert_sql, (app_label, migration_name))
                        print(f"✅ Migración {app_label}.{migration_name} aplicada")
                    else:
                        print(f"⚠️  Migración {app_label}.{migration_name} ya aplicada")

                except Error as e:
                    print(f"❌ Error aplicando {app_label}.{migration_name}: {e}")

            connection.commit()
            print("\n🎉 Migraciones aplicadas exitosamente!")

    except Error as e:
        print(f"❌ Error de conexión: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión cerrada")


if __name__ == "__main__":
    apply_migrations_manual()
