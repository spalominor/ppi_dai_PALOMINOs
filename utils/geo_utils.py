import folium
import geopandas as gpd
import numpy as np
from scipy.cluster.vq import kmeans, vq
from folium.plugins import HeatMap


class GeoUtils:
    """
    Clase que contiene diversas funciones para trabajar con datos geográficos.
    """

    def geocode_address(self, address):
        """
        Geocodifica una dirección a partir de un string.

        Args:
            address (str): Dirección a geocodificar.

        Returns:
            Un string con las coordenadas de la dirección geocodificada.
            ('lat long')
        """
        try:
            point = gpd.tools.geocode(address)
        except ValueError:
            point = gpd.tools.geocode(address, provider="nominatim")
        finally:
            if point.empty:
                return "0 0"
            else:
                return f"{point.geometry.iloc[0].x} {point.geometry.iloc[0].y}"
            
    
    def heatmap(self, user_routes):
        """
        Crea un mapa de calor a partir de las rutas de un usuario.
        
        Args:
            user_routes (QuerySet): Rutas del usuario.
            
        Returns:
            Un objeto de tipo folium.Map con el mapa de calor.
        """
        # Extraer las coordenadas de inicio de las rutas del usuario
        coords = [(route.start_coords.y, route.start_coords.x) for route in user_routes]
        
        # Calcular el centro del mapa y el nivel de zoom
        center_lat = sum(lat for lat, lon in coords) / len(coords)
        center_lon = sum(lon for lat, lon in coords) / len(coords)
        zoom = 10  # Nivel de zoom inicial
        
        # Crear un GeoDataFrame con las coordenadas
        gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(*zip(*coords)))
        
        # Crear un mapa de Folium centrado en el centro calculado
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
        
        # Añadir una capa de mapa de calor
        HeatMap(data=gdf.geometry, radius=15).add_to(m)
        
        return m
    
    
    def clustermap(self, user_routes, num_clusters=1):
        """
        Crea un mapa con centroides de agruación de las rutas de un usuario.
        
        Args:
            user_routes (QuerySet): Rutas del usuario.
            
        Returns:
            Un objeto de tipo folium.Map con el mapa de calor.
        """
        
        # Extraer las coordenadas de inicio de las rutas del usuario
        coords = [(route.start_coords.y, 
                   route.start_coords.x) for route in user_routes]
        
        # Convertir las coordenadas a un array NumPy
        data = np.array(coords)
        
        # Calcular el centroide de todas las coordenadas
        center_lat = np.mean(data[:, 0])
        center_lon = np.mean(data[:, 1])
        
        # Aplicar el algoritmo de clustering K-Means
        # Número de clusters
        k = num_clusters  
        centroids, _ = kmeans(data, k)
        
        # Crear un mapa de Folium centrado en el centroide de las coordenadas
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        # Añadir marcadores en los centroides de los clusters
        for centroid in centroids:
            folium.Marker(location=[centroid[0], centroid[1]]).add_to(m)
