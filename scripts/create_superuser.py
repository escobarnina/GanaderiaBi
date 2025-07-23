#!/usr/bin/env python3
"""
Script para crear un superusuario directamente en la base de datos.
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
from django.contrib.auth.hashers import make_password
from datetime import datetime


def create_superuser():
    """Crear un superusuario directamente en la base de datos."""

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

            # Datos del superusuario
            username = "admin"
            email = "admin@ganaderia.com"
            password = "admin123"  # Contraseña simple para desarrollo
            hashed_password = make_password(password)
            now = datetime.now()

            # Verificar si el usuario ya existe
            check_user_sql = "SELECT id FROM auth_user WHERE username = %s"
            cursor.execute(check_user_sql, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                print(f"⚠️  El usuario '{username}' ya existe")
                return

            # Insertar el superusuario
            insert_user_sql = """
            INSERT INTO auth_user (
                password, last_login, is_superuser, username, 
                first_name, last_name, email, is_staff, 
                is_active, date_joined
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            user_data = (
                hashed_password,  # password
                None,  # last_login
                True,  # is_superuser
                username,  # username
                "",  # first_name
                "",  # last_name
                email,  # email
                True,  # is_staff
                True,  # is_active
                now,  # date_joined
            )

            cursor.execute(insert_user_sql, user_data)
            connection.commit()

            print(f"✅ Superusuario '{username}' creado exitosamente!")
            print(f"📧 Email: {email}")
            print(f"🔑 Contraseña: {password}")
            print(f"🌐 Accede al admin en: http://localhost:8000/admin/")

    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión cerrada")


if __name__ == "__main__":
    print("🐄 Creando superusuario para GanaderiaBi")
    print("=" * 50)
    create_superuser()
