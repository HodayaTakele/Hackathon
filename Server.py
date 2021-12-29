import socket
import struct
import threading
import time
import concurrent
from concurrent.futures import thread
import random
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
        self.udpBroadcastPort = 13117
        self.gemeEndTime = 10
        self.bufferSize = 1024

    def brodcastUdpOffer(self):
        ''' 
        This function is responsible for sending out "offer" announcements
        to all clients in the network evry 1 second via UDP
        '''
        # Start and set the thread to send offers every 1 sec.
        threading.Timer(1.0, self.brodcastUdpOffer).start()
        # Pack the message in a udp format.
        offerMessage = struct.pack("Ibh", 0xabcddcba, 0x2, self.hostPort)
        # brodacast the message to all clients connected to the net
        self.UDPSocket.sendto(
            offerMessage, (self.DevNet, self.udpBroadcastPort))
        # offerMessage, (self.hostIP, self.udpBroadcastPort))

    def waitForClient(self):
        '''
        First stage of the server
        The server start brodcast offers to the clients in the network via UDP 
        while listning to join request from clients via TCP.
        this function update the self.team with the first two teams that request to join
        we leave this this stage when two clients joined the game.
        '''
        UdpBroadcastThread = threading.Thread(target=server.brodcastUdpOffer)
        UdpBroadcastThread.start()
        while len(server.teams) < 2:
            self.TCPSocket.settimeout(0.1)
            try:
                clientSocket, clientAddress = self.TCPSocket.accept()
                teamName = clientSocket.recv(self.bufferSize).decode("utf-8")
                time.sleep(0.1)
                self.teams.append((clientSocket, clientAddress, teamName))
            except:
                continue

    def startGameMode(self, team):
        '''

        '''
        startTime = time.time()
        while time.time() - startTime < self.gemeEndTime:
            try:
                team[0].settimeout(0.01)
                sol = team.recv(self.bufferSize).decode("utf-8")
            except:
                pass
        return (sol, team[2])

    def getMathProblem(self):
        opStr = ['+', '-', '*', '/']
        num1 = random.randrange(1, 12)
        num2 = random.randrange(num1, 50, num1)
        opIndex = random.randrange(0, 4)
        problem = str(num2) + opStr[opIndex] + str(num1)
        if opIndex == 0:
            solution = num2 + num1
        if opIndex == 1:
            solution = num2 - num1
        if opIndex == 2:
            solution = num1 * num2
        if opIndex == 3:
            solution = num2 // num1
        return problem, solution


# Game Flow
if __name__ == '__main__':
    server = Server()
    con = False
    while not con:
        try:
            server.TCPSocket.bind(("", server.hostPort))
            con = True
        except:
            pass
    server.TCPSocket.listen()
    while True:
        server.teams = []
        # Print start message
        print(f"Server started, listening on IP address {server.hostIP}")
        # Start wait for clients stage
        server.waitForClient()

        if len(server.teams) == 0:
            continue

        nameTeam1 = server.teams[0][2]
        nameTeam2 = server.teams[1][2]
        problem, solution = server.getMathProblem()
        welcomeMsg = f"Welcome to Quick Maths.\nPlayer 1: {nameTeam1}\nPlayer 2: {nameTeam2}\n==\n" \
                     f"Please answer the following question as fast as you can:\nHow much is {problem}?"

        for team in server.teams:
            team[0].send(bytes(welcomeMsg, "utf-8"))

        print(welcomeMsg)
        sol = []
        with concurrent.futures.ThreadPoolExecutor(len(server.teams)) as pool:
            for team in server.teams:
                teamSol = pool.submit(server.startGameMode, team)
                sol.append(teamSol)

        if sol[0][0] == None:
            winTeam = 'draw'
        elif sol[0][0] == solution:
            winTeam = sol[0][1]
        else:
            winTeam = sol[1][1]
        gameOverMsg = ''
        if winTeam == 'draw':
            gameOverMsg = f"Game over!\nThe correct answer was {solution}!\n\nit's a draw"
        else:
            gameOverMsg = f"Game over!\nThe correct answer was {solution}!\n\nCongratulations to the winner: {winTeam}"

        print(gameOverMsg)

        for team in server.teams:
            try:
                team[0].sendall(bytes(gameOverMsg, "utf-8"))
            except:
                continue
        for team in server.teams:
            try:
                team[0].close()
            except:
                continue
        print("Game over, sending out offer requests...")
