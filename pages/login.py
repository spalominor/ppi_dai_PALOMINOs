# Importar librerias necesarias
# Importar librerias para el manejo de Streamlit
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__

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
    logout_button_name='Logout',
    hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
)

# Construir la interfaz de inicio de sesión y registrar nuevos usuarios
LOGGED_IN = __login__obj.build_login_ui()

# Si el usuario está autenticado, mostrar la interfaz para registrar nuevos usuarios
if LOGGED_IN:
    st.title("Registro de nuevos usuarios")

    # Formulario para registrar nuevos usuarios
    new_username = st.text_input("Nombre de usuario:")
    new_password = st.text_input("Contraseña:", type="password")
    confirm_password = st.text_input("Confirmar contraseña:", type="password")

    if st.button("Registrar"):
        if new_password == confirm_password:
            # Simplemente imprimir los valores de los nuevos usuarios registrados
            st.write("Nuevo usuario registrado:")
            st.write("Nombre de usuario:", new_username)
            st.write("Contraseña:", new_password)
        else:
            st.error("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
