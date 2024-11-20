import paho.mqtt.client as mqtt
import json

BROKER_ADDRESS = "127.0.0.1"  
PORT = 1883  
TOPIC_ALERT = "alert/car" 


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected successfully")
        client.subscribe(TOPIC_ALERT)
    else:
        print(f"Failed to connect, reason code: {reason_code}")


def on_message(client, userdata, message):
    try:

        decoded_message=message.payload.decode('utf-8')

        # change velocity to gps needed
        data=json.loads(decoded_message)
        collision_location=data.get("collision_location")
        print("alert successfully received")
        print(collision_location)
        # print(f"Received message: {message.payload.decode('utf-8')} on topic {message.topic}")

    except json.JSONDecodeError:
        print("json erre")

near_client = mqtt.Client()
near_client.connect(BROKER_ADDRESS, PORT)
near_client.on_connect = on_connect
near_client.on_message = on_message
near_client.loop_forever()
