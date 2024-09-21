# ETL Pipeline de Datos Climáticos

Este proyecto implementa un pipeline ETL (Extracción, Transformación, Carga) para datos climáticos utilizando Apache Airflow, Docker y Amazon Redshift.

## Requisitos previos

- Docker y Docker Compose
- Python 3.8+
- Cuenta de Amazon Web Services (AWS) con acceso a Redshift
- Cuenta de correo electrónico para envío de alertas
- [Task](https://taskfile.dev/#/installation) instalado en tu sistema

## Instalación y Ejecución

1. Clonar el repositorio:
   ```
   git clone https://github.com/adlcv/coderDE.git
   cd coderDE
   ```

2. Crear un archivo `.env` en la raíz del proyecto (ver sección "Configuración de Variables de Entorno").

3. Preparar el proyecto:
   ```
   task pre_project
   ```

4. Iniciar los servicios:
   ```
   task start_project
   ```

5. Ver la lista de DAGs disponibles:
   ```
   task list_dags
   ```

6. Ejecutar el DAG:
   ```
   task trigger_dag
   ```

7. Detener los servicios cuando hayas terminado:
   ```
   task down_project
   ```

## Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
AIRFLOW_UID=50000
REDSHIFT_HOST=tu-cluster.xxxxxxxxxxxx.us-west-2.redshift.amazonaws.com
REDSHIFT_PORT=5439
REDSHIFT_DBNAME=tu_base_de_datos
REDSHIFT_USER=tu_usuario
REDSHIFT_PASSWORD=tu_contraseña
EMAIL=tu_correo@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_correo
TO_ADDRESS=correo_destino@ejemplo.com
CLAVE_API=tu_clave_api_openweathermap
```

Asegúrate de reemplazar los valores con tus propias credenciales y configuraciones.

## Estructura del proyecto

- `dags/`: Contiene los archivos DAG de Airflow y módulos ETL.
- `logs/`: Almacena los logs de Airflow.
- `plugins/`: Para plugins personalizados de Airflow (si los hay).
- `docker-compose.yaml`: Configura los servicios de Docker.
- `Taskfile.yml`: Define las tareas para gestionar el proyecto.

## Solución de problemas

- Si encuentras problemas de permisos, asegúrate de que AIRFLOW_UID en .env coincida con tu UID local.
- Para ver los logs de los contenedores: `docker-compose logs [nombre-del-servicio]`
- Si el DAG falla, revisa los logs en la interfaz de Airflow para más detalles.

## Mantenimiento

- Regularmente, actualiza las dependencias y la imagen de Airflow.
- Monitorea el uso de recursos en Redshift y escala si es necesario.
- Revisa y actualiza las ciudades en `ciudades.txt` según sea necesario.





