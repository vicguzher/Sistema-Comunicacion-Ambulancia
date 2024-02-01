# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:31:48 2024

@author: vicen
"""

import paho.mqtt.client as mqtt

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

