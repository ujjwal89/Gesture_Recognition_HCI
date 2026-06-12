import cv2
import mediapipe as mp
import math

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCoff=0.5, trackingCoff = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCoff = detectionCoff
        self.trackingCoff = trackingCoff

        self.handsInitial = mp.solutions.hands
        
        '''
        Hands() --> Parameters include static_image_mode --> if set to false it will only track when it has good confidence level. When it is set true it will track continously which makes it slow. max_num_hands, minimum_detection_confidence and minimum_tracking_confidence.
        '''

        self.hands = self.handsInitial.Hands(self.mode,self.maxHands,1,self.detectionCoff,self.trackingCoff)
        self.drawLDM = mp.solutions.drawing_utils # Methods provided by mediapipe for drawing landmarks
        self.tipIds = [4,8,12,16,20] # Ids of the tip of the fingers

    def handLandMarks(self,img,draw=True):
        
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLDM in self.results.multi_hand_landmarks:
                if draw:
                    # Drawing landmarks on original image.
                    self.drawLDM.draw_landmarks(img, handLDM, self.handsInitial.HAND_CONNECTIONS)

        return img
    
    def findHandPosition(self,img,handNo=0,draw=True,):
        xList = []
        yList = []
        bbox = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,landMrks in enumerate(myHand.landmark):
                height, width, channel = img.shape
                        
                    # Calculating the pixels by multiplying the ratios (x,y) we get from landmarks with the width and the height respectively
                cx, cy = int(landMrks.x*width), int(landMrks.y*height)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id,cx,cy])

                if draw:
                # Displaying a landmark with a specific id from (0,20)
                    cv2.circle(img,(cx,cy),5,(255,0,255), cv2.FILLED)

                    
            xMin, xMax = min(xList),max(xList)
            yMin, yMax = min(yList), max(yList)
            bbox = xMin, yMin, xMax, yMax

            if draw:
                cv2.rectangle(img, (xMin - 20, yMin - 20), (xMax + 20, yMax + 20),(0, 255, 0), 2)

        return self.lmList, bbox
    
    def fingersUp(self):
        fingers = []
        if self.lmList and self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if self.lmList and self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
    

    def findDistance(self,p1,p2,img,draw=True,r=15,t=3):
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]

        cx,cy = (x1+x2)//2, (y1+y2)//2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]
 