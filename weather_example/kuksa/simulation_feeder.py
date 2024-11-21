from kuksa_client.grpc import VSSClient, Datapoint
import paho.mqtt.client as mqtt
import time
import json

collision_location = {"latitude": 51, "longitude": 10}
initial_location = {"latitude": 55, "longitude": 10}
BROKER_ADDRESS = "127.0.0.1"
PORT = 1883
TOPIC = "accident"

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        pass
    else:
        print(f"Failed to connect, return code {rc}")

mqtt_client.on_connect = on_connect

try:
    mqtt_client.connect(BROKER_ADDRESS, PORT)
    mqtt_client.loop_start()

    last_publish_time = time.time()
    collision_occurred = False

    while not collision_occurred:
        with VSSClient('127.0.0.1', 55555) as client:
            client.set_current_values({
                'Vehicle.CurrentLocation.Latitude': Datapoint(initial_location["latitude"]),
                'Vehicle.CurrentLocation.Longitude': Datapoint(initial_location["longitude"]),
            })

        print("driving now")

        initial_location["latitude"] -= 0.12
        initial_location["longitude"] -= 0.04

        if time.time() - last_publish_time >= 10:
            location = {
                "collision_location": collision_location
            }
            message = json.dumps(location)
            result = mqtt_client.publish(TOPIC, message)
            print("---------------------------------------------------------------------------")
            print(f"Accident happened at ------>> {collision_location}")
            print("---------------------------------------------------------------------------")
            collision_occurred = True

        time.sleep(1)

    print("stop")

except KeyboardInterrupt:
    print("Terminating the client...")

finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

print("Finished.")
