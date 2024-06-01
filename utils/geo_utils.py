import folium
import geopandas as gpd
import numpy as np
from folium.plugins import MarkerCluster
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
        coords = []
        
        # Iterar sobre las rutas del usuario y extraer las coordenadas de inicio y fin
        for route in user_routes:
            start_coords = route.start_coords.split()
            end_coords = route.end_coords.split()
            coords.append((float(start_coords[1]), float(start_coords[0])))
            coords.append((float(end_coords[1]), float(end_coords[0])))
            
        
        # Crear un GeoDataFrame a partir de las coordenadas
        gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(
            [coord[1] for coord in coords], 
            [coord[0] for coord in coords]
        ))

        # Centrar el mapa en el medio de todas las rutas
        centroid = gdf.unary_union.centroid
        m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10)

        # Agregar el mapa de calor
        HeatMap(data=[[point.y, point.x] for point in gdf.geometry], radius=15).add_to(m)
        
        return m
    
    
    def clustermap(self, user_routes, num_clusters=1):
        """
        Crea un mapa con centroides de agruación de las rutas de un usuario.
        
        Args:
            user_routes (QuerySet): Rutas del usuario.
            
        Returns:
            Un objeto de tipo folium.Map con el mapa de calor.
        """
        # Crear una lista para almacenar las coordenadas
        coordinates = []

        # Iterar sobre las rutas del usuario y extraer las coordenadas de inicio y fin
        for route in user_routes:
            start_coords = route.start_coords.split()
            end_coords = route.end_coords.split()
            coordinates.append([float(start_coords[1]), float(start_coords[0])])
            coordinates.append([float(end_coords[1]), float(end_coords[0])])

        # Convertir las coordenadas a un GeoDataFrame
        gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(
            [coord[1] for coord in coordinates], 
            [coord[0] for coord in coordinates]
        ))

        # Aplicar KMeans de SciPy para encontrar clústeres
        num_clusters = num_clusters
        centroids, _ = kmeans([point.coords[0] for point in gdf.geometry], num_clusters)
        
        # Centrar el mapa en el medio de todas las rutas
        map_center = gdf.unary_union.centroid
        m = folium.Map(location=[map_center.y, map_center.x], zoom_start=10)

        # Añadir los centroides al mapa
        for centroid in centroids:
            folium.Marker(
                location=[centroid[1], centroid[0]], 
                popup="Centroide de clúster",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

        # Crear un objeto de MarkerCluster
        marker_cluster = MarkerCluster().add_to(m)

        # Añadir los puntos al clúster
        for coord in coordinates:
            folium.Marker(location=coord).add_to(marker_cluster)
            
        return m
