from kuksa_client.grpc import VSSClient
import paho.mqtt.client as mqtt   #mqtt fsa
import time
import json


KUKSA_HOST = '127.0.0.1'
KUKSA_PORT = 55555
VEHICLE_ID = "Vehicle1"

BROKER_ADDRESS = "127.0.0.1"  ##this is my ip address 
PORT = 1883    #
TOPIC = "accident"  


mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER_ADDRESS, PORT)

def publish_message(topic, message):
    result = mqtt_client.publish(topic, message)
    # 발행 결과 확인
    status = result[0]
    if status == 0:
        print(f"Message '{message}' sent to topic '{topic}'")
    else:
        print(f"Failed to send message to topic '{topic}'")

collision_location = {"latitude": 51, "longitude": 10}

try:
    with VSSClient(KUKSA_HOST, KUKSA_PORT) as kuksa_client:
        print("Subscribing to location updates...")
        
        for update in kuksa_client.subscribe_current_values(['Vehicle.CurrentLocation.Latitude', 'Vehicle.CurrentLocation.Longitude']):
            updated_latitude = update.get('Vehicle.CurrentLocation.Latitude').value
            updated_longitude = update.get('Vehicle.CurrentLocation.Longitude').value
    
            if updated_latitude == collision_location["latitude"] and updated_longitude == collision_location["longitude"]:

                collision_message = {
                    "vehicle_id": VEHICLE_ID,
                    "collision_location": collision_location,
                    "status": "1"
                }
                message = json.dumps(collision_message) 
                publish_message(TOPIC, message)
                print(f"{VEHICLE_ID} - Collision detected! Message: {collision_message}")
            else:
                print(f"{VEHICLE_ID} - No collision detected. Current position: Latitude = {updated_latitude}, Longitude = {updated_longitude}")

            time.sleep(1)  

except KeyboardInterrupt:
    print("Terminating the client...")

finally:
    # 연결 종료
    mqtt_client.loop_stop()
    mqtt_client.disconnect()