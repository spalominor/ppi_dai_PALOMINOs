"""
URL configuration for flutasapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from consumo_gasolina import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search, name='home'),
    path('data_policy/', views.data_policy, name='data_policy'),
    path('data_policy_en/', views.data_policy_en, name='data_policy_en'),
    path('compare/', views.compare_vehicles, name='compare_vehicles'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.singin, name='login'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reseted, name='password_reset_done'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password/done/', views.changed_password, name='password_change_done'),
    path('logout/', views.signout, name='logout'),
    path('my_account/', views.my_account, name='my_account'),
    path('search_vehicles/', views.search_vehicles, name='search_vehicles'),
    path('get_selected_vehicles/', views.get_selected_vehicles, name='get_selected_vehicles'),
    path('compare/analyze/', views.analyze_selected_vehicles, name='analyze_selected_vehicles'),
    path('update_selected_vehicles/', views.update_selected_vehicles, name='update_selected_vehicles'),
    path('calculate_fuel_cost/', views.calculate_fuel_cost, name='calculate_fuel_cost'),
    path('crear-vehiculo/', views.create_vehicle, name='crear_vehiculo'),
    path('crear-ruta/', views.create_route, name='crear_ruta'),
    path('heatmap/', views.heatmap, name='heatmap'),
    path('clustermap/', views.clustermap, name='clustermap'),
    path('analyze-vehicles/', views.analyze_vehicles, name='analyze_vehicles'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
