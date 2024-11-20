from kuksa_client.grpc import VSSClient, Datapoint
import time

collision_location = {"latitude": 51, "longitude": 10}
initial_location = {"latitude": 52.5200, "longitude": 13.4050}

with VSSClient('127.0.0.1', 55555) as client:
    client.set_current_values({
        'Vehicle.CurrentLocation.Latitude': Datapoint(initial_location["latitude"]),
        'Vehicle.CurrentLocation.Longitude': Datapoint(initial_location["longitude"])
    })
    print(f"Feeding 'Vehicle.CurrentLocation.*' to initial location {initial_location}")


    time.sleep(5)


    client.set_current_values({
        'Vehicle.CurrentLocation.Latitude': Datapoint(collision_location["latitude"]),
        'Vehicle.CurrentLocation.Longitude': Datapoint(collision_location["longitude"])
    })
    print(f"Feeding 'Vehicle.CurrentLocation.*' to collision location {collision_location}")

print("Finished.")
