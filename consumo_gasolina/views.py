# Importa los módulos para el funcionamiento de las vistas de Django
import json
from django.contrib import messages
from django.contrib.auth import (
    authenticate, 
    login, 
    logout, 
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

# Importa los modelos y formularios personalizados
from consumo_gasolina.models import Route, Vehicle
from flutasapp.forms import (
    ChangePasswordForm,
    FuelCostForm,
    LoginForm,
    PasswordResetRequestForm,
    RouteForm,
    SignUpForm,
    VehicleForm,
    VehicleSearchForm,
)

# Importa la clases de utils para buscar y analizar vehículos
from utils.analyze_vehicles import VehicleAnalyzer
from utils.calculate_cost import CostCalculator
from utils.draw_graphs import Drawer
from utils.geo_utils import GeoUtils
from utils.search_vehicle import VehicleSearcher

# Importa la función para enviar correos electrónicos
from .courier import send_password_reset_email

# Crea una instancia de VehicleSearcher para buscar vehículos en el dataset
SEARCHER = VehicleSearcher()

# Crea una instancia de VehicleAnalyzer para analizar la info de los vehículos
ANALYZER = VehicleAnalyzer()

# Crea una instancia de CostCalculator para calcular el costo de combustible
CALCULATOR = CostCalculator()

# Crea una instancia de GeoUtils para geocodificar direcciones
GEOUTILS = GeoUtils()

# Crear una instancia de Drawer para dibujar gráficas
DRAWER = Drawer()

# Create your views here.
def search(request):
    """
    Vista para la página de inicio.

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de inicio con 
        el formulario de búsqueda.
    """
    if request.method == 'POST':
        form = VehicleSearchForm(request.POST)
        if form.is_valid():
            # Buscar vehículos en el dataset con el objeto VehicleSearcher
            vehicles = SEARCHER.search(
                query=form.cleaned_data).to_dict(orient='records')
                                    
            # Renderizar la página de inicio con los resultados de la búsqueda
            return render(
                request, 'search.html', {'form': form, 'vehicles': vehicles})
    else:
        # Inicializar el formulario de búsqueda
        form = VehicleSearchForm()
        
        # Renderizar una búsqueda vacía
        vehicles = SEARCHER.search(query={}).to_dict(orient='records')
    return render(request, 'search.html', {'form': form, 'vehicles': vehicles})




def signup(request):
    """
    Función que permite a un usuario registrarse en el sistema.

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que se enviará al cliente.
    """
    # Si la solicitud es POST, se procesa la información del formulario
    if request.method == "POST":
        # Se crea un formulario con la información recibida
        form = SignUpForm(request.POST)

        # Si el formulario es válido, se guarda el usuario en la base de datos
        if form.is_valid():
            # Guarda el usuario en la base de datos
            form.save()

            # Redirige al usuario a la página de inicio
            return redirect("login")
    else:
        # Si la solicitud no es POST, se crea un formulario en blanco
        form = SignUpForm()

    # Si el formulario no es válido, los errores se agregarán al formulario
    return render(request, "signup.html", {"form": form})


def singin(request):
    """
    Función que permite a un usuario iniciar sesión en el sistema.

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que se enviará al cliente.

    Raises:
        ValidationError: Si el usuario o la contraseña son incorrectos.
    """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect("home")
            else:
                messages.error(request, 
                               "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, 
                           "Por favor corrija los errores en el formulario.")
    else:
        form = LoginForm(request)
    return render(request, "signin.html", {"form": form})


def signout(request):
    """
    Función que permite a un usuario cerrar sesión en el sistema.

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que se enviará al cliente.
    """
    logout(request)
    messages.success(request, "Cierre de sesión exitoso.")
    return redirect("home")


def password_reset_request(request):
    """
    Vista para manejar solicitudes de restablecimiento de contraseña.

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que renderiza el formulario de solicitud
        de restablecimiento de contraseña o redirige después de enviar 
        el correo.
    """
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    # Genera una contraseña temporal segura
                    temporary_password = (
                        PasswordResetRequestForm.generate_temporary_password()
                    )
                    user.password = make_password(str(temporary_password))

                    # Guarda la contraseña temporal en la base de datos
                    user.save()

                    # Obtener el nombre de usuario
                    username = user.username

                    # Envíar la contraseña temporal al correo del usuario
                    send_password_reset_email(email, 
                                              username, 
                                              str(temporary_password))

            # Redirige al usuario a la página de restablecimiento de
            # contraseña enviada
            return redirect("password_reset_done")
    else:
        form = PasswordResetRequestForm()
    return render(request, "password_reset_form.html", {"form": form})


def password_reseted(request):
    """
    Vista que se muestra después de enviar un correo electrónico de
    restablecimiento de contraseña.

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de 
        restablecimiento de contraseña enviada.
    """
    return render(request, "password_reset_done.html")


@login_required
def change_password(request):
    """
    Vista para manejar el cambio de contraseña del usuario autenticado.

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que renderiza el formulario de cambio
        de contraseña o redirige después de cambiar la contraseña.
    """
    if request.method == "POST":
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            # Cambiar la contraseña del usuario
            new_password = form.cleaned_data.get("new_password2")
            request.user.set_password(new_password)
            request.user.save()

            # Actualizar la sesión evitar desconectar al usuario
            update_session_auth_hash(request, request.user)

            # Redirigir al usuario a la página de cambio de contraseña exitoso
            return redirect("password_change_done")
    else:
        # Enviar el formulario de cambio de contraseña a la vista
        form = ChangePasswordForm(user=request.user)
    return render(request, "change_password.html", {"form": form})


def changed_password(request):
    """
    Vista que se muestra después de cambiar la contraseña del usuario.

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de cambio de
        contraseña exitoso.
    """
    # Renderiza la página de cambio de contraseña exitoso
    return render(request, "changed_password.html")


@login_required
def my_account(request):
    """
    Vista para mostrar la información del usuario en la página "Mi Cuenta".

    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.

    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página "Mi Cuenta".
    """
    user = request.user
    return render(request, "my_account.html", {"user": user})


def search_vehicles(request):
    """
    Vista que maneja las solicitudes de búsqueda de vehículos para mostrarlas
    en la página de comparación de vehículos sin necesidad de recargar la 
    página.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        JsonResponse: Respuesta JSON que contiene los vehículos encontrados."""
    if request.method == 'POST':
        # Procesar los datos del formulario de búsqueda
        print(request.POST)
        
        vehicles = SEARCHER.search(query=request.POST).to_dict(orient='records')
        print(vehicles)
        # Devolver los resultados en formato JSON
        return JsonResponse({'vehicles': vehicles})
    else:
        # Manejar el caso en que la solicitud no sea POST
        return JsonResponse({'error': 'Método de solicitud no permitido'}, status=405)


def compare_vehicles(request):
    """
    Vista para la página de comparación de vehículos.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de comparación 
        de vehículos con los vehículos seleccionados.
    """
    if request.method == 'POST':
        print(request.POST)
        print(request.POST.getlist('selected_vehicles'))

    else:
        form = VehicleSearchForm(prefix='form')
        return render(request, 'compare.html', {'form': form})


def get_selected_vehicles(request):
    """
    Función que guarda los vehículos seleccionados por el usuario en la sesión.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        JsonResponse: Respuesta JSON que indica si la operación fue exitosa.
    """
    if request.method == 'POST':
        # Intenta cargar los datos JSON de la solicitud
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Guarda los datos en la sesión del usuario
        request.session['selected_vehicles'] = data
        request.session.save()
        
        # Redirige directamente a la página de análisis
        return JsonResponse({'success': True})
    

def update_selected_vehicles(request):
    """
    Función que actualiza los vehículos seleccionados por el usuario 
    en la sesión.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        JsonResponse: Respuesta JSON que indica si la operación fue exitosa.
    """
    if request.method == 'POST':
        selected_vehicles = request.POST.getlist('selected_vehicles[]')
        request.session['selected_vehicles'] = selected_vehicles
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Método de solicitud no permitido'}, status=405)


def analyze_selected_vehicles(request):
    """
    Función que analiza los vehículos seleccionados por el usuario y
    muestra los resultados en una página web.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de análisis de 
        vehículos seleccionados.
    """
    # Verificar si la solicitud es POST
    if request.method == 'POST':
        print("analyze_selected_vehicles")
        print(request.POST)
        return render(request, 'analyze_selected_vehicles.html')
    else:
        # Obtener los vehículos seleccionados de la sesión
        selected_vehicles = request.session.get('selected_vehicles', [])
        
        # Realizar el análisis de los vehículos seleccionados
        analysis = ANALYZER.analyze(
            selected_vehicles)

        # Definir las columnas que contienen valores de porcentaje
        columns_with_percentage = ['Rendimiento en ciudad (km/L)', 
                                   'Rendimiento en carretera (km/L)', 
                                   'Rendimiento combinado (km/L)',
                                   'Emisiones de CO2 (g/km)',
                                   'Emisiones de NOx (g/km)']
        
        return render(request, 
                      'analyze_selected_vehicles.html',
                      {'selected_vehicles': selected_vehicles,
                       'analysis_vehicles': analysis,
                        'columns_with_percentage': columns_with_percentage})
        

def calculate_fuel_cost(request):
    """
    Función que renderiza la página que calcula el costo de combustible 
    para un vehículo que hace determinada ruta.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de cálculo 
        de costo de combustible.
    """
    if request.method == 'POST':
        # Procesar los datos del formulario de cálculo de costo de combustible
        form = FuelCostForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            # Envía los datos del formulario al objeto CostCalculator
            fuel_cost = CALCULATOR.calculate(form.cleaned_data)
            
            # Redondear los valores de la respuesta
            fuel_cost['distance'] = int(fuel_cost['distance'])
            fuel_cost['cost'] = int(fuel_cost['cost'])
            fuel_cost['fuel'] = round(fuel_cost['fuel'], 2)
            
            # Renderiza la página con el resultado
            return render(request, 'fuel_cost.html', {'form': form,
                                                      'fuel_cost': fuel_cost})
        
    else:
        # Inicializar el formulario de cálculo de costo de combustible
        form = FuelCostForm()
        
        # Renderizar la página con el formulario
        return render(request, 'fuel_cost.html', {'form': form}) 
    

def data_policy(request):
    """
    Función que renderiza la página de la política de tratamiento 
    de datos personales.
    
    Args: 
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de política de 
        tratamiento de datos personales.
    """
    return render(request, 'data_policy.html')


def data_policy_en(request):
    """
    Función que renderiza la página de la política de tratamiento de datos
    personales en inglés.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de política de 
        tratamiento de datos personales en inglés.
    """
    return render(request, 'data_policy_en.html')


def create_vehicle(request):
    """
    Vista para crear un nuevo vehículo.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        HttpResponse: Respuesta HTTP que renderiza el formulario de creación 
        de un nuevo vehículo.
    """
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('analyze_vehicles')  # Redirigir a una página de éxito
    else:
        form = VehicleForm()
    return render(request, 'crear_vehiculo.html', {'form': form})


def create_route(request):
    """
    Vista para crear una nueva ruta.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        HttpResponse: Respuesta HTTP que renderiza el formulario de creación 
        de una nueva ruta.
    """
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            start_address = form.cleaned_data['start']
            end_address = form.cleaned_data['end']
            description = form.cleaned_data['description']
            
            # Geocodificar las direcciones para obtener las coordenadas
            start_coords = GEOUTILS.geocode_address(start_address)
            end_coords = GEOUTILS.geocode_address(end_address)
            
            # Guardar la ruta en la base de datos
            route = Route(owner=request.user, start=start_address, end=end_address,
                          start_coords=start_coords, end_coords=end_coords,
                          description=description)
            
            route.save()
            
            return redirect('heatmap')
    else:
        form = RouteForm()
    return render(request, 'crear_ruta.html', {'form': form})


def heatmap(request):
    """
    Renderiza la página de mapa de calor con las rutas de los usuarios.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
    
    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de mapa de calor.
    """
    # Obtener las rutas del usuario autenticado
    user_routes = Route.objects.filter(owner=request.user)
    
    # Crear un mapa de calor con las rutas del usuario
    m = GEOUTILS.heatmap(user_routes)
    
    return render(request, 'heatmap.html', {'map_html': m._repr_html_()})


def clustermap(request):
    """
    Renderiza la página de los centroides de las rutas de los usuarios.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
        
    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de centroides.
    """
    # Obtener el número de clusters especificado por el usuario
    num_clusters = int(request.GET.get('num_clusters', 5))
    
    # Obtener las rutas del usuario autenticado
    user_routes = Route.objects.filter(owner=request.user)
    
    # Verificar que el número de clusters sea menor o igual al número de rutas
    if num_clusters > user_routes.count():
        num_clusters = user_routes.count()
        
    # Crear el objeto mapa con los centroides de las rutas del usuario
    map_html = GEOUTILS.clustermap(user_routes, num_clusters)._repr_html_()
    
    # Renderizar la página de centroides
    return render(request, 'clustermap.html', {'map_html': map_html})
    
    
def analyze_vehicles(request):
    """
    Crea gráficas de análisis de vehículos del usuario.
    
    Args:
        request (HttpRequest): Solicitud HTTP que se recibe desde el cliente.
    
    Returns:
        HttpResponse: Respuesta HTTP que renderiza la página de análisis de
        vehículos.
    """
    # Obtener los vehículos del usuario autenticado
    user_vehicles = Vehicle.objects.filter(owner=request.user)
    
    # Generar las gráficas
    fuel_efficiency_bar_chart = DRAWER.fuel_efficiency_bar_chart(
        user_vehicles)
    vehicles_by_brand_pie_chart = DRAWER.vehicles_by_brand_pie_chart(
        user_vehicles)
    fuel_efficiency_distribution = DRAWER.fuel_efficiency_distribution(
        user_vehicles)
    
    # Convertir las gráficas a formato HTML
    fuel_efficiency_bar_chart_html = fuel_efficiency_bar_chart._repr_html_()
    vehicles_by_brand_pie_chart_html = vehicles_by_brand_pie_chart._repr_html_()
    fuel_efficiency_distribution_html = fuel_efficiency_distribution._repr_html_()
    
    # Renderizar la vista con las gráficas
    return render(request, 'analyze_vehicles.html', {
        'fuel_efficiency_bar_chart_html': fuel_efficiency_bar_chart_html,
        'vehicles_by_brand_pie_chart_html': vehicles_by_brand_pie_chart_html,
        'fuel_efficiency_distribution_html': fuel_efficiency_distribution_html
    })
        