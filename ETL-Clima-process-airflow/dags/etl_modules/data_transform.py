from datetime import datetime

def clasificar_clima(temp, humidity):
    if temp > 25:
        temp_class = "Cálido"
    elif temp < 10:
        temp_class = "Frío"
    else:
        temp_class = "Templado"
    
    if humidity > 70:
        humidity_class = "Húmedo"
    elif humidity < 30:
        humidity_class = "Seco"
    else:
        humidity_class = "Normal"
    
    return f"{temp_class} y {humidity_class}"

def calcular_indice_comodidad(temp, humidity, wind_speed):
    # Fórmula simplificada para el índice de comodidad
    return 0.5 * (temp + 61.0 + ((temp-68.0)*1.2) + (humidity*0.094)) - (wind_speed * 0.3)

def clasificar_visibilidad(visibility):
    if visibility >= 10000:
        return "Excelente"
    elif visibility >= 5000:
        return "Buena"
    elif visibility >= 1000:
        return "Moderada"
    else:
        return "Pobre"

def clasificar_presion(pressure):
    if pressure < 1000:
        return "Baja"
    elif pressure > 1020:
        return "Alta"
    else:
        return "Normal"

def clasificar_uv(uvi):
    if uvi <= 2:
        return "Bajo"
    elif uvi <= 5:
        return "Moderado"
    elif uvi <= 7:
        return "Alto"
    elif uvi <= 10:
        return "Muy Alto"
    else:
        return "Extremo"

def transformar_datos_clima(datos):
    actual = datos['current']
    
    temp = actual['temp']
    humidity = actual['humidity']
    wind_speed = actual['wind_speed']
    
    return {
        'nombre_ciudad': datos['nombre_ciudad'],
        'temperatura': datos['current']['temp'],
        'humedad': datos['current']['humidity'],
        'velocidad_viento': datos['current']['wind_speed'],
        'tiempo_medicion': datetime.fromtimestamp(datos['current']['dt']),
        'fecha_carga': datos['fecha_carga'],
        'clasificacion_clima': clasificar_clima(datos['current']['temp'], datos['current']['humidity']),
        'indice_comodidad': calcular_indice_comodidad(datos['current']['temp'], datos['current']['humidity'], datos['current']['wind_speed']),
        'visibilidad': clasificar_visibilidad(datos['current'].get('visibility', 0)),
        'fase_del_dia': 'Día' if datos['current']['dt'] > datos['current'].get('sunrise', 0) and datos['current']['dt'] < datos['current'].get('sunset', 0) else 'Noche',
        'presion_atmosferica': datos['current']['pressure'],
        'presion_categoria': clasificar_presion(datos['current']['pressure']),
        'indice_uv': datos['current']['uvi'],
        'categoria_uv': clasificar_uv(datos['current']['uvi']),
        'latitud': datos['lat'],
        'longitud': datos['lon'],
        'zona_horaria': datos['timezone']
    }