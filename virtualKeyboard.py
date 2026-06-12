import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap=cv2.VideoCapture(0)
cap.set(3,1300)
cap.set(4,720)

detector = HandDetector(detectionCon=1)

keys=[["1","2","3","4","5","6","7","8","9","0"],
      ["Q","W","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L",";"],
      ["Z","X","C","V","B","N","M",",",".","/"]]

FinalText=""

keyboard=Controller()

def drawAll(img,buttonList):
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(200,200,0),cv2.FILLED)
        cv2.putText(img,button.text,(x+15,y+60),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),4)
    return img

class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos=pos
        self.size=size
        self.text=text
        


    
buttonList=[]
for i in range(len(keys)):
        for x,key in enumerate(keys[i]):
            buttonList.append(Button([100*x+50,100*i+40],key))

while True:
    success, img = cap.read()
    img=cv2.flip(img,1)

    img = detector.findHands(img)
    lmList, bboxInfo=detector.findPosition(img)
    img= drawAll(img,buttonList)
    
    
    if lmList:
         for button in buttonList:
              x,y=button.pos
              w,h=button.size

              if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h :
                    cv2.rectangle(img,(x-5,y-5),(x+w,y+h),(200,0,200),cv2.FILLED)
                    cv2.putText(img,button.text,(x+15,y+60),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),4)

                    l,_,_=detector.findDistance(8,12,img,draw=False)

                    if l<35:
                        keyboard.press(button.text)
                        cv2.rectangle(img,button.pos,(x+w,y+h),(20,10,200),cv2.FILLED)
                        cv2.putText(img,button.text,(x+15,y+60),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),4)
                        FinalText+=button.text
                        sleep(0.3)

    cv2.rectangle(img,(50,450),(700,550),(200,0,200),cv2.FILLED)
    cv2.putText(img,FinalText,(60,520),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),4)
    
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;

cap.release()
cv2.destroyAllWindows()