import socket
import struct

MCAST_GRP = '239.255.255.250'  # Multicast group
MCAST_PORT = 5007              # Port


async def listen_for_multicast():
    """Listen for multicast messages from ESP32."""
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))  # Bind to multicast port

    # Add socket to multicast group
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Server listening for multicast messages...")
    while True:
        data, address = sock.recvfrom(1024)
        message = data.decode()
        print(f"Received multicast message from {address}: {message}")


