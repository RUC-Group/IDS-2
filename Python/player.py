import cv2
import numpy as np
from PIL import Image
from keras import models
import tensorflow as tf
import threading
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 6565



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))


model = models.load_model("Python/keras_model.h5")
video = cv2.VideoCapture(0)
readPlayerInput = True
waitForHost = False
playerScore = 0

def listen_to_udp():
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(f'\nIncoming message: {data.decode("utf-8")}')


def listen_to_input():
    while True:
        message = input('Chat input: ')
        sock.sendto(bytes(str(message), encoding='utf8'), (UDP_IP, 6566))

if __name__ == "__main__":
    t1 = threading.Thread(target=listen_to_input, args=())
    t2 = threading.Thread(target=listen_to_udp, args=())

    t1.start()
    t2.start()


while False:

        key=cv2.waitKey(1)

        if readPlayerInput:
                _, frame = video.read()
                #Convert the captured frame into RGB
                im = Image.fromarray(frame, 'RGB')

                #Resizing into dimensions you used while training
                im = im.resize((224,224))
                img_array = np.array(im)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = (img_array.astype(np.float32) / 127.0) - 1

                #Calling the predict function using keras
                prediction = model.predict(img_array)

                #print(prediction.shape)
                labels = ['scissor', 'rock', 'paper']
                print(labels[np.argmax(prediction)])

                cv2.imshow("Prediction", frame)

                #[PROJECT] PLAYER-PROMPTED CONFIRMATION OF HAND-GESTURE:
                if key == ord('c'):

                        #[PROJECT] TRANSMISSION OF PREDICTION TO HOST:
                        print("Hand gestuqre to send: " + labels[np.argmax(prediction)])
                        print("Waiting for host to respond...")

                        waitForHost = True
                        readPlayerInput = False
                        
        if waitForHost:
                if key == ord('w'):
                        print("You've beaten the opponents' " + "?" +  " with your " + labels[np.argmax(prediction)] + "!") 
                        readPlayerInput = True
                        waitForHost = False

                        playerScore += 1
                        print(playerScore)

                if key == ord('l'):
                        print("You've lost to the opponents' " + "?" + " with your " + labels[np.argmax(prediction)] + "!")
                        readPlayerInput = True
                        waitForHost = False

        if key == ord('q'):
                break

video.release()
cv2.destroyAllWindows()