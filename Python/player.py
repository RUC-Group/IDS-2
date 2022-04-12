from tkinter.tix import INTEGER
import cv2
import numpy as np
from PIL import Image
from keras import models
import tensorflow as tf

model = models.load_model('C:/Users/Albi/OneDrive/RUC NOTER/4th semester/Interactive Digital Systems/IDS Mini-project/IDS project 2/keras_model.h5')
video = cv2.VideoCapture(0)
readPlayerInput = True
waitForHost = False
playerScore = 0

while True:

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