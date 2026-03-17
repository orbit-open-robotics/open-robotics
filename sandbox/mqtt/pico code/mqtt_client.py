import network
import time
from umqtt.simple import MQTTClient

# --- Configuration ---
SSID = "Room32"
PASSWORD = "password32"

MQTT_BROKER = "broker.hivemq.com"  # Free public broker
MQTT_PORT = 1883
CLIENT_ID = "pico_w_001"           # Must be unique on the broker

# Topics
TOPIC_PUBLISH = b"mypico/data"     # Pico sends data here
TOPIC_SUBSCRIBE = b"mypico/commands"  # Pico listens for commands here

# --- Connect to WiFi ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to WiFi", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConnected! IP:", wlan.ifconfig()[0])

# --- Handle incoming messages ---
def on_message(topic, msg):
    print(f"Received on {topic.decode()}: {msg.decode()}")

    # React to commands from your laptop
    if msg == b"led_on":
        print("Turning LED on")
        # add your GPIO code here
    elif msg == b"led_off":
        print("Turning LED off")
        # add your GPIO code here

# --- Connect to MQTT broker ---
def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(TOPIC_SUBSCRIBE)
    print(f"Connected to broker: {MQTT_BROKER}")
    print(f"Subscribed to: {TOPIC_SUBSCRIBE.decode()}")
    return client

# --- Main loop ---
def main():
    connect_wifi()
    client = connect_mqtt()

    counter = 0
    while True:
        # Check for incoming messages (non-blocking)
        client.check_msg()

        # Publish some data every 5 seconds
        payload = f"hello from pico, count={counter}"
        client.publish(TOPIC_PUBLISH, payload)
        print(f"Published: {payload}")

        counter += 1
        time.sleep(5)

main()


