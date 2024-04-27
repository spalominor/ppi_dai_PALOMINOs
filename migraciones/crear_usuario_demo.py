import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de DATABASE_URL del entorno
DATABASE_URL = os.getenv('DATABASE_URL')

def crear_usuario(usuario, nombre, email, clave):
    """
    Crea un nuevo usuario para la aplicación en la base de datos 
    de PostgreSQL con Heroku.

    Args:
        usuario (str): El nombre de usuario del nuevo usuario.
        nombre (str): El nombre del nuevo usuario.
        email (str): El email del nuevo usuario.
        clave (str): La clave del nuevo usuario.

    Returns:
        None
    """
    try:
        # Conectar a la base de datos PostgreSQL en Heroku
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        
        # Crear un cursor para ejecutar consultas SQL
        cursor = conn.cursor()

        # Definir la consulta SQL para insertar un nuevo usuario
        sql_insert_usuario = """
            INSERT INTO usuarios (usuario, nombre, email, clave)
            VALUES (%s, %s, %s, %s)
        """

        # Ejecutar la consulta SQL para insertar el nuevo usuario
        cursor.execute(sql_insert_usuario, (usuario, nombre, email, clave))
        
        # Confirmar los cambios
        conn.commit()
        print("Usuario creado exitosamente.")

    except psycopg2.Error as e:
        print("Error al crear el usuario:", e)

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

# Datos del nuevo usuario
usuario = 'demo123'
nombre = 'Palta Malana'
email = 'mapa@example.com'
clave = 'demo123'

# Llamar a la función para crear el usuario
crear_usuario(usuario, nombre, email, clave)
