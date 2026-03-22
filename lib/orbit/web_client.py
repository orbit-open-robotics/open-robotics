#
# WebClient
# Requires micropython.umqtt.simple library
#
from network import WLAN, STA_IF
from time import sleep
from umqtt.simple import MQTTClient


# MQTT Information
MQTT_BROKER = "broker.hivemq.com" 
MQTT_PORT = 1883
CLIENT_ID_BASE = "orbit_pico"

# TODO: should this be a derivation?
# TODO: redirect callback so that strings are provided

class WebClient:
    def __init__(self,
                 network_name: str,
                 password: str,
                 id: str,
                 subscribe_topic: str,
                 publish_topic: str,
                 receive_command_func: Callable[[str, str], None] | None = None
                 ) -> None:
        self._id: str = id
        self._subscribe_topic: str = subscribe_topic
        self._publish_topic: str = publish_topic
        self._receive_command_func: Callable[[str, str], None] | None = receive_command_func
        
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
        client_id: str = CLIENT_ID_BASE + self._id
        self.client: MQTTClient = MQTTClient(client_id, MQTT_BROKER, MQTT_PORT)
        self.client.set_callback(self._receive_command_bytes)
        self.client.connect()
        self.client.subscribe(self._subscribe_topic.encode())
        print(f"Connected to broker: {MQTT_BROKER}")
        print(f"Subscribed to: {self._subscribe_topic}")
        
    def _receive_command_bytes(self, topic, message) -> None:
        if self._receive_command_func is not None:
            self._receive_command_func(topic.decode(), message.decode())
        
    def check_command(self) -> None:
        self.client.check_msg()
        
    def publish(self, topic: str = '', command: str = 'No command') -> None:
        if topic == '': topic = self._publish_topic
        self.client.publish(topic.encode(), command.encode())
        print(f"Published: {command}")