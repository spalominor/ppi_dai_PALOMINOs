"""
Este script contiene la configuración de la instancia de Courier que se 
utilizará para enviar notificaciones a los usuarios del sistema por medio 
del correo electrónico.

Funciones:
    send_password_reset_email(email: str, username: str, password: str) -> dict:
        Envía un correo electrónico para reestablecer la contraseña utilizando 
        la API de mensajería Courier.

Clases:
    None
"""
# Importar la clase Courier desde el módulo trycourier.
from courier.client import Courier



def send_password_reset_email(email: str, username: str, password: str):
    """
    Envía un correo electrónico para reestablecer la contraseña utilizando 
    la API de mensajería Courier.

    Args:
        email (str): El correo electrónico del destinatario.
        username (str): El nombre de usuario del destinatario.
        reset_url (str): La URL de restablecimiento de contraseña.
        
    Returns:
        dict: La respuesta de Courier al enviar el correo electrónico.
    """
    # Crear una instancia de Courier con el token de autenticación de Courier.
    CLIENT = Courier(authorization_token="dk_prod_5KSGAP9WKKMGAXHGH35BA94CMHYT")
    
    response = CLIENT.send(
        message={
            "to": {
                "email": email,
            },
            "content": {
                "title": "Restablecimiento de contraseña",
                "body": f"Hola, {username}!"
                        "\n\nRecibiste este correo electrónico porque "
                        "solicitaste restablecer tu contraseña para tu cuenta."
                        "\n\nEsta es tu nueva contraseña temporal: "
                        f"\n\n{password}\n\n"
                        "Por favor, cambia esta contraseña temporal por una "
                        "nueva tan pronto como sea posible."
            },
            "data": {
                'username': username,
                "reset_url": password,
            },
        }
    )
    return response
