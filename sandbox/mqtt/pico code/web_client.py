#
# WebClient
# Requires micropython.umqtt.simple library
#
from network import WLAN, STA_IF
from time import sleep
from umqtt.simple import MQTTClient

# MQTT Information
MQTT_BROKER = "broker.hivemq.com"  # Free public broker
MQTT_PORT = 1883
CLIENT_ID_BASE = "orbit_pico"           # Must be unique on the broker

# Topics
TOPIC_PUBLISH = b"orbit_pico/data"     # Pico sends data here
TOPIC_SUBSCRIBE = b"orbit_pico/commands"  # Pico listens for commands here

# TODO: should this be a derivation?

class WebClient:
    def __init__(self, network_name: str, password: str, id: str) -> None:
        self.id: str = id
        self._connect_to_wifi(network_name=network_name, password=password)
        self._connect_mqtt()
        
    def _connect_to_wifi(self, network_name: str, password: str) -> None:
        wlan: WLAN = WLAN(STA_IF)
        wlan.active(True)
        wlan.connect(network_name, password)
        print("Connecting to WiFi", end="")
        while not wlan.isconnected():
            print(".", end="")
            sleep(0.5)
        print("\nConnected! IP:", wlan.ifconfig()[0])
        
    def _connect_mqtt(self) -> None:
        client_id: str = CLIENT_ID_BASE + self.id
        self.client: MQTTClient = MQTTClient(client_id, MQTT_BROKER, MQTT_PORT)
        self.client.set_callback(self.on_message)
        self.client.connect()
        self.client.subscribe(TOPIC_SUBSCRIBE)
        print(f"Connected to broker: {MQTT_BROKER}")
        print(f"Subscribed to: {TOPIC_SUBSCRIBE.decode()}")
        
    def on_message(self, topic, message)-> None:
        print(f"Received on {topic.decode()}: {message.decode()}")
        
    def start(self)-> None:
        counter: int = 0
        while True:
            # Check for incoming messages (non-blocking)
            self.client.check_msg()

            # Publish some data every 5 seconds
            payload: str = f"hello from pico, count={counter}"
            self.client.publish(TOPIC_PUBLISH, payload)
            print(f"Published: {payload}")

            sleep(5)
    
    
if __name__ == "__main__":
    SSID = "Room32"
    PASSWORD = "password32"
    web_client: WebClient = WebClient(SSID, PASSWORD, "0")
    web_client.start()