import paho.mqtt.client as mqtt
import json
import pygame
import sys
import time
import random
import geopy.distance


BROKER_ADDRESS = "127.0.0.1"
PORT = 1883
TOPIC_ALERT = "alert/car"

pygame.init()
WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Head-Up Display")
font_large = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 20)
clock = pygame.time.Clock()

background_image = pygame.image.load("Hit&Run Case.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

warning_icon = pygame.image.load("alert_msg.png")
warning_icon = pygame.transform.scale(warning_icon, (240, 175))

warning_speed_icon = pygame.image.load("alert_speed.png")
warning_speed_icon = pygame.transform.scale(warning_speed_icon, (280, 270))

warning_road_icon = pygame.image.load("alert_road.png")
warning_road_icon = pygame.transform.scale(warning_road_icon, (328, 99))

alpha = 0

message_to_display = None
collision_location = None
message_display_time = None

current_speed = random.randrange(66,75)
this_location = {"latitude": 50, "longitude": 9}
print("Current Speed: ", current_speed)

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected successfully")
        client.subscribe(TOPIC_ALERT)
    else:
        print(f"Failed to connect, reason code: {reason_code}")

def on_message(client, userdata, message):
    global message_to_display, collision_location, this_location, message_display_time
    try:
        decoded_message = message.payload.decode('utf-8')
        data = json.loads(decoded_message)
        collision_location = data.get("collision_location")
        accident_distance = geopy.distance.distance((collision_location['latitude'], collision_location['longitude']), (this_location['latitude'],this_location['longitude'])).km
        accident_distance = round(accident_distance, 1)

        message_to_display = f"{accident_distance} KM"
        message_display_time = time.time()
        print("Alert successfully received")
    except json.JSONDecodeError:
        print("JSON error")

def display_message(text):
    screen.blit(background_image, (0, 0))
    
    if (current_speed > 70) :
        screen.blit(warning_speed_icon, (WIDTH // 2 - 330, HEIGHT // 2 - 90))
    
    
    screen.blit(warning_icon, (WIDTH // 2, HEIGHT // 2 - 120))
    screen.blit(warning_road_icon, (WIDTH // 2 + 10, HEIGHT // 2 + 40))
    message_surface = font_large.render(text, True, (255, 255, 255))
    screen.blit(message_surface, (WIDTH // 2 + 120, HEIGHT // 2 - 50))
    
    speed_warning = "Reduce Speed Immediately!"
    speed_surface = font_small.render(speed_warning, True, (255, 255, 0))
    screen.blit(speed_surface, (WIDTH // 2 - speed_surface.get_width() // 2, HEIGHT // 2 + 100))
    
    pygame.display.flip()

near_client = mqtt.Client()
near_client.on_connect = on_connect
near_client.on_message = on_message
near_client.connect(BROKER_ADDRESS, PORT)

while True:
    this_location["latitude"] -= 0.05
    this_location["longitude"] -= 0.03

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if message_to_display:
        display_message(message_to_display)
    else:
        screen.blit(background_image, (0, 0))
        pygame.display.flip()

    near_client.loop(timeout=0.1)

    clock.tick(30)
