import network
import socket
import time

# --- Configuration ---
SSID = "Room32"
PASSWORD = "password32"

# --- Connect to WiFi ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)

    print("\nConnected!")
    print("IP Address:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

# --- Build HTML response ---
def build_page():
    html = """<!DOCTYPE html>
    <html>
        <head><title>Pico W Server</title></head>
        <body>
            <h1>Hello from Raspberry Pi Pico W!</h1>
            <p>Your MicroPython web server is running.</p>
        </body>
    </html>"""
    return html

# --- Start Web Server ---
def start_server(ip):
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print(f"Listening on http://{ip}:80")

    while True:
        conn, client_addr = s.accept()
        print("Client connected from:", client_addr)

        request = conn.recv(1024)
        print("Request:", request.decode())

        response = build_page()
        conn.send("HTTP/1.1 200 OK\r\n")
        conn.send("Content-Type: text/html\r\n")
        conn.send("Connection: close\r\n\r\n")
        conn.send(response)
        conn.close()

# --- Main ---
ip = connect_wifi()
start_server(ip)