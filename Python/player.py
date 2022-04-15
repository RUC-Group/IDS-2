import time
import cv2
import numpy as np
from PIL import Image
from keras import models
import tensorflow as tf
import threading
import socket

# font
font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (50, 50)
  
# fontScale
fontScale = 1
   
# Blue color in BGR
color = (255, 0, 0)
  
# Line thickness of 2 px
thickness = 2

#UDP_IP = "192.168.137.35"
UDP_IP = socket.gethostbyname(socket.gethostname())
UDP_PORT = 6566

HOST_IP = "192.168.137.69"
HOST_PORT = 6565



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))


model = models.load_model("keras_model.h5")
video = cv2.VideoCapture(0)
playerReady = True
readPlayerInput = False
waitForHost = False
hostResponse = ""
playerScore = 0

while True:
        data, addr = sock.recvfrom(1024)

        key=cv2.waitKey(1)

        if playerReady:
                sock.sendto(bytes(str("ready"), encoding='utf8'), (HOST_IP, HOST_PORT))
                #time.sleep(3)
                #data, addr = sock.recvfrom(1024)
                if data.decode("utf-8") == "received":
                        playerReady = False
                        readPlayerInput = True

        
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
                #print(labels[np.argmax(prediction)])

                frame = cv2.putText(frame,labels[np.argmax(prediction)], org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)

                cv2.imshow("Prediction", frame)

                #[PROJECT] PLAYER-PROMPTED CONFIRMATION OF HAND-GESTURE:
                
                if key == ord('c'):

                        #[PROJECT] TRANSMISSION OF PREDICTION TO HOST:
                        print("\nHand gesture to send: " + labels[np.argmax(prediction)])
                        
                        sock.sendto(bytes(str(labels[np.argmax(prediction)]), encoding='utf8'), (HOST_IP, HOST_PORT))
                        
                        print("Waiting for host to respond...")

                        waitForHost = True
                        readPlayerInput = False
                        
        if waitForHost:
                #CAN'T CALL "DATA" HERE, BECAUSE IT'S OUT OF SCOPE. MAKE IF-STATEMENTS IN "LISTEN TO UDP"
                if hostResponse=="":
                        hostResponse = data.decode("utf-8")
                if hostResponse == "WON":
                        print("You've won with your " + labels[np.argmax(prediction)] + "!") 
                        readPlayerInput = True
                        waitForHost = False
                        hostResponse=""

                        playerScore += 1
                        print("Your Score: "+ playerScore)

                if hostResponse == "LOST":
                        print("You've lost with your " + labels[np.argmax(prediction)] + "!")
                        readPlayerInput = True
                        waitForHost = False
                        hostResponse=""
                
                if hostResponse == "DRAW":
                        print("You've both drawn " + labels[np.argmax(prediction)] + ", neither of you win")
                        readPlayerInput = True
                        waitForHost = False
                        hostResponse=""

        if key == ord('q'):
                break

video.release()
cv2.destroyAllWindows()