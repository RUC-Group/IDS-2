from multiprocessing import connection
import threading
import socket
import time

import threading
import time
 
def run():
    while True:
        print('thread running')
        global stop_threads
        if stop_threads:
            break


HOST_IP = "172.20.10.10"
HOST_PORT = 6565

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((HOST_IP, HOST_PORT))

#PLAYER1_IP = "172.20.10.2"
#PLAYER2_IP = "172.20.10.4"

PLAYER1 = ""
PLAYER2 = ""

def await_ready():
    while True:
        
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        global PLAYER1
        global PLAYER2
        print(f'\nIncoming message {data.decode("utf-8")}') 
        if PLAYER1=="":
            PLAYER1=addr
        if not(addr==PLAYER1):
            PLAYER2=addr
            sock.sendto(bytes(str("received"), encoding='utf8'), PLAYER1)
            sock.sendto(bytes(str("You are player 1"), encoding='utf8'), PLAYER1)

            sock.sendto(bytes(str("received"), encoding='utf8'), PLAYER2)
            sock.sendto(bytes(str("received. You are player 2"), encoding='utf8'), PLAYER2)
            global connected
            connected=True
            global waitInput
            waitInput=True
            break

def listen_to_udp():
    while True:
        global player1_input,player2_input,PLAYER1,PLAYER2,waitInput
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(addr[0])
        print(f'\nIncoming message {data.decode("utf-8")}')
        if addr==PLAYER1:
            print(f'\nplayer 1 throws {data.decode("utf-8")}')
            player1_input={data.decode("utf-8")}
        if addr==PLAYER2:
            print(f'\nplayer 2 throws {data.decode("utf-8")}')
            player2_input={data.decode("utf-8")}
        if not(player1_input=="") and not(player2_input==""):
            waitInput=False
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

player1_input=""
player2_input=""

while True:
    if not(connected):
        if not(t3.is_alive()):
            t3.start()
            t3.join()
    
    if waitInput:
        #t3.join()
        if not(t2.is_alive()):
            t2.start()
            t2.join()

