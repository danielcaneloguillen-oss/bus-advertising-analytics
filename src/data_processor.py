"""
Módulo para procesar datos de Excel
Lee y valida campañas publicitarias desde archivos Excel
"""

import pandas as pd
from datetime import datetime, timedelta
from src.metrics import MetricsCalculator


class ExcelProcessor:
    """Procesa datos de campaña desde archivos Excel"""
    
    def __init__(self):
        self.calculator = MetricsCalculator()
        self.required_columns = [
            'numero_buses',
            'tipo_bus',
            'formato',
            'fecha_inicio',
            'fecha_fin'
        ]
    
    def validar_datos(self, df):
        """
        Valida que el DataFrame tenga las columnas necesarias
        
        Args:
            df: DataFrame a validar
        
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        columnas_faltantes = [col for col in self.required_columns if col not in df.columns]
        
        if columnas_faltantes:
            return False, f"Columnas faltantes: {', '.join(columnas_faltantes)}"
        
        # Validar tipos de bus
        tipos_invalidos = df[~df['tipo_bus'].isin(['urbano', 'interurbano'])]['tipo_bus'].unique()
        if len(tipos_invalidos) > 0:
            return False, f"Tipos de bus no válidos: {', '.join(tipos_invalidos)}"
        
        return True, "Datos válidos"
    
    def procesar_excel(self, archivo):
        """
        Procesa un archivo Excel con datos de campaña
        
        Args:
            archivo: archivo Excel (BytesIO o ruta)
        
        Returns:
            DataFrame: datos procesados con métricas calculadas
        """
        try:
            df = pd.read_excel(archivo)
        except Exception as e:
            raise Exception(f"Error al leer el archivo: {str(e)}")
        
        # Validar datos
        es_valido, mensaje = self.validar_datos(df)
        if not es_valido:
            raise Exception(mensaje)
        
        # Procesar fechas
        df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'])
        df['fecha_fin'] = pd.to_datetime(df['fecha_fin'])
        df['duracion_dias'] = (df['fecha_fin'] - df['fecha_inicio']).dt.days + 1
        
        # Calcular métricas para cada fila
        metricas = []
        for idx, row in df.iterrows():
            try:
                resumen = self.calculator.generar_resumen_campana(
                    num_buses=int(row['numero_buses']),
                    tipo_bus=row['tipo_bus'].lower(),
                    duracion_dias=int(row['duracion_dias']),
                    formato=row['formato'],
                    audiencia_universo=None
                )
                metricas.append(resumen)
            except Exception as e:
                raise Exception(f"Error en fila {idx + 1}: {str(e)}")
        
        # Crear DataFrame con métricas
        df_metricas = pd.DataFrame(metricas)
        
        # Combinar datos originales con métricas
        df_resultados = pd.concat([df.reset_index(drop=True), df_metricas], axis=1)
        
        return df_resultados
    
    def generar_reporte_excel(self, df_datos, ruta_salida):
        """
        Genera un archivo Excel con los resultados
        
        Args:
            df_datos: DataFrame con datos y métricas
            ruta_salida: ruta donde guardar el archivo
        
        Returns:
            str: ruta del archivo generado
        """
        with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
            # Hoja de datos completos
            df_datos.to_excel(writer, sheet_name='Campañas', index=False)
            
            # Hoja de resumen
            resumen = pd.DataFrame({
                'Métrica': [
                    'Total Impresiones',
                    'Alcance Estimado',
                    'GRPs Promedio',
                    'Frecuencia Promedio',
                    'Número de Campañas'
                ],
                'Valor': [
                    f"{df_datos['impresiones_totales'].sum():,.0f}",
                    f"{df_datos['alcance_estimado'].sum():,.0f}",
                    f"{df_datos['grps'].mean():.2f}",
                    f"{df_datos['frecuencia'].mean():.2f}",
                    len(df_datos)
                ]
            })
            resumen.to_excel(writer, sheet_name='Resumen', index=False)
        
        return ruta_salida