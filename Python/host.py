import threading
import socket

HOST_IP = "192.168.207.35"
HOST_PORT = 6565

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((HOST_IP, HOST_PORT))

PLAYER1_IP = ""
PLAYER2_IP = ""


def listen_to_udp():
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(f'\nIncoming message: {data.decode("utf-8")}')


def listen_to_input():
    while True:
        message = input('Chat input: ')
        sock.sendto(bytes(str(message), encoding='utf8'), ("192.168.207.69", 6565))


if __name__ == "__main__":
    t1 = threading.Thread(target=listen_to_input, args=())
    t2 = threading.Thread(target=listen_to_udp, args=())

    t1.start()
    t2.start()
