import socket
import network
from time import sleep

# First confirm WiFi
wlan = network.WLAN(network.STA_IF)
print("Connected:", wlan.isconnected())
print("ifconfig:", wlan.ifconfig())

# Test DNS resolution directly
print("\nResolving broker hostname...")
try:
    addr = socket.getaddrinfo("broker.hivemq.com", 1883)
    print("Resolved OK:", addr)
except Exception as e:
    print("DNS resolution FAILED:", e)

# Test raw socket connection
print("\nTesting raw socket connection...")
try:
    s = socket.socket()
    s.connect(("broker.hivemq.com", 1883))
    print("Socket connected OK")
    s.close()
except Exception as e:
    print("Socket connection FAILED:", e)