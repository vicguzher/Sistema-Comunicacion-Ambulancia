import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import geojson

# Configuración de InfluxDB
url = "http://localhost:8086"  # URL del servidor InfluxDB
token = "6Ob2rVzxmQtNQKMfr1n-kqfALCFRL-CQoyvJEWpsp5Ffsry-JAfaOx4BNgSuU_3059pqJ9bM5flcQlSoJpRnqw=="  # Token de autenticación de InfluxDB
org = "US"  # Nombre de la organización en InfluxDB
bucket = "pulso"  # Nombre del bucket en InfluxDB

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Definir algunas funciones de callback para los eventos de conexión, suscripción, y recepción de mensajes
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
        # Una vez conectado, suscríbete al tema (topic) que desees
        client.subscribe("pulso")
        client.subscribe("coordenadas")
    else:
        print(f"Fallo en la conexión al broker MQTT. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    # Esta función se ejecutará cada vez que se reciba un mensaje en el tema suscrito
    print(f"Mensaje recibido en el topic {msg.topic}: {msg.payload.decode()}")
    # Procesar mensaje según el topic
    if msg.topic == "pulso":
        try:
            pulso = float(msg.payload.decode())
            print(type(pulso))
            write_api.write(bucket=bucket, record=[{"measurement": "pulso", "fields": {"valor": pulso}}])
        except ValueError:
            print("Error: El mensaje no es un número flotante válido.")
    elif msg.topic == "coordenadas":
        try:
            latitud, longitud = map(float, msg.payload.decode().split(","))
            point_geojson = geojson.Point((longitud, latitud))
            write_api.write(bucket=bucket, record=[{"measurement": "coordenadas", "fields": {"geojson": geojson.dumps(point_geojson)}}])
        except ValueError:
            print("Error: El mensaje de coordenadas no es válido.")

# Crear un cliente MQTT
client = mqtt.Client()

# Configurar las funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT (debes reemplazar "mqtt.example.com" por la dirección del broker)
# Por defecto, el broker utiliza el puerto 1883
client.connect("broker.hivemq.com", 1883, 60)

# Mantener la conexión activa y escuchar por siempre
client.loop_forever()
