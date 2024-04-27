import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def conectar_base_datos():
    try:
        # Obtener el valor de DATABASE_URL del entorno
        DATABASE_URL = os.getenv('DATABASE_URL')

        # Conectar a la base de datos PostgreSQL en Heroku
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        print("Conexión a la base de datos exitosa.")
        return conn

    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def ejecutar_sql_desde_archivo(archivo_sql, conn):
    try:
        # Abre y lee el archivo SQL
        with open(archivo_sql, 'r') as archivo:
            sql = archivo.read()

        # Crea un cursor para ejecutar las instrucciones SQL
        cursor = conn.cursor()

        # Ejecuta las instrucciones SQL
        cursor.execute(sql)

        # Confirma los cambios
        conn.commit()
        print("Las tablas se han creado exitosamente.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error al ejecutar las instrucciones SQL:", error)

    finally:
        # Cierra el cursor
        cursor.close()

# Nombre del archivo SQL que contiene las instrucciones para crear las tablas
archivo_sql = 'flutas_db_create.sql'

# Conectar a la base de datos
conn = conectar_base_datos()

if conn is not None:
    # Ejecutar las instrucciones SQL desde el archivo
    ejecutar_sql_desde_archivo(archivo_sql, conn)
    # Cerrar la conexión a la base de datos
    conn.close()
