# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:29:16 2024

@author: vicen
"""

import serial
import paho.mqtt.client as mqtt

# Configuración del puerto serie
puerto_serie = serial.Serial('COM16', 115200) 

# Configuración del cliente MQTT
cliente_mqtt = mqtt.Client()
cliente_mqtt.connect("broker.hivemq.com", 1883) # Conectar al broker MQTT

try:
    while True:
        # Leer desde el puerto serie
        lectura_serial = puerto_serie.readline().decode().strip()

        # Buscar la palabra "pulso:" en la cadena
        indice_pulso = lectura_serial.find("pulso:")
        indice_rssi = lectura_serial.find("RssiValue=")
        indice_Cfo = lectura_serial.find("Cfo=")

        if indice_rssi != -1:
            inicio = indice_rssi + len("RssiValue=")
            fin = lectura_serial.find(";", inicio)

            # Extraer el mensaje entre "pulso:" y ";"
            rssi = lectura_serial[inicio:fin]
            cliente_mqtt.publish("ambulance/rssi", rssi)
            
        if indice_Cfo != -1:
              inicio = indice_Cfo + len("Cfo=")
              fin = lectura_serial.find(";", inicio)

              # Extraer el mensaje entre "pulso:" y ";"
              cfo = lectura_serial[inicio:fin]
              cliente_mqtt.publish("ambulance/cfo", cfo)    
            
        if indice_pulso != -1:
            # Encontrar el índice de inicio y final del mensaje deseado
            inicio = indice_pulso + len("pulso:")
            fin = lectura_serial.find(";", inicio)

            # Extraer el mensaje entre "pulso:" y ";"
            mensaje_pulso = lectura_serial[inicio:fin]

            # Buscar la palabra "coordenadas:" en el mensaje del pulso
            indice_coordenadas = mensaje_pulso.find("coordenadas:")

            if indice_coordenadas != -1:
                # Separar el mensaje antes y después de "coordenadas:"
                pulso = mensaje_pulso[:indice_coordenadas].strip()
                coordenadas = mensaje_pulso[indice_coordenadas + len("coordenadas:"):].strip()

                # Enviar el mensaje antes de "coordenadas:" por MQTT al topic "coordenadas"
                cliente_mqtt.publish("ambulance/pulso", pulso)

                # Enviar el mensaje después de "coordenadas:" por MQTT al topic "coordenadas"
                cliente_mqtt.publish("ambulance/location", coordenadas)

except KeyboardInterrupt:
    print("Detención del programa por el usuario")

finally:
    puerto_serie.close()  # Cierra el puerto serie al finalizar
    cliente_mqtt.disconnect()  # Desconecta el cliente MQTT
