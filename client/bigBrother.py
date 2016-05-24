#Sends webcam feed to flaschen-taschen
#writen by Sean Gray
#Questions?Comments? Email:SeanGrayiit@gmail.com

#requires intailation of opencv library for webcam processing
import numpy as nb
import cv2
import flaschen
import sys

UDP_IP= 'localhost'
UDP_PORT= 1337
ft = flaschen.Flaschen(UDP_IP,UDP_PORT,45,35)
cam=cv2.VideoCapture(0)
cam.set(3, 45)
cam.set(4, 35)

while(True):
    work,frame=cam.read() # work is a boolean if it worked, frame has data
    #Scales image to flaschen size
    r = 35.0 / frame.shape[1]
    dim = (35, int(frame.shape[0] * r))
    resized=cv2.resize(frame, dim,interpolation = cv2.INTER_AREA);
    #opencv stores in 3 dimention lists of bgr
    #converts to rgb and sets each pixel
    for x in xrange(0,ft.height):
        for y in xrange(0,dim[1]):
            b = (resized[y][x][0]);
            g = (resized[y][x][1]);
            r = (resized[y][x][2]);
            color=(r,g,b)
            ft.set(x,y,color)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    ft.send()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
