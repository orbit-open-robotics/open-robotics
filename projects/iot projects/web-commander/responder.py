from orbit import WebClient
from time import sleep


# Network
SSID = "Room32"
PASSWORD = "password32"
    
# Topics
TOPIC_PUBLISH_BASE = "orbit_pico/response" 
TOPIC_SUBSCRIBE_BASE = "orbit_pico/command" 
    
ID = "bob"
TOPIC_PUBLISH = TOPIC_PUBLISH_BASE + '/' + ID
TOPIC_SUBSCRIBE = TOPIC_SUBSCRIBE_BASE + '/' + ID

respond = False

def receive_command(topic, command)-> None:
    print(f"Received on {topic}: {command}")
    web_client.publish(message=f'Received {command}')
    
             
web_client: WebClient = WebClient(
    network_name = SSID,
    password = PASSWORD,
    id = "0",
    subscribe_topic = TOPIC_SUBSCRIBE,
    publish_topic = TOPIC_PUBLISH,
    receive_command_func = receive_command,
    execute_code = True)  
    
while True:
    web_client.check_command()
    sleep(0.1)
