from kuksa_client.grpc import VSSClient, Datapoint
import time
import random

collision_location = {"latitude": 51, "longitude": 10}
initial_location = {"latitude": 52.5200, "longitude": 10.4050}

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

        print(f"current location: {initial_location}", )

        


    
    #print(f"Feeding 'Vehicle.CurrentLocation.*' to collision location {collision_location}")

print("Finished.")
