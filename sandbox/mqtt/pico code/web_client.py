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

class WebClient:
    def __init__(self,
                 network_name: str,
                 password: str,
                 id: str,
                 subscribe_topic: str = None,
                 receive_message_func: Callable[[str, str], None] = None,
                 create_message_func: Callable[[], Tuple[str, str]] = None,
                 delay: float = 0.5
                 ) -> None:
        self._id: str = id
        self._subscribe_topic: str = subscribe_topic
        self._receive_message_func: Callable[[str, str], None] = receive_message_func
        self._create_message_func: Callable[[], str] = create_message_func
        self._delay: float = delay
        
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
        self.client.set_callback(self._receive_message_func)
        self.client.connect()
        self.client.subscribe(self._subscribe_topic)
        print(f"Connected to broker: {MQTT_BROKER}")
        print(f"Subscribed to: {self._subscribe_topic.decode()}")
        
    def publish(self)-> None:
        if self._create_message_func is None: return
        topic, payload = self._create_message_func()
        if topic is None or payload is None: return
        
        self.client.publish(topic, payload)
        print(f"Published: {payload}")
            
    def start(self)-> None:
        while True:
            self.client.check_msg()
            self.publish()
            sleep(self._delay)
    
    
if __name__ == "__main__":
    # Network
    SSID = "Room32"
    PASSWORD = "password32"
    
    # Topics
    TOPIC_PUBLISH = b"orbit_pico/data"     # Pico sends data here
    TOPIC_SUBSCRIBE = b"orbit_pico/commands"  # Pico listens for commands here
    
    def receive_message(topic, message)-> None:
        print(f"Received on {topic.decode()}: {message.decode()}")
        
    def create_message()-> Tuple[str, str]:
        return TOPIC_PUBLISH, 'hello'
             
    web_client: WebClient = WebClient(
        network_name = SSID,
        password = PASSWORD,
        id = "0",
        subscribe_topic = TOPIC_SUBSCRIBE,
        receive_message_func = receive_message,
        create_message_func = create_message)  
    
    web_client.start()