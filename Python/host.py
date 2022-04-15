import socket
from unittest import result

# player class containing an ip and an input value
class player:
    PLAYER_IP = ""
    player_input=0

# get ip
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 6565

# socket for sending and recieving data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST_IP, HOST_PORT))

PLAYER1 = player()
PLAYER2 = player()

# converter from inputs to numbers
LabelToNumber = {
        "rock" : 1,
        "paper" : 2,
        "scissor" : 3
}

connected = False
waitInput = False
processing = False

# method that finds a player from a value
def getPlayer(value):
    if value == PLAYER1.player_input:
        return PLAYER1,PLAYER2
    else:
        return PLAYER2,PLAYER1

# main loop of the host
while True:
    # state: there is no connection
    if not(connected):
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(f'\nIncoming message {data.decode("utf-8")}') 

        # if player one not defined
        if PLAYER1.PLAYER_IP=="":
            PLAYER1.PLAYER_IP=addr # define player one to be first pc to connect
        # if the most recent ip to connect isnt the player 1
        if not(addr==PLAYER1.PLAYER_IP):
            PLAYER2.PLAYER_IP=addr # define player 2 to the second adress to connect

            # inform the first player that they are player 1
            sock.sendto(bytes(str("received"), encoding='utf8'), PLAYER1.PLAYER_IP)
            sock.sendto(bytes(str("You are player 1"), encoding='utf8'), PLAYER1.PLAYER_IP)

            # inform the second player that they are player 2
            sock.sendto(bytes(str("received"), encoding='utf8'), PLAYER2.PLAYER_IP)
            sock.sendto(bytes(str("received. You are player 2"), encoding='utf8'), PLAYER2.PLAYER_IP)

            # switch state
            connected=True
            waitInput=True
            
    # state: waiting for input from the two players
    if waitInput:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes

        # if IP in msg is player 1's and player 1 doesnt have an input saved
        if addr==PLAYER1.PLAYER_IP and PLAYER1.player_input==0:
            print(f'\n({addr[0]}) player 1 throws {data.decode("utf-8")}')
            PLAYER1.player_input=LabelToNumber[data.decode("utf-8")]

        # if IP in msg is player 2's and player 2 doesnt have an input saved
        if addr==PLAYER2.PLAYER_IP and PLAYER2.player_input==0:
            print(f'\n({addr[0]}) player 2 throws {data.decode("utf-8")}')
            PLAYER2.player_input=LabelToNumber[data.decode("utf-8")]

        # if both players have input, switch state
        if not(PLAYER1.player_input==0) and not(PLAYER2.player_input==0):
            waitInput=False
            processing=True
            
    # state: processes the two player inputs
    if processing:
        # get the bigger and the smaller of the two inputs (rock = 1, paper = 2, Scissors = 3)
        maxValue = max(PLAYER1.player_input,PLAYER2.player_input)
        minValue = min(PLAYER1.player_input,PLAYER2.player_input)
        maxValuePlayer,minValuePlayer = getPlayer(maxValue)             #  get players from their inputs 
        
        # reset player inputs to 0
        PLAYER1.player_input=0
        PLAYER2.player_input=0
        
        result = maxValue-minValue # get result based on the difference of the two values

        # if the difference between players is 0, they threw the same. Send "DRAW" to both and switch state to wait for input
        if result==0:
            sock.sendto(bytes(str("DRAW"), encoding='utf8'), maxValuePlayer.PLAYER_IP)
            sock.sendto(bytes(str("DRAW"), encoding='utf8'), minValuePlayer.PLAYER_IP)
            processing=False
            waitInput=True

        # if the difference between players is 1, return "WON" to the player that threw the highest valued throw and "LOST" to the other and switch states to wait for input
        elif result==1:
            sock.sendto(bytes(str("WON"), encoding='utf8'), maxValuePlayer.PLAYER_IP)
            sock.sendto(bytes(str("LOST"), encoding='utf8'), minValuePlayer.PLAYER_IP)
            processing=False
            waitInput=True

        
        # if the difference between players is 2, return "WON" to the player that threw the lowest valued throw and "LOST" to the other and switch states to wait for input   
        elif result == 2:
            sock.sendto(bytes(str("LOST"), encoding='utf8'), maxValuePlayer.PLAYER_IP)
            sock.sendto(bytes(str("WON"), encoding='utf8'), minValuePlayer.PLAYER_IP)
            processing=False
            waitInput=True

