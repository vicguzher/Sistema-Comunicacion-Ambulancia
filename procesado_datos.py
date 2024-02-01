# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 18:28:48 2024

@author: vicen
"""

import serial

# Configuración del puerto serie
puerto_serie = serial.Serial('COM16', 115200)  # Ajusta el nombre del puerto y la velocidad de baudios según tu configuración

# Archivo para guardar los pulsos
archivo_pulsos = open('pulsos.txt', 'a')  # Abre el archivo en modo de escritura al final

try:
    while True:
        # Leer desde el puerto serie
        lectura_serial = puerto_serie.readline().decode().strip()

        # Buscar la palabra "pulso:" en la cadena
        indice_pulso = lectura_serial.find("pulso:")

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
                mensaje_antes = mensaje_pulso[:indice_coordenadas].strip()
                mensaje_despues = mensaje_pulso[indice_coordenadas + len("coordenadas:"):].strip()

                # Guardar el mensaje antes de "coordenadas:" en el archivo
                archivo_pulsos.write("Antes de coordenadas: " + mensaje_antes + "\n")
                archivo_pulsos.flush()  # Asegura que los datos se escriban inmediatamente en el archivo

                # Guardar el mensaje después de "coordenadas:" en el archivo
                archivo_pulsos.write("Después de coordenadas: " + mensaje_despues + "\n")
                archivo_pulsos.flush()  # Asegu

except KeyboardInterrupt:
    print("Detención del programa por el usuario")

finally:
    archivo_pulsos.close()  # Cierra el archivo al finalizar
    puerto_serie.close()  # Cierra el puerto serie
