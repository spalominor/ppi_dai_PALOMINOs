import streamlit as st
import os
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_cookies_manager import EncryptedCookieManager
from .utils import check_usr_pass
from .utils import load_lottieurl
from .utils import check_valid_name
from .utils import check_valid_email
from .utils import check_unique_email
from .utils import check_unique_usr
from .utils import register_new_usr
from .utils import check_email_exists
from .utils import generate_random_passwd
from .utils import send_passwd_in_email
from .utils import change_passwd
from .utils import check_current_passwd

#st.session_state
class __login__:
    """
    Builds the UI for the Login/ Sign Up page.
    """

    def __init__(self, auth_token: str, company_name: str, width, height, 
                 logout_button_name: str = 'Logout', 
                 hide_menu_bool: bool = False, 
                 hide_footer_bool: bool = False, 
                 lottie_url: str = "https://assets8.lottiefiles.com/packag" + 
                 "es/lf20_ktwnwv5m.json" ):
        """
        Método constructor de la clase __login__
        
        Args:
            auth_token (str): El token de autenticación de la API del Email
            company_name (str): El nombre de la empresa
            width (int): Ancho de la interfaz
            height (int): Alto de la interfaz
            logout_button_name (str): Nombre del botón de logout
            hide_menu_bool (bool): Ocultar el menú de Streamlit
            hide_footer_bool (bool): Ocultar el footer de Streamlit
            lottie_url (str): URL de la animación Lottie
            
        Returns:
            None
        """
        # Cargar las credenciales de cookies
        password = os.getenv("COOKIES_PASSWORD")
        
        self.auth_token = auth_token
        self.company_name = company_name
        self.width = width
        self.height = height
        self.logout_button_name = logout_button_name
        self.hide_menu_bool = hide_menu_bool
        self.hide_footer_bool = hide_footer_bool
        self.lottie_url = lottie_url

        self.cookies = EncryptedCookieManager(
        prefix="streamlit_login_ui_yummy_cookies",
        password=password)

        if not self.cookies.ready():
            st.stop()   


    def login_widget(self) -> None:
        """
        Crea el widget de inicio de sesión y autentica al usuario.
        
        Args:
            Self
            
        Returns:
            None
        """

        # Checks if cookie exists.
        if st.session_state['LOGGED_IN'] is False:
            if st.session_state['LOGOUT_BUTTON_HIT'] is False:
                fetched_cookies = self.cookies
                if '__username__' in fetched_cookies.keys():
                    cookies_temp = '1c9a923f-fb21-4a91-b3f3-5f18e3f01182'
                    if fetched_cookies['__username__'] != cookies_temp:
                        st.session_state['LOGGED_IN'] = True
                        st.session_state[
                            'username'] = fetched_cookies['__username__']

        if st.session_state['LOGGED_IN'] is False:
            st.session_state['LOGOUT_BUTTON_HIT'] = False
            st.session_state['username'] = None

            del_login = st.empty()
            with del_login.form("Login Form"):
                username = st.text_input("Usuario", 
                                         placeholder = 'Tu nombre de usuario')
                password = st.text_input("Contraseña", 
                                         placeholder = 'Tu contraseña', 
                                         type = 'password')

                st.markdown("###")
                login_submit_button = st.form_submit_button(label = 'Login')

                if login_submit_button is True:
                    authenticate_user_check = check_usr_pass(username, 
                                                             password)

                    if authenticate_user_check is False:
                        st.error("Usuario o contraseña incorrectos")

                    else:
                        st.session_state['LOGGED_IN'] = True
                        st.session_state['username'] = username
                        self.cookies['__username__'] = username
                        self.cookies.save()
                        del_login.empty()
                        st.rerun()


    def animation(self) -> None:
        """
        Crea la animación Lottie en la interfaz de usuario.
        
        Args:
            Self
        
        Returns:
            None
        """
        # Cargar la animación Lottie
        lottie_json = load_lottieurl(self.lottie_url)
        
        # Mostrar la animación Lottie
        st_lottie(lottie_json, width = self.width, height = self.height)


    def sign_up_widget(self) -> None:
        """
        Crea el widget de registro y almacena la información del usuario de 
        forma segura en la base de datos.
        
        Args:
            Self
            
        Returns:
            None
        """
        with st.form("Sign Up Form"):
            name_sign_up = st.text_input("Nombre *", 
                                         placeholder = 'Ingresa tu nombre')
            valid_name_check = check_valid_name(name_sign_up)

            email_sign_up = st.text_input("Email *", 
                                          placeholder = 'Ingresa tu email')
            valid_email_check = check_valid_email(email_sign_up)
            unique_email_check = check_unique_email(email_sign_up)
            
            mensaje_username = 'Ingresa un nombre de usuario único'
            username_sign_up = st.text_input("Usuario *", 
                                             placeholder = mensaje_username)
            unique_username_check = check_unique_usr(username_sign_up)

            mensaje_contraseña = 'Crea una contraseña segura'
            password_sign_up = st.text_input("Password *", 
                                             placeholder = mensaje_contraseña, 
                                             type = 'password')

            st.markdown("###")
            sign_up_submit_button = st.form_submit_button(label = 'Register')

            if sign_up_submit_button:
                if valid_name_check is False:
                    st.error("Por favor, ingrese un nombre de usuario válido")

                elif valid_email_check is False:
                    st.error("Por favor, ingrese un email válido")
                
                elif unique_email_check is False:
                    st.error("Este email ya está registrado")
                
                elif unique_username_check is False:
                    st.error(f'Lo sentimos, {username_sign_up} ya existe')
                
                elif unique_username_check is None:
                    st.error('Ingresa un nombre de usuario')

                if valid_name_check is True:
                    if valid_email_check is True:
                        if unique_email_check is True:
                            if unique_username_check is True:
                                register_new_usr(name_sign_up, 
                                                 email_sign_up, 
                                                 username_sign_up, 
                                                 password_sign_up)
                                st.success("¡Registro Exitoso!")


    def forgot_password(self) -> None:
        """
        Crea un widget para recuperar la contraseña en caso de olvido.
        Verifica que el email ingresado por el usuario esté en la base de 
        datos.
        
        Args:
            Self
        
        Returns:
            None
        """
        with st.form("Forgot Password Form"):
            mensaje_email = 'Ingresa el email registrado con nosotros'
            email_forgot_passwd = st.text_input("Email", 
                                                placeholder=mensaje_email)
            email_exists_check, username_forgot_passwd = check_email_exists(
                email_forgot_passwd)

            st.markdown("###")
            forgot_passwd_submit_button = st.form_submit_button(
                label = 'Enviar contraseña')

            if forgot_passwd_submit_button:
                if email_exists_check is False:
                    st.error("Email ID not registered with us!")

                if email_exists_check is True:
                    random_password = generate_random_passwd()
                    send_passwd_in_email(self.auth_token, 
                                         username_forgot_passwd, 
                                         email_forgot_passwd, 
                                         self.company_name, 
                                         random_password)
                    change_passwd(email_forgot_passwd, random_password)
                    st.success("""¡Contraseña segura enviada a su 
                               correo electrónico!""")


    def reset_password(self) -> None:
        """
        Crea un widget para restablecer la contraseña temporal enviada al
        correo del usuario. Recibe la contraseña enviada y actualiza la
        nueva contraseña ingresada en la base de datos.
        
        Args:
            Self
            
        Returns:
            None
        """
        with st.form("Reset Password Form"):
            mensaje_email = 'Ingresa el email registrado con nosotros'
            email_reset_passwd = st.text_input("Email", 
                                               placeholder=mensaje_email)
            
            email_exists_check, username_reset_passwd = check_email_exists(
                email_reset_passwd)

            mensaje_contraseña = 'Ingresa la contraseña enviada a tu email'
            current_passwd = st.text_input("Contraseña temporal", 
                                           placeholder=mensaje_contraseña)
            current_passwd_check = check_current_passwd(email_reset_passwd, 
                                                        current_passwd)

            mensaje_contraseña_n = 'Crea una nueva contraseña segura'
            new_passwd = st.text_input("New Password", 
                                       placeholder=mensaje_contraseña_n, 
                                       type = 'password')

            mensaje_contraseña_n_1 = 'Re-ingresa la nueva contraseña'
            new_passwd_1 = st.text_input("Confirmar nueva contraseña", 
                                         placeholder=mensaje_contraseña_n_1, 
                                         type = 'password')

            st.markdown("###")
            reset_passwd_submit_button = st.form_submit_button(
                label = 'Cambiar contraseña')

            if reset_passwd_submit_button:
                if email_exists_check is False:
                    st.error("Email no registrado con nosotros")

                elif current_passwd_check is False:
                    st.error("Contraseña temporal incorrecta")

                elif new_passwd != new_passwd_1:
                    st.error("Contraseñas no coinciden")
            
                if email_exists_check is True:
                    if current_passwd_check is True:
                        change_passwd(email_reset_passwd, new_passwd)
                        st.success("Contraseña cambiada exitosamente")
                

    def logout_widget(self) -> None:
        """
        Crea el widget de logout y cierra la sesión del usuario.
        
        Args:
            Self
        
        Returns:
            None
        """
        if st.session_state['LOGGED_IN'] is True:
            del_logout = st.sidebar.empty()
            del_logout.markdown("#")
            logout_click_check = del_logout.button(self.logout_button_name)

            if logout_click_check is True:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                st.session_state['LOGGED_IN'] = False
                st.session_state['username'] = None
                cookie_temp = '1c9a923f-fb21-4a91-b3f3-5f18e3f01182'
                self.cookies[
                    '__username__'] = cookie_temp
                del_logout.empty()
                st.rerun()
        

    def nav_sidebar(self):
        """
        Crea la barra lateral de navegación.
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title = 'Mi Cuenta',
                menu_icon = 'list-columns-reverse',
                icons = ['box-arrow-in-right', 
                         'person-plus', 
                         'x-circle',
                         'arrow-counterclockwise'],
                options = ['Ingresar', 
                           'Crear cuenta', 
                           'Olvidé mi contraseña', 
                           'Cambiar contraseña'],
                styles = {
                    "container": {"padding": "5px"},
                    "nav-link": {"font-size": "14px", 
                                 "text-align": "left", 
                                 "margin":"0px"}} )
        return main_page_sidebar, selected_option
    

    def hide_menu(self) -> None:
        """
        Esconde el menú de Streamlit de la parte superior derecha.
        
        Args:
            Self
            
        Returns:
            None
        """
        st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        </style> """, unsafe_allow_html=True)
    

    def hide_footer(self) -> None:
        """
        Esconde el pie de página de Streamlit. 
        """
        st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)


    def build_login_ui(self):
        """
        Construye la interfaz del manejo de usuarios. Trabaja con todas las 
        funciones anteriores y las integra. Retorna el estado de la sesión del 
        usuario en una variable de sesión.

        Args:
            Self
            
        Returns:
            bool: Retorna True si el usuario está autenticado, de lo contrario
        """
        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False
            
        if 'username' not in st.session_state:
            st.session_state['username'] = None

        main_page_sidebar, selected_option = self.nav_sidebar()

        if selected_option == 'Ingresar':
            c1, c2 = st.columns([7,3])
            with c1:
                self.login_widget()
            with c2:
                if st.session_state['LOGGED_IN'] is False:
                    self.animation()
        
        if selected_option == 'Crear cuenta':
            self.sign_up_widget()

        if selected_option == 'Olvidé mi contraseña':
            self.forgot_password()

        if selected_option == 'Cambiar contraseña':
            self.reset_password()
        
        self.logout_widget()

        if st.session_state['LOGGED_IN'] is True:
            main_page_sidebar.empty()
        
        if self.hide_menu_bool is True:
            self.hide_menu()
        
        if self.hide_footer_bool is True:
            self.hide_footer()
        
        return st.session_state['LOGGED_IN']
