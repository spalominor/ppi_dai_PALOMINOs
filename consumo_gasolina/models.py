from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Vehicle(models.Model):
    """
    Modelo para almacenar la información de los vehículos de los usuarios.
    
    Atributos:
        owner (ForeignKey): Usuario propietario del vehículo.
        brand (CharField): Marca del vehículo.
        sub_brand (CharField): Submarca del vehículo.
        model_year (PositiveIntegerField): Año de fabricación del vehículo.
        version (CharField): Versión del vehículo.
        fuel_efficiency (FloatField): Rendimiento de combustible del vehículo.
        fuel_type (CharField): Tipo de combustible del vehículo.
        license_plate (CharField): Placa del vehículo.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    sub_brand = models.CharField(max_length=100)
    model_year = models.PositiveIntegerField()
    version = models.CharField(max_length=100)
    fuel_efficiency = models.FloatField()
    fuel_type = models.CharField(max_length=8)
    license_plate = models.CharField(max_length=20)

    def __str__(self):
        return f"brand:{self.brand} sub_brand:{self.sub_brand} version:{self.version} model_year:({self.model_year}) fuel_efficiency:{self.fuel_efficiency} fuel_type:{self.fuel_type} license_plate:{self.license_plate}"
    
    
class Route(models.Model):
    """
    Modelo para almacenar la información de las rutas de los usuarios.
    
    Atributos:
        owner (ForeignKey): Usuario creador de la ruta.
        start (CharField): Punto de inicio de la ruta.
        end (CharField): Punto de destino de la ruta.
        start_coords (CharField): Coordenadas del punto de inicio de la ruta.
        end_coords (CharField): Coordenadas del punto de destino de la ruta.
        date_created (DateTimeField): Fecha y hora de creación de la ruta.
        description (TextField): Descripción de la ruta.
        date_completed (DateTimeField): Fecha y hora de finalización de la ruta.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    start_coords = models.CharField(max_length=255)
    end_coords = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"start:{self.start} - end:{self.end} date_c({self.date_created}) date_f({self.date_completed}) start_coords:{self.start_coords} end_coords:{self.end_coords}"