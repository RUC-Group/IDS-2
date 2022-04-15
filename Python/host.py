import math
import threading
import socket

import threading
import time
from unittest import result

class player:
    PLAYER_IP = ""
    player_input=0

HOST_IP = "172.20.10.10"
HOST_PORT = 6565

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((HOST_IP, HOST_PORT))

#PLAYER1_IP = "172.20.10.2"
#PLAYER2_IP = "172.20.10.4"

PLAYER1 = player()
PLAYER2 = player()

LabelToNumber = {
        "rock" : 1,
        "paper" : 2,
        "scissor" : 3
}

def await_ready():
    while True:
        
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        global PLAYER1
        global PLAYER2
        print(f'\nIncoming message {data.decode("utf-8")}') 
        if PLAYER1.PLAYER_IP=="":
            PLAYER1.PLAYER_IP=addr
        if not(addr==PLAYER1.PLAYER_IP):
            PLAYER2.PLAYER_IP=addr
            sock.sendto(bytes(str("received"), encoding='utf8'), PLAYER1.PLAYER_IP)
            sock.sendto(bytes(str("You are player 1"), encoding='utf8'), PLAYER1.PLAYER_IP)

            sock.sendto(bytes(str("received"), encoding='utf8'), PLAYER2.PLAYER_IP)
            sock.sendto(bytes(str("received. You are player 2"), encoding='utf8'), PLAYER2.PLAYER_IP)
            global connected
            connected=True
            global waitInput
            waitInput=True
            break

def listen_to_udp():
    while True:
        global PLAYER1,PLAYER2,waitInput,processing
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(addr[0])
        print(f'\nIncoming message {data.decode("utf-8")}')
        if addr==PLAYER1.PLAYER_IP:
            print(f'\nplayer 1 throws {data.decode("utf-8")}')
            PLAYER1.player_input=int(data.decode("utf-8"))
        if addr==PLAYER2.PLAYER_IP:
            print(f'\nplayer 2 throws {data.decode("utf-8")}')
            PLAYER2.player_input=int(data.decode("utf-8"))
        if not(PLAYER1.player_input==0) and not(PLAYER2.player_input==0):
            waitInput=False
            processing=True
            break
        



def listen_to_input():
    while True:
        message = input('Chat input: ')
        sock.sendto(bytes(str(message), encoding='utf8'), PLAYER1)
        sock.sendto(bytes(str(message), encoding='utf8'), PLAYER2)

if __name__ == "__main__":
    stop_threads = False
    t1 = threading.Thread(target=listen_to_input, args=())
    t2 = threading.Thread(target=listen_to_udp, args=())
    t3 = threading.Thread(target=await_ready, args=())

    #t1.start()
    #t2.start()
    #t3.start()

connected = False
waitInput=False
processing=False

def getPlayer(value):
    if value==PLAYER1.player_input:
        return PLAYER1,PLAYER2
    else:
        return PLAYER2,PLAYER1

while True:
    if not(connected):
        if not(t3.is_alive()):
            t3.start()
            t3.join()
    
    if waitInput:
        #t3.join()
        #if not(t2.is_alive()):
         #   t2.start()
          #  t2.join()
        #global PLAYER1,PLAYER2,waitInput,processing
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(addr[0])
        print(f'\nIncoming message {data.decode("utf-8")}')
        if addr==PLAYER1.PLAYER_IP and PLAYER1.player_input==0:
            print(f'\nplayer 1 throws {data.decode("utf-8")}')
            PLAYER1.player_input=LabelToNumber[data.decode("utf-8")]
        if addr==PLAYER2.PLAYER_IP and PLAYER2.player_input==0:
            print(f'\nplayer 2 throws {data.decode("utf-8")}')
            PLAYER2.player_input=LabelToNumber[data.decode("utf-8")]
        if not(PLAYER1.player_input==0) and not(PLAYER2.player_input==0):
            waitInput=False
            processing=True
            #break

    if processing:
        maxValue = max(PLAYER1.player_input,PLAYER2.player_input)
        minValue = min(PLAYER1.player_input,PLAYER2.player_input)
        maxValuePlayer,minValuePlayer = getPlayer(maxValue)
        PLAYER1.player_input=0
        PLAYER2.player_input=0
        result = maxValue-minValue
        if result==0:
            sock.sendto(bytes(str("DRAW"), encoding='utf8'), maxValuePlayer.PLAYER_IP)
            sock.sendto(bytes(str("DRAW"), encoding='utf8'), minValuePlayer.PLAYER_IP)
            processing=False
            waitInput=True
        elif result==1:
            sock.sendto(bytes(str("WON"), encoding='utf8'), maxValuePlayer.PLAYER_IP)
            sock.sendto(bytes(str("LOST"), encoding='utf8'), minValuePlayer.PLAYER_IP)
            processing=False
            waitInput=True
        elif result==2:
            sock.sendto(bytes(str("LOST"), encoding='utf8'), maxValuePlayer.PLAYER_IP)
            sock.sendto(bytes(str("WON"), encoding='utf8'), minValuePlayer.PLAYER_IP)
            processing=False
            waitInput=True

