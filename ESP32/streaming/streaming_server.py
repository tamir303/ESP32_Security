import socket as soc
import _thread
from cam_config import hdr
from auth import is_authenticated, SECRET_TOKEN
from wifi import WiFi
from camera_module import Camera

class StreamingServer:
    def __init__(self, camera: Camera, wifi: WiFi, port=80):
        self.camera = camera
        self.wifi = wifi
        self.port = port
        self.server_socket = None

    def setup_server(self):
        addr = soc.getaddrinfo('0.0.0.0', self.port)[0][-1]
        self.server_socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        self.server_socket.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
        self.server_socket.bind(addr)
        self.server_socket.listen(1)
        
        # Retrieve IP address and print streaming URL
        ip_address = self.wifi.get_ip_address()  # Assuming `get_ip_address()` returns the IP as a string
        if ip_address:
            print(f"Streaming server started on http://{ip_address}:{self.port}?token={SECRET_TOKEN}")
        else:
            print("Unable to retrieve IP address.")

    def start_streaming(self):
        if not self.wifi.is_connected() or not self.camera.is_ready():
            print("System not ready for streaming.")
            return

        self.setup_server()
        while True:
            client_socket, client_address = self.server_socket.accept()
            print('Request from:', client_address)
            request = client_socket.recv(200)

            if not is_authenticated(request):
                # Send 403 Forbidden response if authentication fails
                client_socket.send("HTTP/1.1 403 Forbidden\r\n\r\n")
                client_socket.close()
                continue
            
            # Authenticated - Start streaming
            client_socket.write(b'%s\r\n\r\n' % hdr['stream'])
            put = client_socket.write
            hr = hdr['frame']

            while True:
                try:
                    put(b'%s\r\n\r\n' % hr)
                    put(self.camera.capture_image())
                    put(b'\r\n')  # Send and flush the buffer
                except Exception as e:
                    print("TCP send error:", e)
                    client_socket.close()
                    break

    def start(self):
        self.streaming_thread = _thread.start_new_thread(self.start_streaming, ())