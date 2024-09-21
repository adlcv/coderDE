import psycopg2
import logging
from .utilidades import cargar_configuracion

def insertar_datos_en_redshift(datos_lista):
    if not isinstance(datos_lista, list):
        logging.error(f"Se esperaba una lista, pero se recibió: {type(datos_lista)}")
        return 0

    config = cargar_configuracion()
    
    conn_params = {
        'host': config['REDSHIFT_HOST'],
        'port': config['REDSHIFT_PORT'],
        'dbname': config['REDSHIFT_DBNAME'],
        'user': config['REDSHIFT_USER'],
        'password': config['REDSHIFT_PASSWORD']
    }
    
    inserted_count = 0
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                for datos in datos_lista:
                    if not isinstance(datos, dict):
                        logging.warning(f"Se esperaba un diccionario, pero se recibió: {type(datos)}")
                        continue

                    sql = """
                    INSERT INTO datos_clima 
                    (nombre_ciudad, temperatura, humedad, velocidad_viento, tiempo_medicion, fecha_carga,
                    clasificacion_clima, indice_comodidad, visibilidad, fase_del_dia, presion_atmosferica,
                    presion_categoria, indice_uv, categoria_uv, latitud, longitud, zona_horaria)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    try:
                        cur.execute(sql, (
                            datos.get('nombre_ciudad'),
                            datos.get('temperatura'),
                            datos.get('humedad'),
                            datos.get('velocidad_viento'),
                            datos.get('tiempo_medicion'),
                            datos.get('fecha_carga'),
                            datos.get('clasificacion_clima'),
                            datos.get('indice_comodidad'),
                            datos.get('visibilidad'),
                            datos.get('fase_del_dia'),
                            datos.get('presion_atmosferica'),
                            datos.get('presion_categoria'),
                            datos.get('indice_uv'),
                            datos.get('categoria_uv'),
                            datos.get('latitud'),
                            datos.get('longitud'),
                            datos.get('zona_horaria')
                        ))
                        inserted_count += 1
                    except KeyError as ke:
                        logging.error(f"Falta clave en los datos: {ke}")
                    except Exception as e:
                        logging.error(f"Error al insertar datos: {e}")

        logging.info(f"Se insertaron {inserted_count} registros exitosamente en Redshift")
    except Exception as e:
        logging.error(f"Error al conectar o insertar datos en Redshift: {str(e)}")
        raise

    return inserted_count