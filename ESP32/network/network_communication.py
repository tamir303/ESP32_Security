import socket
import struct
import _thread
from time import sleep
from logger import Logger

log = Logger(name="Network_Communication", level="DEBUG")

class Unicast:
    """
    Handles unicast communication (point-to-point).
    """
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.host, self.port))
            log.info(f"Unicast socket bound to {self.host}:{self.port}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize unicast socket: {e}")

    def send_message(self, message, target_ip, target_port):
        """
        Sends a unicast message to a specific target.
        """
        try:
            self.sock.sendto(message.encode(), (target_ip, target_port))
            log.info(f"Sent unicast message to {target_ip}:{target_port}")
        except Exception as e:
            raise Exception(f"Error sending unicast message: {e}")

    def receive_message(self):
        """
        Receives a unicast message.
        """
        try:
            data, addr = self.sock.recvfrom(1024)
            log.info(f"Received message from {addr}: {data.decode()}")
            return data, addr
        except Exception as e:
            raise Exception(f"Error receiving unicast message: {e}")

class Multicast:
    """
    Handles multicast communication (group communication).
    """
    def __init__(self, group_ip='224.1.1.1', port=5007):
        self.group_ip = group_ip
        self.port = port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', self.port))

            # Join multicast group
            group = struct.pack("4s", bytes(map(int, self.group_ip.split("."))))
            mreq = group + struct.pack("I", 0)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            log.info(f"Joined multicast group {self.group_ip}:{self.port}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize multicast socket: {e}")

    def send_message(self, message):
        """
        Sends a multicast message to the group.
        """
        try:
            self.sock.sendto(message.encode(), (self.group_ip, self.port))
            log.info(f"Sent multicast message to {self.group_ip}:{self.port}")
        except Exception as e:
            raise Exception(f"Error sending multicast message: {e}")

    def receive_message(self):
        """
        Receives a multicast message.
        """
        try:
            data, addr = self.sock.recvfrom(1024)
            log.info(f"Received multicast message from {addr}: {data.decode()}")
            return data, addr
        except Exception as e:
            raise Exception(f"Error receiving multicast message: {e}")


class CommunicationManager:
    """
    Manages unicast and multicast communication in separate threads.
    """
    def __init__(self, unicast_port=5000, multicast_group='224.1.1.1', multicast_port=5007):
        try:
            self.unicast = Unicast(port=unicast_port)
            self.multicast = Multicast(group_ip=multicast_group, port=multicast_port)
        except Exception as e:
            raise RuntimeError(f"Error initializing CommunicationManager: {e}")

    def start_multicast_listener(self):
        """
        Starts a listener thread for multicast messages.
        """
        def multicast_thread():
            while True:
                try:
                    data, addr = self.multicast.receive_message()
                    log.info(f"Multicast received: {data.decode()} from {addr}")
                except Exception as e:
                    log.error(f"Error in multicast listener thread: {e}")
                sleep(1)

        try:
            _thread.start_new_thread(multicast_thread, ())
        except Exception as e:
            raise Exception(f"Error starting multicast listener thread: {e}")

    def start_unicast_listener(self):
        """
        Starts a listener thread for unicast messages.
        """
        def unicast_thread():
            while True:
                try:
                    data, addr = self.unicast.receive_message()
                    log.info(f"Unicast received: {data.decode()} from {addr}")
                except Exception as e:
                    log.error(f"Error in unicast listener thread: {e}")
                sleep(1)

        try:
            _thread.start_new_thread(unicast_thread, ())
        except Exception as e:
            raise RuntimeError(f"Error starting unicast listener thread: {e}")

    def send_multicast(self, message):
        """
        Sends a multicast message.
        """
        try:
            self.multicast.send_message(message)
        except Exception as e:
            raise Exception(f"Error sending multicast message: {e}")

    def send_unicast(self, message, target_ip, target_port):
        """
        Sends a unicast message.
        """
        try:
            self.unicast.send_message(message, target_ip, target_port)
        except Exception as e:
            raise Exception(f"Error sending unicast message: {e}")
