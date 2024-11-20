from kuksa_client.grpc import VSSClient
import paho.mqtt.client as mqtt   #mqtt fsa
import time
import json
import math
import geopy.distance


KUKSA_HOST = '127.0.0.1'
KUKSA_PORT = 55555
VEHICLE_ID = "Vehicle2"

BROKER_ADDRESS = "127.0.0.1"  ##this is my ip address 
PORT = 1883    #
TOPIC = "weather"


mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER_ADDRESS, PORT)

def publish_weather_message(topic, message):
    result = mqtt_client.publish(topic, message)
    
    status = result[0]
    if status == 0:
        print(f"Message '{message}' sent to topic '{topic}'")
    else:
        print(f"Failed to send message to topic '{topic}'")

engine_speed = 15000
speed = 120
threshold = 500
humidity = 70

while True:
    try:
        with VSSClient(KUKSA_HOST, KUKSA_PORT) as kuksa_client:

            weather_message = {
                       "vehicle_id": VEHICLE_ID,
                       "slide_value": engine_speed - speed * 100,
                       "humidity": humidity,
                       "status": "1"
                   }
            
            message = json.dumps(weather_message) 
            publish_weather_message(TOPIC, message)
            print(f"{VEHICLE_ID} - Weather Message: {weather_message}")
            
            time.sleep(1)  

    except KeyboardInterrupt:
        print("Terminating the client...")

    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

