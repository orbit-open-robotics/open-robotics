from orbit import WebClient
from time import sleep


# Network
SSID = "Room32"
PASSWORD = "password32"

SSID = "Linton"
PASSWORD = "Old_coffee_mugz2"
    
# Topics
TOPIC_PUBLISH_BASE = "orbit_pico/response"     # Pico sends data here
TOPIC_SUBSCRIBE_BASE = "orbit_pico/command"  # Pico listens for commands here
    
ID = "bob"
TOPIC_PUBLISH = TOPIC_PUBLISH_BASE + '/' + ID
TOPIC_SUBSCRIBE = TOPIC_SUBSCRIBE_BASE + '/' + ID

respond = False

def receive_command(topic, message)-> None:
    print(f"Received on {topic}: {message}")
    web_client.publish(command=f'Received {message}')
    
             
web_client: WebClient = WebClient(
    network_name = SSID,
    password = PASSWORD,
    id = "0",
    subscribe_topic = TOPIC_SUBSCRIBE,
    publish_topic = TOPIC_PUBLISH,
    receive_command_func = receive_command)  
    
while True:
    web_client.check_command()
    sleep(0.1)