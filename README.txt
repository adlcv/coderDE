# ETL Pipeline de Datos Climáticos

Este proyecto implementa un pipeline ETL (Extracción, Transformación, Carga) para datos climáticos utilizando Apache Airflow, Docker y Amazon Redshift.

## Requisitos previos

- Docker y Docker Compose
- Python 3.8+
- Cuenta de Amazon Web Services (AWS) con acceso a Redshift
- Cuenta de correo electrónico para envío de alertas

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/etl-clima-project.git
   cd etl-clima-project
   ```

2. Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
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

3. Construir y levantar los contenedores de Docker:
   ```
   docker-compose up -d
   ```

4. Inicializar la base de datos de Airflow:
   ```
   docker-compose run airflow-init
   ```

## Configuración

1. Acceder a la interfaz web de Airflow en `http://localhost:8080` (usuario: airflow, contraseña: airflow).

2. En Airflow, ir a Admin > Connections y agregar una nueva conexión:
   - Conn Id: redshift_default
   - Conn Type: Amazon Redshift
   - Host: [Tu host de Redshift]
   - Schema: [Tu schema de Redshift]
   - Login: [Tu usuario de Redshift]
   - Password: [Tu contraseña de Redshift]
   - Port: 5439

3. En Admin > Variables, agregar:
   - Key: CIUDADES_FILE
   - Value: /opt/airflow/dags/ciudades.txt

## Ejecución

1. En la interfaz web de Airflow, buscar el DAG "clima_etl_dag".

2. Activar el DAG haciendo clic en el botón de encendido.

3. Para ejecutar el DAG manualmente, hacer clic en el botón "Trigger DAG".

4. Monitorear la ejecución en la vista de árbol o gráfico del DAG.

## Estructura del proyecto

- `dags/`: Contiene los archivos DAG de Airflow y módulos ETL.
- `logs/`: Almacena los logs de Airflow.
- `plugins/`: Para plugins personalizados de Airflow (si los hay).
- `docker-compose.yaml`: Configura los servicios de Docker.
- `Dockerfile`: Define la imagen de Docker para Airflow.

