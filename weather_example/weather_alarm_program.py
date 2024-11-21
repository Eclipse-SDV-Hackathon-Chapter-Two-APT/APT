import paho.mqtt.client as mqtt
import json
import pygame
import sys
import time
import random
import geopy.distance

BROKER_ADDRESS = "127.0.0.1"
PORT = 1883
TOPIC_WEATHER = "alert/weather"

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
slide_value = 0
humidity = 0
message_display_time = None

threshold = 500
slide_cnt = 0
time_cnt = 0

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected successfully")
        client.subscribe(TOPIC_WEATHER)
    else:
        print(f"Failed to connect, reason code: {reason_code}")

def on_message(client, userdata, message):
    global message_to_display, slide_cnt, time_cnt, message_display_time, humidity
    try:
        decoded_message = message.payload.decode('utf-8')
        data = json.loads(decoded_message)
        slide_value = data.get("slide_value")
        humidity = data.get("humidity")
        print(slide_value)
        print(humidity)
        if slide_value >= threshold:
            slide_cnt += 1

        time_cnt = (time_cnt + 1) % 60
        if time_cnt == 0:
            slide_cnt = 0

        message_to_display = f"Slide count: {slide_cnt}"
        print(message_to_display)
        message_display_time = time.time()
        print("Weather successfully received")
    except json.JSONDecodeError:
        print("JSON error")

def display_message(text):
    screen.blit(background_image, (0, 0))
    
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if message_to_display:
        print("Get Message")

    if slide_cnt > 10 and humidity >= 60:
        display_message(message_to_display)
        print(00)
        time.sleep(3)
    else:
        screen.blit(background_image, (0, 0))
        pygame.display.flip()

    near_client.loop(timeout=0.1)

    clock.tick(30)
