from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl_modules.data_extract import obtener_datos_clima_todas_ciudades
from etl_modules.data_transform import transformar_datos_clima
from etl_modules.data_load import insertar_datos_en_redshift
from etl_modules.mail_sender import procesar_y_enviar_email
from etl_modules.utilidades import get_default_args
import logging

default_args = get_default_args()

with DAG(
    'clima_etl_dag',
    default_args=default_args,
    description='ETL para datos de clima',
    schedule_interval=timedelta(days=1),
) as dag:

    def extract_wrapper(**kwargs):
        try:
            return obtener_datos_clima_todas_ciudades()
        except Exception as e:
            logging.error(f"Error en la extracción de datos: {str(e)}")
            raise

    extract_task = PythonOperator(
        task_id='extraer_datos_clima',
        python_callable=extract_wrapper,
    )

    def transform_data(**kwargs):
        ti = kwargs['ti']
        datos_extraidos = ti.xcom_pull(task_ids='extraer_datos_clima')
        datos_transformados = [transformar_datos_clima(datos) for datos in datos_extraidos]
        ti.xcom_push(key='datos_transformados', value=datos_transformados)
        return len(datos_transformados)

    transform_task = PythonOperator(
        task_id='transformar_datos_clima',
        python_callable=transform_data,
    )

    def load_data(**kwargs):
        ti = kwargs['ti']
        datos_transformados = ti.xcom_pull(key='datos_transformados', task_ids='transformar_datos_clima')
        total_registros = insertar_datos_en_redshift(datos_transformados)
        ti.xcom_push(key='total_registros', value=total_registros)
        return total_registros

    load_task = PythonOperator(
        task_id='cargar_datos_redshift',
        python_callable=load_data,
    )

    def enviar_email(**kwargs):
        ti = kwargs['ti']
        datos_transformados = ti.xcom_pull(key='datos_transformados', task_ids='transformar_datos_clima')
        total_registros = ti.xcom_pull(key='total_registros', task_ids='cargar_datos_redshift')
        
        if not datos_transformados or not isinstance(datos_transformados, list):
            logging.error(f"Datos transformados no válidos: {datos_transformados}")
            return
        
        procesar_y_enviar_email(datos_transformados, total_registros)

    email_task = PythonOperator(
        task_id='enviar_email',
        python_callable=enviar_email,
    )

    extract_task >> transform_task >> load_task >> email_task