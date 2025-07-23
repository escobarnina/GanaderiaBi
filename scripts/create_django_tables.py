#!/usr/bin/env python3
"""
Script para crear las tablas de Django necesarias para el sistema GanaderiaBi.
"""

import mysql.connector
from mysql.connector import Error


def create_django_tables():
    """Crear las tablas de Django necesarias."""

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

            # Crear tabla auth_user
            auth_user_sql = """
            CREATE TABLE IF NOT EXISTS `auth_user` (
                `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `password` varchar(128) NOT NULL,
                `last_login` datetime(6) NULL,
                `is_superuser` bool NOT NULL,
                `username` varchar(150) NOT NULL UNIQUE,
                `first_name` varchar(150) NOT NULL,
                `last_name` varchar(150) NOT NULL,
                `email` varchar(254) NOT NULL,
                `is_staff` bool NOT NULL,
                `is_active` bool NOT NULL,
                `date_joined` datetime(6) NOT NULL
            );
            """

            # Crear tabla django_content_type
            content_type_sql = """
            CREATE TABLE IF NOT EXISTS `django_content_type` (
                `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `app_label` varchar(100) NOT NULL,
                `model` varchar(100) NOT NULL,
                UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`, `model`)
            );
            """

            # Crear tabla django_admin_log
            admin_log_sql = """
            CREATE TABLE IF NOT EXISTS `django_admin_log` (
                `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `action_time` datetime(6) NOT NULL,
                `object_id` longtext NULL,
                `object_repr` varchar(200) NOT NULL,
                `action_flag` smallint UNSIGNED NOT NULL,
                `change_message` longtext NOT NULL,
                `content_type_id` integer NULL,
                `user_id` integer NOT NULL,
                FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
                FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
            );
            """

            # Crear tabla django_session
            session_sql = """
            CREATE TABLE IF NOT EXISTS `django_session` (
                `session_key` varchar(40) NOT NULL PRIMARY KEY,
                `session_data` longtext NOT NULL,
                `expire_date` datetime(6) NOT NULL
            );
            """

            # Crear tabla django_migrations
            migrations_sql = """
            CREATE TABLE IF NOT EXISTS `django_migrations` (
                `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `app` varchar(255) NOT NULL,
                `name` varchar(255) NOT NULL,
                `applied` datetime(6) NOT NULL
            );
            """

            # Ejecutar las consultas
            tables = [
                ("auth_user", auth_user_sql),
                ("django_content_type", content_type_sql),
                ("django_admin_log", admin_log_sql),
                ("django_session", session_sql),
                ("django_migrations", migrations_sql),
            ]

            for table_name, sql in tables:
                try:
                    cursor.execute(sql)
                    print(f"✅ Tabla {table_name} creada correctamente")
                except Error as e:
                    if "already exists" in str(e):
                        print(f"⚠️  Tabla {table_name} ya existe")
                    else:
                        print(f"❌ Error creando tabla {table_name}: {e}")

            connection.commit()
            print("\n🎉 Tablas de Django creadas exitosamente!")

    except Error as e:
        print(f"❌ Error de conexión: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión cerrada")


if __name__ == "__main__":
    print("🐄 Creando tablas de Django para GanaderiaBi")
    print("=" * 50)
    create_django_tables()
