import paho.mqtt.client as mqtt
import json

BROKER_ADDRESS = "127.0.0.1"  
PORT = 1883  
TOPIC_POLICE = "alert/police" 


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected successfully")
        client.subscribe(TOPIC_POLICE)
    else:
        print(f"Failed to connect, reason code: {reason_code}")


def on_message(client, userdata, message):
    try:

        decoded_message=message.payload.decode('utf-8')

        # change velocity to gps needed
        data=json.loads(decoded_message)
        collision_location=data.get("collision_location")
        print("police received gps data")
        print(collision_location)
        # print(f"Received message: {message.payload.decode('utf-8')} on topic {message.topic}")

    except json.JSONDecodeError:
        print("json erre")


police = mqtt.Client()
police.connect(BROKER_ADDRESS, PORT)
police.on_connect = on_connect
police.on_message = on_message
police.loop_forever()