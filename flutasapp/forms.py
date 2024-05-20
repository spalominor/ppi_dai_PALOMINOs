"""
Módulo que contiene los formularios de la aplicación.

Clases:
    SignUpForm: Formulario para el registro de usuarios.
    LoginForm: Formulario para el inicio de sesión de usuarios.
    PasswordResetRequestForm: Formulario para solicitar restablecimiento de
        contraseña.
    ChangePasswordForm: Formulario para cambiar la contraseña del usuario.
    VehicleSearchForm: Formulario para buscar vehículos.
    FuelCostForm: Formulario para calcular el costo de combustible.
    
Funciones:
    None.
"""
import re
import secrets
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as Error
import string



class SignUpForm(UserCreationForm):
    """
    Un formulario que extiende UserCreationForm para incluir un campo del
    correo electrónico.
    
    Atributos:
        email (EmailField): Campo para el correo electrónico.
        
    Métodos:
        Meta: Clase que contiene metadatos para el formulario.
        
    """
    # Crear el campo de correo electrónico en el formulario
    email = forms.EmailField(max_length=254, 
                             help_text='Required. Inform a valid email.')
    
    # Crear el campo de aceptación de la política de privacidad
    # Ya solucionado con HTML y JS
    """
    accept_data_policy = forms.BooleanField(
        label=('He leído y acepto la política de '
               'tratamiento de datos personales'),
        required=True
    )
    """

    def clean_password1(self):
        """
        Método que valida la contraseña ingresada por el usuario.
        
        Args:
            self (SignUpForm): Instancia del formulario.
            
        Returns:
            str: Contraseña ingresada por el usuario.
            
        Raises:
            ValidationError: Si la contraseña tiene menos de 8 caracteres, no
                contiene al menos una letra mayúscula o no contiene al menos
                un número.
        """
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise Error("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password1):
            raise Error("La contraseña debe tener al menos una mayúscula.")
        if not re.search(r'\d', password1):
            raise Error("La contraseña debe contener al menos un número.")
        return password1

    def clean_email(self):
        """
        Método que valida el correo electrónico ingresado por el usuario.
        
        Args:
            self (SignUpForm): Instancia del formulario.
            
        Returns:
            str: Correo electrónico ingresado por el usuario.
            
        Raises:
            ValidationError: Si el correo electrónico no tiene un formato
                válido.
        """
        email = self.cleaned_data.get("email")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 
                        email):
            raise Error("Dirección de correo electrónico no válida.")
        return email

    def clean_username(self):
        """
        Método que valida el nombre de usuario ingresado por el usuario.
        
        Args:
            self (SignUpForm): Instancia del formulario.
            
        Returns:
            str: Nombre de usuario ingresado por el usuario.
            
        Raises:
            ValidationError: Si el nombre de usuario ya está en uso.
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise Error("Este nombre de usuario ya está en uso.")
        return username

    def clean_password2(self):
        """
        Método que valida la confirmación de la contraseña ingresada por el
        usuario.
        
        Args:
            self (SignUpForm): Instancia del formulario.
            
        Returns:
            str: Confirmación de la contraseña ingresada por el usuario.
            
        Raises:
            ValidationError: Si las contraseñas ingresadas no coinciden.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        # Comparar las contraseñas ingresadas por el usuario
        if password1 and password2 and password1 != password2:
            raise Error("Las contraseñas no coinciden.")
        return password2
    
    
    def clean_accept_privacy_policy(self):
        """
        Método que valida que el usuario haya aceptado la política de
        privacidad.
        
        Args:
            self (SignUpForm): Instancia del formulario.
            
        Returns:
            bool: Valor de la casilla de aceptación de la política de
            privacidad.
            
        Raises:
            ValidationError: Si el usuario no ha aceptado la política de
            privacidad.
        """
        accept_privacy_policy = self.cleaned_data.get("accept_privacy_policy")
        if not accept_privacy_policy:
            raise Error("Debes aceptar la política de "
                        "privacidad para registrarte.")
        return accept_privacy_policy


    class Meta:
        """
        Clase que contiene metadatos para el formulario.
        
        Atributos:
            model (User): Modelo de usuario.
            fields (tuple): Campos del formulario.
            
        Métodos:
            None.
        """
        model = User
        fields = ('username', 
                  'email', 
                  'password1', 
                  'password2')
        

class LoginForm(AuthenticationForm):
    """
    Formulario de inicio de sesión personalizado que extiende 
    AuthenticationForm de Django.
    
    Atributos:
        None.
        
    Métodos:
        __init__: Constructor de la clase.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Puedes personalizar los widgets de los campos si lo deseas
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Contraseña'})
        

class PasswordResetRequestForm(forms.Form):
    """
    Formulario para solicitar restablecimiento de contraseña.
    
    Atributos:
        email (EmailField): Campo para el correo electrónico.
        
    Métodos:
        clean_email: Método que valida el correo electrónico ingresado por el
            usuario.
        generate_temporary_password: Método que genera una contraseña temporal
            segura.
    """
    email = forms.EmailField(label="Correo electrónico", 
                             max_length=254, 
                             help_text=('Un email será enviado a esta '
                                        'dirección con instrucciones '
                                        'para restablecer la contraseña.'))

    def clean_email(self):
        """
        Valida que el correo electrónico ingresado por el usuario exista en la
        base de datos.
        
        Args:
            Self: Instancia del formulario.
            
        Returns:
            str: Correo electrónico validado.
            
        Raises:
            ValidationError: Si no existe ningún usuario registrado con el
                dirección de correo electrónico ingresada.
        """
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(("No hay ningún usuario registrado "
                                         "con este correo electrónico."))
        return email
    
    
    def generate_temporary_password():
        """
        Genera una contraseña temporal segura.
        
        Args:
            None.
            
        Returns:
            str: Contraseña temporal generada.
        """
        length = 12
        alphabet = string.ascii_letters + string.digits        
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        return password
    

class ChangePasswordForm(forms.Form):
    """
    Formulario para cambiar la contraseña del usuario.
    Hereda de la clase Form de Django.

    Atributos:
        old_password (CharField): Campo para la contraseña actual.
        new_password1 (CharField): Campo para la nueva contraseña.
        new_password2 (CharField): Campo para confirmar la nueva contraseña.
        
    Métodos:
        clean_old_password: Valida que la contraseña actual ingresada sea
            correcta.
        clean_new_password2: Valida que las dos entradas de la nueva contraseña
            coincidan.
        __init__: Inicializa el formulario con el usuario autenticado.
    """
    # Crear los campos para el formulario
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput
    )

    def clean_old_password(self):
        """
        Valida que la contraseña actual ingresada sea correcta.
        
        Args:
            Self: Instancia del formulario.

        Returns:
            str: Contraseña actual validada.

        Raises:
            forms.ValidationError: Si la contraseña actual es incorrecta.
        """
        old_password = self.cleaned_data.get('old_password')
        user = authenticate(username=self.user.username, password=old_password)
        if not user:
            raise forms.ValidationError("La contraseña actual es incorrecta.")
        return old_password

    def clean_new_password2(self):
        """
        Valida que las dos entradas de la nueva contraseña coincidan.
        
        Args:
            Self: Instancia del formulario.

        Returns:
            str: Nueva contraseña confirmada.

        Raises:
            forms.ValidationError: Si las nuevas contraseñas no coinciden.
        """
        # Obtener las contraseñas ingresadas por el usuario
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        
        # Comparar las contraseñas ingresadas por el usuario
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("Las nuevas contraseñas no coinciden.")
        return new_password2


    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario con el usuario autenticado.

        Args:
            *args: Argumentos posicionales.
            **kwargs: Argumentos de palabras clave.
            
        Returns:
            None.
        """
        self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        

class VehicleSearchForm(forms.Form):
    """
    Formulario de búsqueda de vehículos.
    
    Clase Padre:
        forms.Form: Clase base de formularios de Django.
    
    Fields:
        brand (CharField): Campo para la marca del vehículo.
        model_year (IntegerField): Campo para el año modelo del vehículo.
        version (CharField): Campo para la versión del vehículo.
    """
    brand = forms.CharField(label='Marca',
     max_length=100,
      required=False, 
      widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    sub_brand = forms.CharField(label='Submarca',
     max_length=100,
      required=False, 
      widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    model_year = forms.IntegerField(label='Año Modelo',
     required=False, 
     widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    version = forms.CharField(label='Versión',
     max_length=100,
      required=False, 
      widget=forms.TextInput(attrs={'autocomplete': 'off'}))


class FuelCostForm(forms.Form):
    """
    Formulario para calcular el costo de combustible según la distancia
    recorrida en una ruta.
    
    Clase Padre:
        forms.Form: Clase base de formularios de Django.
        
    Fields:
        start_address (CharField): Campo para la dirección de inicio.
        end_address (CharField): Campo para la dirección de llegada.
        fuel_efficiency (FloatField): Campo para el rendimiento del vehículo.
        fuel_type (ChoiceField): Campo para el tipo de combustible.
    """
    start_address = forms.CharField(label='Dirección de inicio',
                    help_text='Ingrese la dirección de origen de la ruta')
    end_address = forms.CharField(label='Dirección de llegada',
                    help_text='Ingrese la dirección de destino de la ruta')
    fuel_efficiency = forms.FloatField(label='Rendimiento (km/L)',
                    help_text='Ingrese el rendimiento en km/L del vehículo',
                    min_value=0.0, max_value=1000.0)
    fuel_type = forms.ChoiceField(label='Tipo de Combustible', 
                                  choices=[('gasolina', 'Gasolina'), 
                                           ('diesel', 'Diesel')], 
                                help_text='Seleccione el tipo de combustible')
