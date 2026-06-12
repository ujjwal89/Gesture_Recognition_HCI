import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
prevTime = 0

detector=  htm.handDetector()

'''
Volume control using pycaw (Python Core Audio Windows Library)  author="Andre Miras", MIT license
https://github.com/AndreMiras/pycaw
'''


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minVol,maxVol = volRange[0],volRange[1]
vol,volBar,volPer = 0,400,0


while True:
    success, img = cap.read()
    img = detector.handLandMarks(img)
    lmList, bbox = detector.findHandPosition(img,draw=False)
    if len(lmList)!=0:
        # print(lmList[4],lmList[8]) # Getting the tip of index finger and the thumb

        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2 # Caclulating the centeral point of the line

        # Highliting the fingertips and drawing a connecting line between them
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        # Caculating length of the line
        length = math.hypot(x2-x1, y2-y1)
        if length < 50:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED) 

        # Hand range:- 50 to 300
        # Volume range:- -65 to 0
        vol = np.interp(length,[30,210],[minVol,maxVol])
        volBar = np.interp(length,[30,210],[400,150])
        volPer = np.interp(length,[30,210],[0,100])
        volume.SetMasterVolumeLevel(vol, None) 

    # Displaying fps
    cTime = time.time()
    fps = 1/(cTime-prevTime)
    prevTime = cTime


    cv2.rectangle(img,(50,145),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,str(int(fps)),(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.putText(img,f"{int(volPer)}%",(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()