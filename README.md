# Sistema para el envío de datos biomédicos mediante Lora en entornos no urbanos 


## 1	Introducción
El siguiente trabajo tiene como objetivo la transmisión de datos biomédicos en entornos de baja cobertura de tecnologías móvil celular (GSM, 4G, 5G…). Para ello se usará la tecnología de comunicaciones LoRa, se crearán script en Python para el procesado de los datos, el uso de una base de datos NoSQL InfluxDB y la herramienta de visualización Grafana.

### 1.1	Problema a resolver
En entornos rurales y de montaña podemos encontrarnos el problema de no disponer cobertura suficiente de tecnologías móviles celulares, debido al menor despliegue de estos sistemas por el bajo nivel de población en estas zonas. Aspecto que puede resultar crítico si existe la necesidad de compartir datos biomédicos para personas residentes en estos lugares o en situaciones de rescate de montañeros y deportistas de actividades en alta montaña.
Para resolver este problema se hará uso de la tecnología LoRa, la cual permite un alcance máximo teórico de 20 Km frente a los 8 Km de las tecnologías móviles. Además de la ventaja que proporciona de un bajo consumo. 

## 2	Arquitectura del Sistema
La arquitectura del sistema seguirá el siguiente esquema:
 

Se dispondrá de una placa stm32wl55 que actuará de transmisor simulando estar conectado a un pulsómetro y a un dispositivo GPS, este transmitirá la información mediante LoRa a otra placa stm32wl55 que actuará de Gateway. Esta recibirá la señal transmitida y mandará esa información por puerto serie. Un script en Python se encontrará en ejecución leyendo el puerto serie correspondiente, tras el procesado de los datos, transmitirá mediante MQTT a un bróker cloud gratuito que proporciona la empresa HiveMQ (https://www.hivemq.com/mqtt/public-mqtt-broker/). Por otro lado, se tendrá un script en Python que estará suscrito a los topic pertinentes, además será el encargado de escribir los datos recogido en la base de datos InfluxDB. Una vez los datos se encuentren en la BBDD, mediante el software OpenSource Grafana serán visualizados.

## 3	Implementación
### 3.1	Placa stm32wl55
Como se describe en el apartado anterior, la transmisión y recepción de los datos se realizará mediante el uso de dos placas stm32wl55. Estos dispositivos proporcionan una forma asequible y flexible para que los usuarios prueben nuevos conceptos y construyan prototipos con el microcontrolador de la serie STM32WL, eligiendo entre las diferentes combinaciones de rendimiento, consumo de energía y características.
Los dispositivos son programados en C, haciendo uso del IDE que proporciona STMicroelectronics, STM32CubeIDE. Se ha tomado de base el código de ejemplo PING-PONG que realiza un envío de mensajes entre las dos placas de forma que la placa master transmite PING y el dispositivo slave responde con PONG, tras un tiempo el rol de estas placas conmuta. Se han realizado las siguientes modificaciones al código:
•	Las placas tendrán siempre el mismo rol, una actuará de master y otra de slave.
•	La placa slave generará un número aleatorio entre 20 y 220 que simulará el pulsómetro al que se encontraría conectado el transmisor. Además, se transmitirán las coordenadas: 37.683041,-6.620870 (pertenecientes a una zona rural cerca de las minas de Rio Tinto, Huelva) de forma que simule un sistema GPS
 

•	El dispositivo master estará encargado de recibir la información transmitida por el nodo slave, enviará por puerto serie el valor de la frecuencia cardíaca, las coordenadas y, además, la RSSI y SNR. Por último, enviará PONG de forma que le pueda indicar al slave que sigue establecida la conexión.
 



Parámetros:
•	PTX: 14 dBm
•	BW: 125 KHz
•	Coding rate: 4/5
•	Frecuencia: 868 MHz
•	Spreading factor: 7

### 3.2	Lectura de Puerto Serie y transmisión MQTT
Se ha creado un script en Python (mqttout) que es el encargado de leer el puerto serie correspondiente (COM16) y a la velocidad establecida (115200 baudios). También, se dispone de un cliente MQTT que establece comunicación con el bróker a través de la IP broker.hivemq.com y puerto 1883. Una vez que el código se encuentra en ejecución, empieza a leer el puerto serie en busca de las siguientes cadenas de caracteres: “RssiValue=”, “Cfo=”, “pulso:” y “coordenadas:”. Una vez se encuentran las cadenas de caracteres se obtendrá el valor de cada una de ellas y se publicará en el topic correspondiente (ambulance/rssi, ambulance/cfo, ambulance/pulso, ambulance/location). 

### 3.3	Recepción de mensajes MQTT y almacenamiento en BBDD
Se tendrá otro script en Python (mqttin) que será el encargado de suscribirse a los topic anteriormente mencionados, filtrar el mensaje y convertirlos al formato apropiado, float para rssi, snr y pulso, y las coordenadas a formato JSON, separando entre latitud y longitud de forma que después se pueda procesar correctamente en Grafana. Además, se crea el cliente InfluxDB para alojar los datos recibidos. La base de datos InfluxDB se ha decidido desplegar en un contenedor Docker y con la configuración de un volumen de forma que exista persistencia de los datos.
 

### 3.4	Visualización de los datos
Para la visualización de los datos se usará el software OpenSource Grafana, el cual también se encuentra en un contenedor Docker. Primero será necesario elegir la fuente de datos, en este caso InfluxDB. Una vez se encuentre configurado, se continua con la creación de un Dashboard en el que se mostraran en gráficas el valor de la frecuencia cardíaca, la RSSI y SNR, la ubicación será mostrada en un mapa.
 
