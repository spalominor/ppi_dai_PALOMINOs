"""
Módulo que contiene la clase Drawer, la cual contiene diversas funciones
para dibujar gráficos a partir de datos de los vehículos de los usuarios.

Clase:
    Drawer
    
Metodos:
    fuel_efficiency_bar_chart(vehicles): Crea un gráfico de barras con el 
    rendimiento de combustible de los vehículos.
    
    vehicles_by_brand_pie_chart(vehicles): Crea un gráfico de pastel con la 
    distribución de vehículos por marca.
    
    fuel_efficiency_distribution(vehicles): Crea un gráfico de barras con la 
    distribución de rendimiento de combustible de los vehículos.
    
Dependencias:
    - numpy
    - matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt



class Drawer:
    """
    Clase que contiene diversas funciones para dibujar gráficos a 
    partir de datos de los vehículos de los usuarios.
    
    Atributos:
        None
        
    Métodos:
        fuel_efficiency_bar_chart(vehicles): Crea un gráfico de barras con el 
        rendimiento de combustible de los vehículos.
        
        vehicles_by_brand_pie_chart(vehicles): Crea un gráfico de pastel con 
        la distribución de vehículos por marca.
        
        fuel_efficiency_distribution(vehicles): Crea un gráfico de barras con 
        la distribución de rendimiento de combustible de los vehículos.
    """
    def __init__(self):
        """
        Constructor de la clase Drawer. Se inicializan los atributos.
        De momento esta como parte de tener buena practica de programación.
        
        Args:
            None
            
        Returns:
            None
        """
        pass

    def fuel_efficiency_bar_chart(self, vehicles):
        """
        Crea un gráfico de barras con el rendimiento de combustible de los 
        vehículos.
        
        Args:
            vehicles (list): Lista de objetos de tipo Vehicle.
            
        Returns:
            Un objeto de tipo matplotlib.pyplot con el gráfico de barras.
        """
        # Extraer las marcas y rendimientos de combustible de los vehículos
        brands = [vehicle.brand for vehicle in vehicles]
        fuel_efficiencies = [vehicle.fuel_efficiency for vehicle in vehicles]

        # Crear el gráfico de barras
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(fuel_efficiencies)), fuel_efficiencies, 
                tick_label=brands)
        plt.xlabel('Marca del Vehículo')
        plt.ylabel('Rendimiento de Combustible (km/L)')
        plt.title('Rendimiento de Combustible por Marca de Vehículo')
        plt.xticks(rotation=45)
        plt.tight_layout()

        return plt

    def vehicles_by_brand_pie_chart(self, vehicles):
        """
        Crear un gráfico de pastel con la distribución de vehículos por marca.
        
        Args:
            vehicles (list): Lista de objetos de tipo Vehicle.
            
        Returns:
            Un objeto de tipo matplotlib.pyplot con el gráfico de pastel.
        """
        brands = [vehicle.brand for vehicle in vehicles]
        brand_counts = {brand: brands.count(brand) for brand in set(brands)}

        plt.figure(figsize=(8, 8))
        plt.pie(
            brand_counts.values(), 
            labels=brand_counts.keys(), autopct='%1.1f%%')
        plt.title('Porcentaje de Vehículos por Marca')
        plt.tight_layout()

        return plt

    def fuel_efficiency_distribution(self, vehicles):
        """
        Crea un gráfico de barras con la distribución de rendimiento de
        combustible de los vehículos.
        
        Args:
            vehicles (list): Lista de objetos de tipo Vehicle.
            
        Returns:
            Un objeto de tipo matplotlib.pyplot con el gráfico de barras.
        """
        fuel_efficiencies = [vehicle.fuel_efficiency for vehicle in vehicles]
        vehicle_plates = [vehicle.license_plate for vehicle in vehicles]

        # Calcular estadísticas
        indice_min = np.argmin(fuel_efficiencies)
        indice_max = np.argmax(fuel_efficiencies)
        rendimiento_promedio = round(np.mean(fuel_efficiencies), 2)
        rendimiento_mediana = round(np.median(fuel_efficiencies), 2)

        # Plotting
        fig = plt.figure(figsize=(10, 6))
        plt.bar(vehicle_plates, fuel_efficiencies, 
                color='skyblue', edgecolor='black', alpha=0.7)
        plt.axhline(rendimiento_promedio, 
                    color='red', linestyle='dashed', 
                    linewidth=1, label='Media')
        plt.axhline(rendimiento_mediana, 
                    color='green', linestyle='dashed', 
                    linewidth=1, label='Mediana')
        
        # Añadir títulos y etiquetas
        plt.title('Distribución de Rendimiento de Combustible')
        plt.xlabel('Vehículo (placa)')
        plt.ylabel('Rendimiento (km/L)')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.grid(True)

        # Añadir anotaciones para el menor rendimiento
        plt.annotate(f'Menor: {min(fuel_efficiencies)} km/L',
                     xy=(indice_min, min(fuel_efficiencies)),
                     xytext=(indice_min + 2, min(fuel_efficiencies) + 3),
                     arrowprops=dict(facecolor='red', shrink=0.05))

        # Añadir anotaciones para el mayor rendimiento
        plt.annotate(f'Mayor: {max(fuel_efficiencies)} km/L',
                     xy=(indice_max, max(fuel_efficiencies)),
                     xytext=(indice_max + 2, max(fuel_efficiencies) + 3),
                     arrowprops=dict(facecolor='green', shrink=0.05))

        plt.ylim(min(fuel_efficiencies) - 10, max(fuel_efficiencies) + 20)

        return fig