import numpy as np
import geopandas as gpd
from scipy.spatial import distance


class CostCalculator():
    """
    Calcula el costo de viajar entre dos puntos.
    
    Atributos:
    
    """
    # Definir el precio del combustible según el tipo [$/L] [1gal = 3.79 L]
    # 15.000 y 10.000 pesos el galón de gasolina y diesel respectivamente
    PRECIO_COMBUSTIBLE = {'gasolina': 3950, 'diesel': 2650}
    
    
    def _is_null_query(self, query: dict) -> bool:
        """
        Verifica si la consulta es nula.
        
        Args:
            query (dict): Consulta a verificar.
        
        Returns:
            bool: Verdadero si la consulta es nula, falso de lo contrario.
        """
        if query['start_address'] == '':
            return True
        elif query['end_address'] == '':
            return True
        elif query['fuel_type'] == '':
            return True
        elif query['fuel_efficiency'] == '' or query['fuel_efficiency'] == 0:
            return True
        elif query['fuel_efficiency'] is None:
            return True
        else:
            return False
    
    
    def _calculate_distance(self, direccion_inicio: str, 
                            direccion_destino: str) -> float:
        """
        Calcula la distancia entre dos puntos. Geocodifica los puntos a 
        coordenadas cartesianas y calcula la distancia de Manhattan
        entre ellos.
        
        Args:
            direccion_inicio (str): Dirección de inicio.
            direccion_destino (str): Dirección de destino.
        
        Returns:
            float: Distancia entre los dos puntos.
        """
        # Cargar los datos de las direcciones de inicio y destino
        try:
            start_point = gpd.tools.geocode(direccion_inicio)
            end_point = gpd.tools.geocode(direccion_destino)
        except ValueError:
            start_point = gpd.tools.geocode(direccion_inicio, 
                                            provider='nominatim')
            end_point = gpd.tools.geocode(direccion_destino,
                                            provider='nominatim')
            print("ValueError", ValueError)
        finally:
            if start_point.empty or end_point.empty:
                return 0.0
            
        # Obtener las coordenadas en grados decimales
        start_coords = (start_point.geometry.iloc[0].x, 
                        start_point.geometry.iloc[0].y)
        print("start_coords", start_coords)
        end_coords = (end_point.geometry.iloc[0].x, 
                      end_point.geometry.iloc[0].y)

        # Calcular la distancia de Manhattan en grados
        dist_deg = distance.cityblock(start_coords, end_coords)

        # Convertir la distancia de grados a kilómetros (aproximadamente)
        dist_km = dist_deg * 111.32
        
        return dist_km
    
    
    def calculate(self, query: dict) -> float:
        """
        Calcula el costo de combustible para viajar una distancia dada.
        
        Args:
            distancia (float): Distancia a recorrer.
            precio_combustible (float): Precio del combustible.
        
        Returns:
            float: Costo de combustible para recorrer la distancia dada.
        """
        # Obtener los datos discriminados de la consulta
        if self._is_null_query(query):
            print("Consulta nula")
            return {'distance': '', 
                    'fuel': '',
                    'cost': '',
                    'fuel_type': ''}
        else:
            distancia = self._calculate_distance(query['start_address'], 
                                                 query['end_address'])
            tipo_combustible = query['fuel_type']
            rendimiento = query['fuel_efficiency']
        
        # Calcular el combustible necesario para recorrer la distancia
        combustible = distancia / rendimiento
        
        # Obtener el precio del combustible según el tipo
        precio_combustible = self.PRECIO_COMBUSTIBLE[tipo_combustible]
        
        # Calcular el costo de combustible
        costo_combustible = precio_combustible * combustible
        
        response = {'distance': distancia, 
                    'fuel': combustible,
                    'cost': costo_combustible,
                    'fuel_type': tipo_combustible}
        
        print(response)
        return response