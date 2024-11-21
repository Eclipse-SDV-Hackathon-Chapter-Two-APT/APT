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
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")


mqtt_client.on_connect = on_connect

try:
    mqtt_client.connect(BROKER_ADDRESS, PORT)
    mqtt_client.loop_start()

    last_publish_time = time.time()  # 메시지 발행 시간 기록

    while True:
        # 1초마다 위치 데이터 업데이트
        with VSSClient('127.0.0.1', 55555) as client:
            client.set_current_values({
                'Vehicle.CurrentLocation.Latitude': Datapoint(initial_location["latitude"]),
                'Vehicle.CurrentLocation.Longitude': Datapoint(initial_location["longitude"]),
            })
            print(f"Feeding 'Vehicle.CurrentLocation.*' to initial location {initial_location}")

        initial_location["latitude"] -= 0.12
        initial_location["longitude"] -= 0.04

        # 현재 시간이 마지막 발행 시간으로부터 5초가 지났는지 확인
        if time.time() - last_publish_time >= 5:
            location = {
                "collision_location": {"latitude": 51, "longitude": 10}
            }

            message = json.dumps(location)
            result = mqtt_client.publish(TOPIC, message)

            print(f"Published message to topic {TOPIC}: {message}")
            last_publish_time = time.time()  # 마지막 발행 시간 업데이트

        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    print("Terminating the client...")

finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

print("Finished.")
