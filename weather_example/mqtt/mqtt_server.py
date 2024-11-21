import paho.mqtt.client as mqtt
import json

BROKER_ADDRESS = "127.0.0.1"  
PORT = 1883  
TOPICS = [("accident", 0), ("weather", 0)]  


TOPIC_ALERT = "alert/car"
TOPIC_WEATHER_ALERT = "alert/weather"
TOPIC_POLICE = "alert/police"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        client.subscribe(TOPICS)  
        print("Connected and subscribed successfully")
    else:
        print(f"Failed to connect, reason code: {reason_code}")


def on_message(client, userdata, message):
    try:
        decoded_message = message.payload.decode('utf-8')
        data = json.loads(decoded_message)
        vehicle_id = data.get("vehicle_id")


        if message.topic == "accident":
            alert_publish_message(TOPIC_ALERT, decoded_message)
            police_publish_message(TOPIC_POLICE, decoded_message)
            print(f"Accident alert sent for vehicle {vehicle_id}")
        elif message.topic == "weather":
            alert_publish_message(TOPIC_WEATHER_ALERT, decoded_message)
            police_publish_message(TOPIC_POLICE, decoded_message)
            print(f"Weather alert sent for vehicle {vehicle_id}")

        print(f"Processed message from topic {message.topic}: {decoded_message}")
    except json.JSONDecodeError:
        print("Error decoding JSON from message")


def alert_publish_message(topic, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Message '{message}' sent to topic '{topic}'")
    else:
        print(f"Failed to send message to topic '{topic}'")

def police_publish_message(topic, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Message '{message}' sent to topic '{topic}'")
    else:
        print(f"Failed to send message to topic '{topic}'")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_ADDRESS, PORT)
client.loop_start()


try:
    print("MQTT client running. Press Ctrl+C to exit.")
    while True:
        pass  
except KeyboardInterrupt:
    print("Terminating MQTT client...")
finally:
    client.loop_stop()  
    client.disconnect()  
