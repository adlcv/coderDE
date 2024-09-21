import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .utilidades import cargar_configuracion

# Definimos los límites para las alertas
LIMITES_ALERTA = {
    'temperatura': {'max': 35, 'min': 0},
    'indice_uv': {'max': 8}
}

def verificar_alertas(datos_clima):
    alertas = []
    
    if datos_clima['temperatura'] > LIMITES_ALERTA['temperatura']['max']:
        alertas.append(f"Alerta de temperatura alta: {datos_clima['temperatura']}°C")
    elif datos_clima['temperatura'] < LIMITES_ALERTA['temperatura']['min']:
        alertas.append(f"Alerta de temperatura baja: {datos_clima['temperatura']}°C")
    
    if datos_clima['indice_uv'] > LIMITES_ALERTA['indice_uv']['max']:
        alertas.append(f"Alerta de índice UV alto: {datos_clima['indice_uv']}")
    
    return alertas

def crear_contenido_email(datos_ciudades, total_registros):
    contenido = f"""
    <html>
    <body>
        <h2>Reporte de Carga de Datos Climáticos</h2>
        <p>Se han cargado exitosamente {total_registros} registros en Redshift.</p>
        <h3>Resumen de Alertas por Ciudad:</h3>
    """
    
    for datos in datos_ciudades:
        alertas = verificar_alertas(datos)
        if alertas:
            contenido += f"""
            <h4>{datos['nombre_ciudad']}</h4>
            <ul>
                <li>Temperatura: {datos['temperatura']}°C</li>
                <li>Índice UV: {datos['indice_uv']} ({datos['categoria_uv']})</li>
                <li>Alertas: {'<br>'.join(alertas)}</li>
            </ul>
            """
    
    contenido += """
        <p>El proceso de extracción y carga a Redshift ha sido realizado con éxito.</p>
    </body>
    </html>
    """
    return contenido

def enviar_email(from_address, to_address, subject, html_content, password):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Email enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el email: {str(e)}")

def enviar_reporte_y_alertas(datos_ciudades, total_registros):
    config = cargar_configuracion()
    
    subject = "Reporte de Carga de Datos Climáticos y Alertas"
    from_address = config['EMAIL']
    password = config['EMAIL_PASSWORD']
    to_address = config['TO_ADDRESS']

    html_content = crear_contenido_email(datos_ciudades, total_registros)
    
    enviar_email(from_address, to_address, subject, html_content, password)

# Esta función será llamada desde el DAG
def procesar_y_enviar_email(datos_ciudades, total_registros):
    enviar_reporte_y_alertas(datos_ciudades, total_registros)