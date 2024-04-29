# Importar librerías necesarias
import streamlit as st



def obtener_nombre_usuario(login_obj):
    """
    Obtiene el nombre de usuario desde las cookies.

    Args:
        cookies (dict): Un diccionario con las cookies de la sesión.

    Returns:
        str: El nombre de usuario.
    """
    if 'username' in st.session_state:
        username = st.session_state['username']
    return username