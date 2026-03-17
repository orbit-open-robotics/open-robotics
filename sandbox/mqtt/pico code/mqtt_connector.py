import network
import time
from umqtt.simple import MQTTClient

SSID = "Room32"
PASSWORD = "password32"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("WiFi connected")

def on_message(topic, msg):
    print("Received:", msg.decode())

connect_wifi()

client = MQTTClient("pico_001", "broker.hivemq.com")
client.set_callback(on_message)
client.connect()
client.subscribe(b"mypico/inbox")
print("Waiting for messages...")

while True:
    client.check_msg()
    time.sleep(0.1)