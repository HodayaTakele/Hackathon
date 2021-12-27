import socket
import struct
import threading
import time
import concurrent
from concurrent.futures import thread
# from termcolor import colored


class Server:
    def __init__(self):
        # initialize UDP socket
        self.UDPSocket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # initialize TCP socket
        self.TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostName = socket.gethostname()
        self.hostIP = socket.gethostbyname(self.hostName)
        self.hostPort = 2009
        self.teams = []
        self.DevNet = "172.1.255.255"
        self.tcpConnectionPort = 13117
        self.gemeEndTime = 10
        self.bufferSize

    def brodcastUdpOffer(self):
        # sending out "offer" announcements evry 1 second
        threading.Timer(1.0, self.brodcastUdpOffer).start()
        offerMessage = struct.pack("Ibh", 0xabcddcba, 0x2, self.hostPort)
        self.UDPSocket.sendto(
            offerMessage, (self.DevNet, self.tcpConnectionPort))
