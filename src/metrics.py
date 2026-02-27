"""
Módulo de cálculo de métricas publicitarias
Calcula GRPs, alcance, frecuencia e impresiones
"""

class MetricsCalculator:
    """Calcula métricas publicitarias para campañas de autobuses"""
    
    # Datos de audiencia por tipo de bus (personas/día)
    AUDIENCIA_POR_BUS = {
        'urbano': 350,  # Promedio de pasajeros por autobús urbano
        'interurbano': 150  # Promedio de pasajeros por autobús interurbano
    }
    
    # Factor de visibilidad por formato
    VISIBILIDAD_FORMATO = {
        'exterior_frontal': 1.0,
        'exterior_lateral': 0.8,
        'interior': 0.6,
        'digital': 1.2
    }
    
    def __init__(self):
        pass
    
    def calcular_audiencia_diaria(self, num_buses, tipo_bus):
        """
        Calcula la audiencia diaria total
        
        Args:
            num_buses: número de autobuses
            tipo_bus: 'urbano' o 'interurbano'
        
        Returns:
            int: audiencia diaria estimada
        """
        audiencia_base = self.AUDIENCIA_POR_BUS.get(tipo_bus.lower(), 0)
        return num_buses * audiencia_base
    
    def calcular_impresiones(self, audiencia_diaria, duracion_dias):
        """
        Calcula las impresiones totales
        
        Args:
            audiencia_diaria: audiencia por día
            duracion_dias: duración de la campaña en días
        
        Returns:
            int: impresiones totales
        """
        return audiencia_diaria * duracion_dias
    
    def calcular_grp(self, impresiones, universo=1000000):
        """
        Calcula GRPs (Gross Rating Points)
        GRP = (Impresiones / Universo) * 100
        
        Args:
            impresiones: número total de impresiones
            universo: población objetivo total
        
        Returns:
            float: GRP value
        """
        if universo == 0:
            return 0
        return (impresiones / universo) * 100
    
    def calcular_alcance_frecuencia(self, num_buses, duracion_dias, tipo_bus):
        """
        Estima alcance y frecuencia
        
        Args:
            num_buses: número de autobuses
            duracion_dias: duración en días
            tipo_bus: tipo de autobús
        
        Returns:
            tuple: (alcance_estimado, frecuencia)
        """
        # Alcance estimado (% de población expuesta)
        audiencia_diaria = self.calcular_audiencia_diaria(num_buses, tipo_bus)
        alcance_estimado = min(audiencia_diaria * duracion_dias * 0.3, 100)  # Cap at 100%
        
        # Frecuencia promedio (veces que ve el anuncio)
        frecuencia = duracion_dias * 0.8  # Asumiendo exposición variable
        
        return alcance_estimado, frecuencia
    
    def generar_resumen_campana(self, num_buses, tipo_bus, duracion_dias, formato, audiencia_universo=None):
        """
        Genera resumen completo de métricas para una campaña
        
        Args:
            num_buses: número de autobuses
            tipo_bus: 'urbano' o 'interurbano'
            duracion_dias: días de campaña
            formato: formato del anuncio
            audiencia_universo: población objetivo
        
        Returns:
            dict: resumen con todas las métricas
        """
        if audiencia_universo is None:
            audiencia_universo = 1000000
        
        audiencia_diaria = self.calcular_audiencia_diaria(num_buses, tipo_bus)
        impresiones = self.calcular_impresiones(audiencia_diaria, duracion_dias)
        grp = self.calcular_grp(impresiones, audiencia_universo)
        alcance, frecuencia = self.calcular_alcance_frecuencia(num_buses, duracion_dias, tipo_bus)
        
        return {
            'audiencia_diaria': audiencia_diaria,
            'impresiones_totales': impresiones,
            'grps': grp,
            'alcance_estimado': alcance,
            'frecuencia': frecuencia,
            'costo_por_impresion': 0.05,  # Valor por defecto
            'costo_total_estimado': impresiones * 0.05
        }