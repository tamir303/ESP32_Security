import network
from time import sleep

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
                        print("WiFi connected:", self.connection_info)
                        return True
                    else:
                        print("WiFi not ready. Wait...")
                        sleep(2)
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
