import network
import socket
import machine
import ubinascii
import ure
from machine import Pin
import time

# Configure the LED to show connection status
led = Pin(2, Pin.OUT)

# Get device unique ID
device_id = ubinascii.hexlify(machine.unique_id()).decode()

# Setup the ESP32 as an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ssid = f"ESP32-{device_id}"
ap.config(essid=ssid, password='123456789')
ap.config(max_clients=2)  # Limit number of clients that can connect
ap.config(authmode=network.AUTH_WPA_WPA2_PSK)  # WPA2 Security
print(f"Access Point {ssid} created! IP Address: {ap.ifconfig()[0]}")

# Set up the Form HTML Page
def start_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    while True:
        # Wait for a client to connect
        cl, addr = s.accept()
        print('Client connected from', addr)

        # Read the HTTP request
        request = cl.recv(1024)
        request = str(request)

        # Check if the request includes 'POST' and contains the Wi-Fi SSID and password
        if 'POST' in request:
            ssid = ure.search('ssid=([^&]*)', request)
            password = ure.search('password=([^&]*)', request)

            if ssid and password:
                ssid = ssid.group(1)
                password = password.group(1)
                print(f"SSID: {ssid}, Password: {password}")
                
                # Save the credentials to a file
                try:
                    with open('wifi_cred.txt', 'w') as f:
                        f.write(f"{ssid}\n")
                        f.write(f"{password}")
                    print("Wi-Fi credentials saved!")
                except Exception as e:
                    print("Error saving Wi-Fi credentials:", e)
                
                # Serve a response confirming the Wi-Fi connection attempt
                response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
                <html><body><h1>Connecting to Wi-Fi...</h1></body></html>"""
                cl.send(response)
                cl.close()
                break

        else:
            # Serve the captive portal HTML page
            response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Wi-Fi Setup</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f0f4f8;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        background-color: #ffffff;
                        padding: 30px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        width: 100%;
                        max-width: 400px;
                    }
                    h1 {
                        font-size: 24px;
                        text-align: center;
                        color: #333333;
                        margin-bottom: 20px;
                    }
                    label {
                        font-size: 16px;
                        color: #333333;
                        margin-bottom: 8px;
                        display: block;
                    }
                    input[type="text"], input[type="password"] {
                        width: 100%;
                        padding: 12px;
                        margin: 8px 0;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        box-sizing: border-box;
                        font-size: 16px;
                    }
                    input[type="submit"] {
                        width: 100%;
                        padding: 14px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 16px;
                    }
                    input[type="submit"]:hover {
                        background-color: #45a049;
                    }
                    .footer {
                        text-align: center;
                        margin-top: 20px;
                        font-size: 12px;
                        color: #777777;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Wi-Fi Setup</h1>
                    <form method="POST" action="/setup">
                        <label for="ssid">SSID:</label>
                        <input type="text" name="ssid" id="ssid" placeholder="Enter Wi-Fi name" required><br>

                        <label for="password">Password:</label>
                        <input type="password" name="password" id="password" placeholder="Enter Wi-Fi password" required><br>

                        <input type="submit" value="Connect">
                    </form>
                    <div class="footer">
                        <p>If you're having trouble, please make sure the Wi-Fi credentials are correct.</p>
                    </div>
                </div>
            </body>
            </html>"""
            cl.send(response)
            cl.close()