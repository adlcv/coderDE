import requests
from datetime import datetime
import logging
import os
from airflow.models import Variable
from .utilidades import cargar_configuracion

def obtener_datos_clima_todas_ciudades():
    logging.info("Iniciando obtener_datos_clima_todas_ciudades")
    
    config = cargar_configuracion()
    clave_api = config['CLAVE_API']
    
    # Imprimir el directorio de trabajo actual y su contenido
    current_dir = os.getcwd()
    logging.info(f"Directorio actual: {current_dir}")
    logging.info(f"Contenido del directorio actual: {os.listdir(current_dir)}")
    
    # Intentar obtener la ruta del archivo desde una variable de Airflow
    nombre_archivo_ciudades = Variable.get("CIUDADES_FILE", "/opt/airflow/dags/ciudades.txt")
    logging.info(f"Ruta del archivo de ciudades: {nombre_archivo_ciudades}")
    
    # Verificar si el archivo existe
    if not os.path.exists(nombre_archivo_ciudades):
        logging.error(f"El archivo {nombre_archivo_ciudades} no existe")
        raise FileNotFoundError(f"No se pudo encontrar el archivo {nombre_archivo_ciudades}")
    
    def leer_ciudades(nombre_archivo):
        logging.info(f"Intentando leer el archivo: {nombre_archivo}")
        ciudades = []
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                partes = linea.strip().split(',')
                if len(partes) == 3:
                    nombre = partes[0].strip()
                    lat = float(partes[1].strip())
                    lon = float(partes[2].strip())
                    ciudades.append((nombre, (lat, lon)))
        logging.info(f"Se leyeron {len(ciudades)} ciudades")
        return ciudades
    
    def obtener_datos_clima_ciudad(nombre_ciudad, lat, lon):
        url_base = "https://api.openweathermap.org/data/3.0/onecall"
        parametros = {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,hourly,daily,alerts",
            "appid": clave_api,
            "units": "metric"
        }
        
        respuesta = requests.get(url_base, params=parametros)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            datos_filtrados = {
                'nombre_ciudad': nombre_ciudad,
                'current': datos['current'],
                'timezone': datos['timezone'],
                'lat': datos['lat'],
                'lon': datos['lon']
            }
            datos_filtrados['fecha_carga'] = datetime.now()
            return datos_filtrados
        else:
            logging.error(f"Error al obtener datos para {nombre_ciudad}. Código de estado: {respuesta.status_code}")
            return None

    ciudades = leer_ciudades(nombre_archivo_ciudades)
    resultados = []
    for nombre, (lat, lon) in ciudades:
        datos = obtener_datos_clima_ciudad(nombre, lat, lon)
        if datos:
            resultados.append(datos)
    
    logging.info(f"Se obtuvieron datos para {len(resultados)} ciudades")
    return resultados