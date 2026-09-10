#
# WebClient
# Requires micropython.umqtt.simple library
#
import ubinascii, machine
from network import WLAN, STA_IF
from time import sleep
from umqtt.simple import MQTTClient
from orbit.wifi_connector import WifiConnector

# MQTT Information
MQTT_BROKER = "broker.hivemq.com" 
MQTT_PORT = 1883
CLIENT_ID_BASE = "orbit_pico" # change this name
# Default topics
TOPIC_PUBLISH = "orbit_pico/response"     # Pico sends data here
TOPIC_SUBSCRIBE = "orbit_pico/command"  # Pico listens for commands here

class WebClient(WifiConnector):
    def __init__(self,
                 network_name: str | None = None,
                 password: str | None = None,
                 secrets_file_path: str | None = '/secrets.txt',
                 delay: float = 0.5,
                 subscribe_topic: str | None = TOPIC_SUBSCRIBE,
                 publish_topic: str | None = TOPIC_PUBLISH,
                 receive_message_func: Callable[[str, str], None] | None = None,
                 create_message_func: Callable[[], str] | None = None,
                 ) -> None:
        super().__init__(
            network_name = network_name,
            password = password,
            secrets_file_path = secrets_file_path
            )
        self._delay = delay
        self._subscribe_topic: str = subscribe_topic
        self._publish_topic: str = publish_topic
        self._receive_message_func: Callable[[str, str], None] | None = receive_message_func
        self._create_message_func: Callable[[], str] | None = create_message_func
        
        self.connect()
        self._client = self._connect_mqtt()
        
    def _connect_mqtt(self) -> MQTTClient:
        '''
        Create and return the MQTTClient. It will subscribe to the provided topic
        '''
        # Create the client and register callback
        client_id = CLIENT_ID_BASE + ubinascii.hexlify(machine.unique_id()).decode()
        client: MQTTClient = MQTTClient(client_id, MQTT_BROKER, MQTT_PORT)
        client.set_callback(self._receive_message)
        
        # Connect to the broker
        for attempt in range(5):
            try:
                print(f'Connecting to MQTT with client id {client_id}...')
                client.connect()
                print(f'Connected to broker: {MQTT_BROKER}')
                break
            except OSError as e:
                print(f'MQTT connect failed (attempt {attempt + 1}): {e}')
                sleep(2)
        else:
            raise RuntimeError("Could not connect to MQTT broker after 5 attempts")
        
        # Subscribe
        if self._subscribe_topic :
            client.subscribe(self._subscribe_topic.encode())
            print(f"Subscribed to: {self._subscribe_topic}")
            
        return client

    def _receive_message(self, topic, message) -> None:
        '''
        This is method is called back when a subscribed message is available
        It calls the provided callback function if provided
        '''
        if self._receive_message_func:
            self._receive_message_func(topic.decode(), message.decode())
            return
        print(f'topic {topic.decode()} : {message.decode()}')
        
    def _create_and_send_message(self) -> None:
        '''
        Create a message using the callback function (if available) and
        send it as the published topic.
        '''
        if self._create_message_func is None: return
        message = self._create_message_func()
        if message is None: return
        
        self._client.publish(self._publish_topic.encode(), message.encode())
        print(f"Published: {message}")

    def send_message(self, topic: str, message: str) -> None:
        '''
        Send a message as the provided topic at any time
        '''
        self._client.publish(topic.encode(), message.encode())
            
    def start(self)-> None:
        '''
        This method starts a loop to receive message from the server (subscribed topic),
        and allow the create_message method to create a message which is 
        sent (published topic)
        '''
        while True:
            self._client.check_msg()
            self._create_and_send_message()
            sleep(self._delay)
    
    
if __name__ == "__main__":
    from orbit.secret_reader import SecretReader

    def receive_message(topic, message)-> None:
        print(f"Received on {topic}: {message}")

    num: int = 0
    def create_message()-> str:
        global num
        num += 1
        return f'hello {num}'
    
    # Get Wifi credentials
    secret_reader = SecretReader()
    secret_reader.read()
    network_name = secret_reader.get_value('network_name')
    password = secret_reader.get_value('password')
    print(f'network: {network_name}')

    # Create the web client
    web_client: WebClient = WebClient(
        subscribe_topic = TOPIC_SUBSCRIBE,
        receive_message_func = receive_message,
        create_message_func = create_message)  
    
    web_client.start()