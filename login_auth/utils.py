# Importar bibliotecas estándar de Python
import re
import os

# Importar bibliotecas de terceros
import psycopg2
from courier.client import Courier
import secrets
from dotenv import load_dotenv
from argon2 import PasswordHasher
import requests



# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de DATABASE_URL del entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Crear una instancia del objeto para cifrar contraseñas
ph = PasswordHasher() 

def check_usr_pass(username: str, password: str) -> bool:
    """
    Autentica el nombre de usuario y la contraseña.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT clave FROM usuarios WHERE usuario = %s", 
                       (username,))
        hashed_password = cursor.fetchone()
        if hashed_password and ph.verify(hashed_password[0], password):
            return True
    except Exception as e:
        print("Error al autenticar el usuario:", e)
    finally:
        cursor.close()
        conn.close()
    
    return False


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        print(e)


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    # Compilar la expresión regular
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@' +
                        r'[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(email_sign_up: str) -> bool:
    """
    Verifica si el correo electrónico ya está registrado en la base de datos.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT email FROM usuarios WHERE email = %s", 
                       (email_sign_up,))
        if cursor.fetchone():
            return False
    except psycopg2.Error as e:
        print("Error al verificar la unicidad del correo electrónico:", e)
    finally:
        cursor.close()
        conn.close()

    return True


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Verifica si la cadena de texto no está vacía.
    
    Args:
        username_sign_up (str): La cadena de texto a verificar.
        
    Returns:
        bool: True si la cadena de texto no está vacía, False si está vacía.
    """
    if not username_sign_up or username_sign_up.isspace():
        return False
    return True


def check_unique_usr(username_sign_up: str) -> bool:
    """
    Verifica si el nombre de usuario ya está registrado en la base de datos 
    y si no está vacío.
    
    Args:
        username_sign_up (str): El nombre de usuario a verificar
        
    Returns:
        bool: True si el nombre de usuario no está registrado y no está vacío, 
              False si ya está registrado o está vacío
    """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        # Verificar si el nombre de usuario ya está en uso
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = %s", 
                       (username_sign_up,))
        if cursor.fetchone():
            return False
        
        # Verificar si el nombre de usuario no está vacío
        if non_empty_str_check(username_sign_up) is False:
            return False
        
        return True
    except psycopg2.Error as e:
        print("Error al verificar la unicidad del nombre de usuario:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def register_new_usr(name: str, 
                     email: str, 
                     username: str, 
                     password: str) -> None:
    """
    Registra la información del nuevo usuario en la base de datos.
    
    Args:
        name (str): El nombre del usuario
        email (str): El correo electrónico del usuario
        username (str): El nombre de usuario
        password (str): La contraseña del usuario
        
    Returns:
        None
    """
    hashed_password = ph.hash(password)
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (
                nombre, email, usuario, clave) 
            VALUES (%s, %s, %s, %s)
            """, (name, email, username, hashed_password)
            )
        conn.commit()
        print("Usuario registrado exitosamente.", username)
    except psycopg2.Error as e:
        print("Error al registrar el usuario:", e)
    finally:
        cursor.close()
        conn.close()


def check_username_exists(username: str) -> bool:
    """
    Verifica si el nombre de usuario ya existe en la base de datos.
    
    Args:
        username (str): El nombre de usuario a verificar
        
    Returns:
        bool: True si el nombre de usuario ya existe, False si no existe
    """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = %s", (username))
        if cursor.fetchone():
            return True
    except psycopg2.Error as e:
        print("Error al verificar el nombre de usuario:", e)
    finally:
        cursor.close()
        conn.close()

    return False
        

def check_email_exists(email: str):
    """
    Verifica si el correo electrónico ya está registrado en la base de datos.
    Si está registrado, devuelve True junto con el nombre de usuario asociado.
    Si no está registrado, devuelve False.
    
    Args:
        email (str): El correo electrónico del usuario
        
    Returns:
        tuple: (bool, str)
    """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT usuario FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            # Devuelve True y el nombre de usuario asociado al email
            return True, user[0]  
    except psycopg2.Error as e:
        print("Error al verificar el correo electrónico:", e)
    finally:
        cursor.close()
        conn.close()

    # Devuelve False si el correo electrónico no está registrado
    return False, None  



def generate_random_passwd() -> str:
    """
    Genera una clave temporal de 10 caracteres aleatorios.
    
    Args: 
        None
        
    Returns:
        str: La clave temporal generada aleatoriamente
    """
    # Definir la longitud de la clave temporal
    password_length = 10
    
    # Retornar una clave temporal aleatoria
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(auth_token: str, 
                         username_forgot_passwd: str, 
                         email_forgot_passwd: str, 
                         company_name: str, 
                         random_password: str) -> None:
    """
    Envía la clave temporal al usuario que olvidó la contraseña.
    
    Args:
        auth_token (str): El token de autenticación de Courier (Email API)
        username_forgot_passwd (str): El usuario que olvidó la contraseña
        email_forgot_passwd (str): El email del usuario que olvidó la clave
        company_name (str): El nombre de la aplicación
        random_password (str): La clave temporal generada aleatoriamente
        
    Returns:
        None
    """
    # Crear el objeto cliente Courier para enviar el correo
    client = Courier(authorization_token=auth_token)

    # Enviar el correo con la clave temporal
    client.send(
    message={
        "to": {
            "email": email_forgot_passwd
        },
        "content": {
            "title": company_name + ": Clave temporal",
            "body": (
                "¡Hola! " + username_forgot_passwd + "," + "\n" +
                "\n" +
                "tu clave temporal es: " + random_password + "\n" +
                "\n" +
                "{{info}}"
            )
        },
        "data": {
            "info": "Por favor cambia tu contraseña nuevamente por seguridad."
        }
    }
)


def change_passwd(email: str, new_password: str) -> None:
    """
    Actualiza la contraseña de un usuario en la base de datos.
    
    Args:
        email (str): El correo electrónico del usuario
        new_password (str): La nueva contraseña del usuario
        
    Returns:
        None
    """
    # Cifrar la nueva contraseña
    hashed_password = ph.hash(new_password)
    
    # Conectar a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    
    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    try:
        # Actualizar la contraseña del usuario
        cursor.execute(
            "UPDATE usuarios SET clave = %s WHERE email = %s", 
            (hashed_password, email))
        conn.commit()
        
        # Imprimir un mensaje de éxito
        print("Contraseña de usuario actualizada exitosamente.")
    except psycopg2.Error as e:
        # Imprimir un mensaje de error si ocurre un problema
        print("Error al actualizar la contraseña de usuario:", e)
    finally:
        # Cerrar el cursor
        cursor.close()
        
        # Cerrar la conexión a la base de datos
        conn.close()
    

def check_current_passwd(email: str, current_passwd: str) -> bool:
    """
    Autentica la contraseña actual del usuario.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    if email is None or current_passwd is None:
        return False

    try:
        cursor.execute("SELECT clave FROM usuarios WHERE email = %s", (email,))
        hashed_password = cursor.fetchone()
        if hashed_password and ph.verify(hashed_password[0], current_passwd):
            print("Contraseña actual verificada.", email)
            return True
    except Exception as e:
        print("Error al verificar la contraseña actual:", e)
    finally:
        cursor.close()
        conn.close()

    return False
