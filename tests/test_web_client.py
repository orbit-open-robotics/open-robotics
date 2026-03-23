#
# WebClient
# Requires micropython.umqtt.simple library
#
from orbit import WebClient
from time import sleep

# Network
SSID = "Room32"
PASSWORD = "password32"
    
# Topics
TOPIC_PUBLISH = "orbit_pico/response"     # Pico sends data here
TOPIC_SUBSCRIBE = "orbit_pico/command"  # Pico listens for commands here
    
def receive_command(topic, message)-> None:
    print(f"Received on {topic}: {message}")
             
web_client: WebClient = WebClient(
    network_name = SSID,
    password = PASSWORD,
    subscribe_topic = TOPIC_SUBSCRIBE,
    publish_topic = TOPIC_SUBSCRIBE,
    receive_command_func = receive_command,
    id="0")    
    
while True:
    web_client.publish(TOPIC_PUBLISH, 'hello!')
    web_client.check_command()
    sleep(1)
