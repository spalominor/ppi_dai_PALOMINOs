# Importar librerias necesarias
# Importar librerias para el manejo de Streamlit
import streamlit as st
from login_auth.widgets import __login__

# Importar dotenv para cargar las variables de entorno
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token de autenticación del archivo .env
courier_auth_token = os.getenv("COURIER_AUTH_TOKEN")

# Crear el objeto de autenticación
__login__obj = __login__(
    auth_token=courier_auth_token,
    company_name="Flutas",
    width=300,
    height=400,
    logout_button_name='Salir',
    hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
)

# Construir la interfaz de inicio de sesión y registrar nuevos usuarios
LOGGED_IN = __login__obj.build_login_ui()

# Obtener las cookies
cookies = __login__obj.cookies

# Obtener el nombre de usuario
username = cookies['__username__']

# Si el usuario está autenticado, mostrar la interfaz para registrar nuevos usuarios
if LOGGED_IN:
    st.title("Hola, bienvenido a Flutas, ¿qué deseas hacer hoy?")

    st.subheader("Tu perfil")
                
    st.write("Nombre de usuario:", username)