"""
Configuración de la aplicación
"""

# Configuración de la aplicación
APP_NAME = "Bus Advertising Analytics"
APP_VERSION = "1.0.0"

# Configuración de rutas
UPLOAD_FOLDER = "uploads"
EXPORT_FOLDER = "exports"

# Configuración de métricas
DEFAULT_UNIVERSE = 1000000  # Población objetivo por defecto
COST_PER_IMPRESSION = 0.05  # Costo por impresión en euros

# Tipos de buses válidos
VALID_BUS_TYPES = ['urbano', 'interurbano']

# Formatos válidos
VALID_FORMATS = [
    'exterior_frontal',
    'exterior_lateral',
    'interior',
    'digital'
]

# Configuración de Streamlit
STREAMLIT_CONFIG = {
    'theme': 'light',
    'layout': 'wide'
}