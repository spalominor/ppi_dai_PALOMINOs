# Importar el objeto login de la página de login
from pages.login import __login__obj

# Obtener las cookies
cookies = __login__obj.cookies

# Obtener el nombre de usuario
username = cookies['__username__']
"""
# Obtener el nombre del usuario desde las cookies de la sesión
username = cookies['__username__']
"""