from camera_module import Camera
from wifi import WiFi
from auth import load_secrets, env
from streaming_server import StreamingServer
from network_communication import CommunicationManager
from configurations import UNICAST_PORT, MULTICAST_GROUP, MULTICAST_PORT
from logger import Logger
from time import sleep
from led import set_color
import machine

log = Logger(name="Main", level="INFO")

def start():
    # Load secrets: TOKEN, AP, PW
    load_secrets()
    secret_token = env.get('secret_token')
    ap = env.get('AP')  # Access Point (WiFi SSID)
    pw = env.get('PW')  # WiFi Password
    
    try:
        with WiFi(ap, pw) as wifi, Camera() as camera:
            if wifi.is_connected() and camera.is_ready():
                # Initialize and start the streaming server
                streaming_server = StreamingServer(
                    camera=camera,
                    wifi=wifi,
                    SECRET_TOKEN=secret_token)
                streaming_server.start()
                
                sleep(1)
                
                # Initialize communication manager for uni/multi casting
                comm_manager = CommunicationManager(
                    unicast_port=UNICAST_PORT, 
                    multicast_group=MULTICAST_GROUP, 
                    multicast_port=MULTICAST_PORT)
                
                # Start listeners
                comm_manager.start_multicast_listener()
                comm_manager.start_unicast_listener()
                
                # TEST MULTICAST
                comm_manager.send_multicast("Hello, Multicast Group!")
            else:
                if not wifi.is_connected():
                    log.error("WiFi not connected.")
                    
                if not camera.is_ready():
                    log.error("Camera not ready. Please do machine.reset()")
                    
                log.error("System not ready. Please restart")
                
    except KeyboardInterrupt:
        log.error("Force program stop!")
    except RuntimeError as e:
        log.error(f"Error during initialization: {e}")
        machine.reset()
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    start()
