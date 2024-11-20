import traci
import random

SUMO_CMD = ["sumo-gui", "-c", "hack.sumocfg"]

CRASHED_VEHICLES = set()
ACCIDENT_ROAD = None
POLICE_CAR_ID = "police_1"
COLLISION_STEP = 1000  


def run_simulation():
    global CRASHED_VEHICLES, ACCIDENT_ROAD

    traci.start(SUMO_CMD) 
    step = 0

    while step < 10000: 
        traci.simulationStep()  


        collisions = traci.simulation.getCollidingVehiclesIDList()
        if collisions:
            for vehicle_id in collisions:
                if vehicle_id not in CRASHED_VEHICLES:
                    print(f"Collision detected: {vehicle_id}")
                    handle_collision(vehicle_id)

        if ACCIDENT_ROAD and POLICE_CAR_ID not in traci.vehicle.getIDList():
            spawn_police_car()

        if ACCIDENT_ROAD and POLICE_CAR_ID in traci.vehicle.getIDList():
            move_police_car_to_accident()

        create_vehicles_for_collision(step) 

        step += 1

    traci.close()

def handle_collision(vehicle_id):
    global CRASHED_VEHICLES, ACCIDENT_ROAD

    traci.vehicle.setColor(vehicle_id, (255, 0, 0))  # 빨간색
    CRASHED_VEHICLES.add(vehicle_id)

    ACCIDENT_ROAD = traci.vehicle.getRoadID(vehicle_id)
    print(f"Accident on road: {ACCIDENT_ROAD}")

    print_road_coordinates(ACCIDENT_ROAD)

    set_road_color(ACCIDENT_ROAD)

    block_accident_road(ACCIDENT_ROAD)


def print_road_coordinates(road_id):
    from_node = traci.edge.getFromNode(road_id) 
    to_node = traci.edge.getToNode(road_id)    

    from_x, from_y = traci.node.getPosition(from_node)
    to_x, to_y = traci.node.getPosition(to_node)

    print(f"Road {road_id} starts at ({from_x}, {from_y}) and ends at ({to_x}, {to_y})")


def set_road_color(road_id):
    for edge_id in traci.edge.getIDList():
        if edge_id == road_id:
            traci.edge.setColor(edge_id, (128, 0, 128))  


def block_accident_road(road_id):
    for vehicle_id in traci.vehicle.getIDList():
        if traci.vehicle.getRoadID(vehicle_id) == road_id:
            traci.vehicle.setSpeed(vehicle_id, 0) 
        else:
            traci.vehicle.setSpeed(vehicle_id, max(5, random.uniform(1, 10))) 

def spawn_police_car():
    global POLICE_CAR_ID
    available_vehicles = [vehicle_id for vehicle_id in traci.vehicle.getIDList() if vehicle_id not in CRASHED_VEHICLES]
    
    if available_vehicles:
        police_vehicle_id = random.choice(available_vehicles) 
        traci.vehicle.setColor(police_vehicle_id, (0, 0, 255))  
        POLICE_CAR_ID = police_vehicle_id 


def move_police_car_to_accident():
    global POLICE_CAR_ID, ACCIDENT_ROAD
    if ACCIDENT_ROAD:
        route = traci.simulation.findRoute(traci.vehicle.getRoadID(POLICE_CAR_ID), ACCIDENT_ROAD)
        traci.vehicle.setRoute(POLICE_CAR_ID, route.edges)


def create_vehicles_for_collision(step):
    if step == COLLISION_STEP:
        vehicle_list = traci.vehicle.getIDList()

        if len(vehicle_list) < 20:
            print("충돌을 유도할 차량이 부족합니다.")
            return


        vehicles_to_speed_up = random.sample(vehicle_list, min(10, len(vehicle_list)))


        remaining_vehicles = [v for v in vehicle_list if v not in vehicles_to_speed_up]
        vehicles_to_stop = random.sample(remaining_vehicles, min(10, len(remaining_vehicles)))


        for vehicle_id in vehicles_to_speed_up:
            traci.vehicle.setSpeed(vehicle_id, 100)  # 속도를 100으로 설정
            print(f"Vehicle {vehicle_id} speed set to 100.")

        for vehicle_id in vehicles_to_stop:
            traci.vehicle.setSpeed(vehicle_id, 0)  # 속도를 0으로 설정
            print(f"Vehicle {vehicle_id} speed set to 0 to increase collision chance.")





if __name__ == "__main__":
    run_simulation()

