#!/usr/bin/env python3
"""
Script simple para crear la base de datos y usuario
"""

import mysql.connector


def create_database():
    """Crea la base de datos y usuario"""

    try:
        # Conectar como root
        conn = mysql.connector.connect(host="localhost", user="root", password="")
        cursor = conn.cursor()

        # Crear base de datos
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS ganaderia_bi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print("Base de datos ganaderia_bi creada")

        # Crear usuario
        cursor.execute(
            'CREATE USER IF NOT EXISTS "bi_user"@"localhost" IDENTIFIED BY "password"'
        )
        print("Usuario bi_user creado")

        # Otorgar privilegios
        cursor.execute(
            'GRANT ALL PRIVILEGES ON ganaderia_bi.* TO "bi_user"@"localhost"'
        )
        cursor.execute("FLUSH PRIVILEGES")
        print("Privilegios otorgados")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def test_connection():
    """Prueba la conexión con el nuevo usuario"""

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="bi_user",
            password="password",
            database="ganaderia_bi",
        )
        cursor = conn.cursor()

        print("Conexión exitosa con bi_user")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error de conexión: {e}")
        return False


if __name__ == "__main__":
    print("Creando base de datos GanaderiaBi...")

    if create_database():
        print("\nBase de datos creada correctamente!")

        if test_connection():
            print("Todo listo!")
        else:
            print("Problemas con la conexión del usuario")
    else:
        print("Error creando la base de datos")
