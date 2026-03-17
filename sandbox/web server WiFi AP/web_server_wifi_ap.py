import network
import socket

# --- Configuration ---
AP_SSID = "PicoW-Server"
AP_PASSWORD = "password123"  # Must be at least 8 characters

# --- Start Access Point ---
def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(ssid=AP_SSID, password=AP_PASSWORD)

    while not ap.active():
        pass

    print("Access Point started!")
    print("SSID:", AP_SSID)
    print("IP Address:", ap.ifconfig()[0])  # Usually 192.168.4.1
    return ap.ifconfig()[0]

# --- Build HTML response ---
def build_page():
    html = """<!DOCTYPE html>
    <html>
        <head><title>Pico W Server</title></head>
        <body>
            <h1>Hello from Raspberry Pi Pico W!</h1>
            <p>You are connected directly to the Pico.</p>
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
ip = start_ap()
start_server(ip)