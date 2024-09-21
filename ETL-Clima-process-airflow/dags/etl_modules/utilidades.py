import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

def configurar_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cargar_configuracion():
    # Carga las variables de entorno desde el archivo credenciales.env
    load_dotenv('credenciales.env')
    
    return {
        'CLAVE_API': os.getenv("CLAVE_API"),
        'REDSHIFT_HOST': os.getenv('REDSHIFT_HOST'),
        'REDSHIFT_PORT': int(os.getenv('REDSHIFT_PORT', 5439)),  
        'REDSHIFT_DBNAME': os.getenv('REDSHIFT_DBNAME'),
        'REDSHIFT_USER': os.getenv('REDSHIFT_USER'),
        'REDSHIFT_PASSWORD': os.getenv('REDSHIFT_PASSWORD'),
        'EMAIL': os.getenv('EMAIL'),
        'EMAIL_PASSWORD': os.getenv('EMAIL_PASSWORD'),
        'TO_ADDRESS': os.getenv('TO_ADDRESS')
    }
    
def get_default_args():
    return {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2024, 9, 21),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }