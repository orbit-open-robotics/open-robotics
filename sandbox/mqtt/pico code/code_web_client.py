from web_client import WebClient

TOPIC_PUBLISH = b"orbit_pico/status"     # Pico sends data here
TOPIC_SUBSCRIBE = b"orbit_pico/upload"  # Pico listens for commands here

class CodeWebClient(WebClient):
    def __init__(self,
                 network_name: str,
                 password: str,
                 id: str,
                 delay: float = 0.5)-> None:
        
        super().__init__(
            network_name = network_name,
            password = password,
            id = id,
            subscribe_topic = TOPIC_SUBSCRIBE,
            receive_message_func = self.receive_message,
            create_message_func = None)
    
    def receive_message(self, topic, message)-> None:
        print("Received program, running...")
        try:
            exec(message.decode())
            print("Program finished OK")
        except Exception as e:
            print("Error:", e)
    
if __name__ == "__main__":
    
    # Network
    SSID = "Room32"
    PASSWORD = "password32"
             
    web_client: CodeWebClient = CodeWebClient(
        network_name = SSID,
        password = PASSWORD,
        id = "0")  
    
    web_client.start()