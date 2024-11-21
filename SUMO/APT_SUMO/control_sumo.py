import sys
sys.path.append('/media/llj/SanDisk/sumo-src-1.20.0/sumo-1.20.0/tools/')

import traci
import sumolib
import time

# set up for simulation
sumo_binary = "sumo-gui"
sumo_config = "osm.sumocfg" 
sumo_net = sumolib.net.readNet("osm.net.xml.gz")
traci.start([sumo_binary, "-c", sumo_config, "--no-step-log"])

# basic setting
victim_id = "victim"
offender_id = "offender"
police_id = "police"

collision_point = (1328.20, 944.76)
tolerance_distance = 2.0 #3.0, 2.3

victim_initial_speed = 2.0
offender_initial_speed = 4.3
police_initial_speed = 4.0

time_cnt = 0

########################################################################################################
def is_near_collision_point(vehicle_position, collision_point, tolerance):
    vehicle_x, vehicle_y = vehicle_position
    collision_x, collision_y = collision_point
    distance = ((vehicle_x - collision_x) ** 2 + (vehicle_y - collision_y) ** 2) ** 0.5
    return distance <= tolerance

def smooth_speed_adjust(vehicle_id, target_speed, step=0.1):
    current_speed = traci.vehicle.getSpeed(vehicle_id)
    if abs(current_speed - target_speed) > step:
        new_speed = current_speed + step if current_speed < target_speed else current_speed - step
        traci.vehicle.setSpeed(vehicle_id, new_speed)
    else:
        traci.vehicle.setSpeed(vehicle_id, target_speed)

########################################################################################################
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    victim_position = traci.vehicle.getPosition(victim_id)
    offender_position = traci.vehicle.getPosition(offender_id)
    police_position = traci.vehicle.getPosition(police_id)

    if is_near_collision_point(victim_position, collision_point, tolerance_distance):
        traci.vehicle.setSpeed(victim_id, 0)
    else:
        smooth_speed_adjust(victim_id, victim_initial_speed)

    if is_near_collision_point(offender_position, collision_point, tolerance_distance):
        traci.vehicle.setSpeed(offender_id, 0)
        # time_cnt += 1
        # if time_cnt >= 160:
        #     traci.vehicle.setSpeed(offender_id, 1)
        #     time_cnt = 0
    else:
        smooth_speed_adjust(offender_id, offender_initial_speed)

    traci.vehicle.setSpeed(police_id, 2.2)

    # print(f"time_cnt : ", time_cnt)

traci.close()
