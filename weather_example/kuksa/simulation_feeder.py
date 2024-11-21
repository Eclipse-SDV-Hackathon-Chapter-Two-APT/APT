from kuksa_client.grpc import VSSClient, Datapoint
import paho.mqtt.client as mqtt
import time
import json
import random

collision_location = {"latitude": 51, "longitude": 10}
initial_location = {"latitude": 55, "longitude": 10}
BROKER_ADDRESS = "127.0.0.1"  
PORT = 1883
TOPIC = "accident"

mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

mqtt_client.on_connect = on_connect

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")
try:
    mqtt_client.connect(BROKER_ADDRESS, PORT)
    mqtt_client.loop_start()  

    while True :
        with VSSClient('127.0.0.1', 55555) as client:
            client.set_current_values({
            'Vehicle.CurrentLocation.Latitude': Datapoint(initial_location["latitude"]),
            'Vehicle.CurrentLocation.Longitude': Datapoint(initial_location["longitude"]),
            })
            print(f"Feeding 'Vehicle.CurrentLocation.*' to initial location {initial_location}")


            time.sleep(1)
            initial_location["latitude"] -= 0.12
            initial_location["longitude"] -= 0.04

            client.set_current_values({
            'Vehicle.CurrentLocation.Latitude': Datapoint(initial_location["latitude"]),
            'Vehicle.CurrentLocation.Longitude': Datapoint(initial_location["longitude"]),
            })


            location = {
                    "collision_location" : {"latitude": 51, "longitude": 10}
            }

            message = json.dumps(location)


            result = mqtt_client.publish(TOPIC, message)
            print(f"current location: {initial_location}", )


except KeyboardInterrupt:
    print("Terminating the client...")

finally:
    mqtt_client.loop_stop()  
    mqtt_client.disconnect() 
        


    
    #print(f"Feeding 'Vehicle.CurrentLocation.*' to collision location {collision_location}")

print("Finished.")
