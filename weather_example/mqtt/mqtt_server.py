import paho.mqtt.client as mqtt
import json

BROKER_ADDRESS = "127.0.0.1"  
PORT = 1883  
TOPIC_ACCIDENT = "accident" 
TOPIC_WEATHER = "weather"

TOPIC_ALERT = "alert/car"
TOPIC_WEATHER_ALERT = "alert/weather"

TOPIC_POLICE = "alert/police"


def on_connect1(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected successfully")
        client.subscribe(TOPIC_ACCIDENT)
    else:
        print(f"Failed to connect, reason code: {reason_code}")

def on_connect2(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected successfully")
        client.subscribe(TOPIC_WEATHER)
    else:
        print(f"Failed to connect, reason code: {reason_code}")


def on_message1(client, userdata, message):
    try:

        decoded_message=message.payload.decode('utf-8')

        data=json.loads(decoded_message)
        vehicle_id=data.get("vehicle_id")
        
        alert_publish_message(TOPIC_ALERT,decoded_message)
        police_publish_message(TOPIC_POLICE,decoded_message)
        print("alert successfully sent")
        print(vehicle_id)
        print(f"Received message: {message.payload.decode('utf-8')} on topic {message.topic}")

    except json.JSONDecodeError:
        print("json erre")

def on_message2(client, userdata, message):
    try:

        decoded_message=message.payload.decode('utf-8')

        data=json.loads(decoded_message)
        vehicle_id=data.get("vehicle_id")
        
        alert_publish_message(TOPIC_WEATHER_ALERT,decoded_message)
        police_publish_message(TOPIC_POLICE,decoded_message)
        print("alert successfully sent")
        print(vehicle_id)
        print(f"Received message: {message.payload.decode('utf-8')} on topic {message.topic}")

    except json.JSONDecodeError:
        print("json erre")



def alert_publish_message(TOPIC_ALERT, message):
    result = send_alert_server.publish(TOPIC_ALERT, message)
    
    status = result[0]
    if status == 0:
        print(f"Message '{message}' sent to topic '{TOPIC_ALERT}'")
    else:
        print(f"Failed to send message to topic '{TOPIC_ALERT}'")


def police_publish_message(TOPIC_POLICE, message):
    result = police_alert_server.publish(TOPIC_POLICE, message)
    
    status = result[0]
    if status == 0:
        print(f"Message '{message}' sent to topic '{TOPIC_POLICE}'")
    else:
        print(f"Failed to send message to topic '{TOPIC_POLICE}'")


# ---------------------------------------------------------------------------


get_accident_server = mqtt.Client()
get_accident_server.connect(BROKER_ADDRESS, PORT)

get_weather_server = mqtt.Client()
get_weather_server.connect(BROKER_ADDRESS, PORT)

send_alert_server = mqtt.Client()
send_alert_server.connect(BROKER_ADDRESS, PORT)

police_alert_server = mqtt.Client()
police_alert_server.connect(BROKER_ADDRESS, PORT)

get_accident_server.on_connect = on_connect1
get_accident_server.on_message = on_message1

get_weather_server.on_connect = on_connect2
get_weather_server.on_message = on_message2


get_accident_server.loop_forever()
get_weather_server.loop_forever()
send_alert_server.loop_forever()
police_alert_server.loop_forever()

