import network
from time import sleep
from logger import Logger

log = Logger(name="Wifi", level="DEBUG")

class WiFi:
    def __init__(self, ssid, password):
        try:
            self.ssid = ssid
            self.password = password
            self.sta = network.WLAN(network.STA_IF)
            self.sta.active(True)
            self.connection_info = ()
            
        except Exception as e:
            print(e)

    def connect(self):
        try:
            if not self.sta.isconnected():
                self.sta.connect(self.ssid, self.password)
                for _ in range(5):  # Wait for WiFi connection
                    if self.sta.isconnected():
                        self.connection_info = self.sta.ifconfig()
                        log.info(f"Connecting to WiFi: {ssid}")
                        return True
            else:
                self.connection_info = self.sta.ifconfig()
                
            return self.connection_info != ()
        
        except Exception as e:
            print(e)

    def is_connected(self):
        return self.sta.isconnected()
    
    def get_ip_address(self):
        if self.is_connected():
            return self.sta.ifconfig()[0]  # Returns the IP address
        return None
    
    def __enter__(self):
        if self.is_connected():
            log.info(f"Successfully connected to WiFi")
            return self
        else:
            log.debug(f"Attempting to connect to WiFi: {self.ssid}")
            for attempt in range(10):  # Try connecting 10 times
                if self.connect():
                    log.info(f"Successfully connected to WiFi")
                    return self
                else:
                    log.debug(f"Attempt {attempt + 1} failed. Retrying...")
                    sleep(2)
            raise RuntimeError("Failed to connect to WiFi after 10 attempts.")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
