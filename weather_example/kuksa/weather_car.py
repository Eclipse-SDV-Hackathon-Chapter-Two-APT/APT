from kuksa_client.grpc import VSSClient
import paho.mqtt.client as mqtt
import time
import json

KUKSA_HOST = '127.0.0.1'
KUKSA_PORT = 55555
VEHICLE_ID = "Vehicle2"

BROKER_ADDRESS = "127.0.0.1"  
PORT = 1883
TOPIC = "weather"


mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

mqtt_client.on_connect = on_connect

try:
    mqtt_client.connect(BROKER_ADDRESS, PORT)
    mqtt_client.loop_start()  


    engine_speed = 15000
    speed = 120
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


                result = mqtt_client.publish(TOPIC, message)
                if result.rc == 0:
                    print(f"{VEHICLE_ID} - Weather Message: {weather_message}")
                else:
                    print("Failed to send message")

                time.sleep(1) 

        except Exception as e:
            print(f"Error in VSSClient or MQTT: {e}")

except KeyboardInterrupt:
    print("Terminating the client...")

finally:
    mqtt_client.loop_stop()  
    mqtt_client.disconnect() 
