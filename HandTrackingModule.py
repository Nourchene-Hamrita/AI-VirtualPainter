import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self, mode=False, maxHands=2,model_complexity = 1, detectionCon =0.5, trackCon=0.5 ):
      self.mode = mode
      self.maxHands = maxHands
      self.model_complexity = model_complexity
      self.detectionCon = detectionCon
      self.trackCon = trackCon

      self.mpHands = mp.solutions.hands
      self.hands = self.mpHands.Hands( self.mode, self.maxHands,self.model_complexity, self.detectionCon, self.trackCon)
      self.mpDraw = mp.solutions.drawing_utils
      self.tipIds = [4, 8, 12, 16, 20]

    def FindHands(self, img, draw=True):
        # sending RGB image
      imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      self.results = self.hands.process(imgRGB)
      #print(results.multi_hand_landmarks)

      if self.results.multi_hand_landmarks:
         for handLms in self.results.multi_hand_landmarks:
             if draw:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
      return img

    def FindPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                 cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return  self.lmList

    def FingersUp(self):
        fingers= []
        #Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.FindHands(img)
        lmList = detector.FindPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()


###Which camera is detected###
#def return_camera_indices():
     #index = -2
     #arr = []
     #i = 10
     #while i > 0:
        # cap = cv2.VideoCapture(index)
         #if cap.read()[0]:
             #arr.append(index)
             #cap.release()
         #index += 1
         #i -= 1
     #return arr

#print (return_camera_indices())