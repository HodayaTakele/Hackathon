import socket
import struct
import time
#import getch
import msvcrt
# from termcolor import colored


def lookingForServer():
    # state one:
    # multicasts a UDP datagram(multi clients)
    UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Servers broadcast their announcements with destination port 13117 using UDP:
    UDPSocket.bind(("", 13117))
    messageFromServer = None
    while messageFromServer is None:
        try:
            UDPSocket.settimeout(0.5)
            # the numBytes2Get = 1024
            # messageFromServer = (receivedData, addr), #addr[0] = IP, adder[1] = portUdp
            messageFromServer = UDPSocket.recvfrom(1024)
        except:
            continue
    #addr[0] = IP, adder[1] = portUdp
    return messageFromServer


def getPortNum(receivedData):
    try:
        # if the message format is "Ibh" but the message incorrect - return None
        # un pack the message that the client got from the server, from hex to dec
        MsgUnPack = struct.unpack("Ibh", receivedData)
        # cheking the message:
        if MsgUnPack[0] != 2882395322 or MsgUnPack[1] != 2 or MsgUnPack[2] < 1024 or MsgUnPack[2] > 32768:
            return None
    # if the message format isn't "Ibh" - return None
    except:
        return None
    return MsgUnPack[2]


def connectingToServer(addr, portNum):
    # connecting via TCP
    #connect(host, port)
    tcpIp, UDPport = addr
    TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPSocket.connect(tcpIp, portNum)
    TCPSocket.send(bytes("Solving_With_A_Smile"+"\n", "utf-8"))
    welcomeData = TCPSocket.recv(1024).decode("utf-8")
    print(welcomeData)  # print welcome msg
    # game state
    startGameMode(TCPSocket)


def startGameMode(TCPSocket):
    try:
        # timer of 10 sec
        startTime = time.time()
        while time.time() - startTime < 10:
            #char = getch.getch()
            char = msvcrt.getch()
            if char.isdigit():
                TCPSocket.sendall(bytes(char, "utf-8"))
            else:
                print("The input supposed to be a digit !")
        summaryMessage = TCPSocket.recv(1024).decode("utf-8")
        # print(colored(summaryMessage,'blue'))
        print(summaryMessage)
    except:
        return


def startClient():
    print("Client started, listening for offer requests...")
    while True:
        receivedData, addr = lookingForServer()
        print(addr)
        print(f"Received offer from {addr[0]}, attempting to connect...")
        portNum = getPortNum(receivedData)  # could be None!
        if portNum is None:
            # continue wait for other port
            continue
        try:
            connectingToServer(addr, portNum)
        except:
            continue
        print("Server disconnected, listening for offer requests...")
        # the client continue to waiting for offer messages


startClient()
