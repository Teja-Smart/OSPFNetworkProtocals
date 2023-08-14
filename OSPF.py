#https://pythontic.com/modules/socket/udp-client-server-example
#NAME: DRONADULA TEJA
# Roll Number: CS20B026
# Course: CS3205 Jan. 2023 semester
# Lab number: 4
# Date of submission: 12 APR (12 hrs late)
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): <fill>
import socket
import sys
import os
import time
from threading import Thread
import random

n = len(sys.argv)

#python3 OSPF.py -i id -f input -o output -h 1 -a 3 -s 30 &


id = 1
infile = "input.txt"
outfile = "output-" + str(id) + ".txt"
HELLO_INTERVAL = 1
LSA_INTERVAL = 5
SPF_INTERVAL = 20
ENDTIME = 30
seqNotobesent = 0
INF = 1e10
startport = 60000

for i in range(n):
    tmp = sys.argv[i]
    if tmp == "-i":
        id = int(sys.argv[i + 1])
    if tmp == "-f":
        infile = sys.argv[i + 1] + ".txt"
    if tmp == "-o":
        outfile = sys.argv[i + 1] + "-" + str(id) + ".txt"
    if tmp == "-h":
        HELLO_INTERVAL = float(sys.argv[i + 1])
    if tmp == "-a":
        LSA_INTERVAL = float(sys.argv[i + 1])
    if tmp == "-s":
        SPF_INTERVAL = float(sys.argv[i + 1])  

portNumber = startport + id
bufferSize = 1024


adjlist = []

finput = open(infile, 'r')
foutput = open(outfile, 'w')
INPUT = finput.readlines()

N = int(INPUT[0].split()[0])
M = int(INPUT[0].split()[1])

mcostDict = [[int(INF) for i in range(N + 1)] for j in range(N + 1)]
McostDict = [[int(INF) for i in range(N + 1)] for j in range(N + 1)]
Costs = [[int(INF) for i in range(N + 1)] for j in range(N + 1)]

for i in range(N + 1):
    Costs[i][i] = 0

for i in range(M):
    Line = INPUT[i + 1].split()
    x = int(Line[0])
    y = int(Line[1])
    mC = int(Line[2])
    MC = int(Line[3])
    mcostDict[x][y] = mC
    McostDict[x][y] = MC
    mcostDict[y][x] = mC
    McostDict[y][x] = MC
    if x == id:
        adjlist.append(y)
    if y == id:
        adjlist.append(x)


lastseqNocame = [-1 for i in range(N + 1)]


# Create a UDP socket at client side
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind(("localhost", startport + id))

#generating HELLOS
def generateHELLO():
    global UDPSocket

    while True:
        for j in adjlist:
            hellomsg = "HELLO " + str(id)
            serverAddressPort = ("localhost", startport + j)
            UDPSocket.sendto(hellomsg.encode(), serverAddressPort)
        time.sleep(HELLO_INTERVAL)

#generating LSAs
def generateLSA():
    global seqNotobesent
    global UDPSocket
    global Costs

    while True:
        LSAmessage = "LSA " + str(id) + " " + str(seqNotobesent) + " "
        seqNotobesent += 1
        LSAmessage += str(len(adjlist)) + " "
        for j in adjlist:
            LSAmessage += str(j) + " " + str(Costs[id][j]) + " "
        
        for j in adjlist:
            serverAddressPort = ("localhost", startport + j)
            UDPSocket.sendto(LSAmessage.encode(), serverAddressPort)
        time.sleep(LSA_INTERVAL)

#find shortest paths
def findshortestpaths():
    global UDPSocket
    global Costs

    CostsCopy = Costs.copy()

    curtime = 0
    while True:
        print("Routing Table for Node No. " + str(id) + " at Time " + str(curtime) +"\n")
        foutput.write("Routing Table for Node No. " + str(id) + " at Time " + str(curtime) +"\n")
        foutput.write("Destination|           Path           | Cost  \n")

        # print("Costs of ", id, " = ")
        # for i in range(1, N + 1):
        #     for j in range(1, N + 1):
        #         print(Costs[i][j], end = ' ')
        #     print()
        dist = [int(INF) for i in range(N + 1)]
        sptSet = [0 for i in range(N + 1)]
        p = [-1 for i in range(N + 1)]
        src = id
        dist[src] = 0
        for cout in range(N):
            u = -1
            mdist = INF
            for x in range(1, N + 1):
                if (sptSet[x] == 0) and (dist[x] < mdist):
                    u = x
                    mdist = dist[x]
            sptSet[u] = 1
            
            for v in range(1, N + 1):
                if (sptSet[v] == 0) and (dist[v] > dist[u] + CostsCopy[u][v]):
                    dist[v] = dist[u] + CostsCopy[u][v]
                    p[v] = u
        
        # print("Dijkstea", dist, p, sptSet)
        for v in range(1, N + 1):
            if v == src:
                continue
            if p[v] == -1:
                foutput.write(str(v) + "   No path     No Path  \n")
            else:
                minpath = []
                u = v
                while u != -1:
                    minpath.append(u)
                    u = p[u]
                minpath.reverse()
                strminpath = str(minpath[0])
                for i in range(1, len(minpath)):
                    strminpath += "-" + str(minpath[i])
                foutput.write(str(v) + "  " + strminpath + "  " + str(dist[v]) + "\n")
        curtime += SPF_INTERVAL
        time.sleep(SPF_INTERVAL)
    

def endProgram():
    time.sleep(ENDTIME)
    # for i in range(1, N + 1):
    #     for j in range(1, N + 1):
    #         print(Costs[i][j], end = " ")
    #     print()
    foutput.close()
    os._exit(0)


thread_end = Thread(target = endProgram, args = ())
thread_end.start()

thread_hello = Thread(target = generateHELLO, args = ())
thread_hello.start()

thread_LSA = Thread(target = generateLSA, args = ())
thread_LSA.start()

thread_SPF = Thread(target = findshortestpaths, args = ())
thread_SPF.start()


UDPSendingSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    msgFromServer = UDPSocket.recvfrom(bufferSize)
    message = msgFromServer[0].decode().split()
    address = msgFromServer[1]
    # print("Recieved = ", id, message)
    if message[0] == "HELLO":
        i = int(message[1])
        Costs[id][i] = random.randint(mcostDict[id][i], McostDict[id][i])
        helloreply = "HELLOREPLY " + str(id) + " " + str(i) + " " + str(Costs[id][i])
        UDPSendingSocket.sendto(helloreply.encode(), ("localhost", startport + i))
        # print(id, helloreply, startport + i, i)
        # Address = ("localhost", startport + int(id + 1))
    if message[0] == "HELLOREPLY":
        # print("YESS HELLOREPLY")
        i = int(message[1])
        j = int(message[2])
        cij = int(message[3])
        Costs[i][j] = cij
        # print("Hello reply costs = ", i, j, Costs[i][j])
    
    if message[0] == "LSA":
        i = int(message[1])
        seqnoofi = int(message[2])
        degofi = int(message[3])
        if seqnoofi > lastseqNocame[i]:
            # print("LSA recieved by ", id, message)
            lastseqNocame[i] = seqnoofi
            for j in range(degofi):
                u = int(message[4 + j * 2])
                w = int(message[5 + j * 2])
                Costs[i][u] = w
            for j in adjlist:
                Address = ("localhost", startport + j)
                UDPSendingSocket.sendto(msgFromServer[0], Address)
    
UDPSocket.close()