from pages.login import __login__obj

# Obtener las cookies
cookies = __login__obj.cookies

# Obtener el nombre de usuario
username = cookies['__username__']
