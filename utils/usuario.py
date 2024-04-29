# Importar librerías necesarias
import streamlit as st



def obtener_nombre_usuario():
    """
    Obtiene el nombre de usuario desde las cookies.

    Args:
        cookies (dict): Un diccionario con las cookies de la sesión.

    Returns:
        str: El nombre de usuario.
    """
    if st.session_state['LOGGED_IN']:
        username = st.session_state['username']
        return username
    else:
        return "No logeado"