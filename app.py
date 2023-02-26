import math
import cv2
import mediapipe as mp
import time
from subprocess import call
from sys import platform

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.mediapipe.python.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils

pTime = 0
cTime = 0

def executeBasedOnOS():
    if platform == "linux" or platform == "linux2":
        if distance_between_thumb_index >= 500:
                call(["amixer set Master 10%+"], shell=True)
        elif distance_between_thumb_index <= 300:
            call(["amixer set Master 10%-"], shell=True)
        #  if the os is MAC
    elif platform == "darwin":
        if distance_between_thumb_index >= 500:
                call(["osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'"], shell=True)
        elif distance_between_thumb_index <= 300:
            call(["osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'"], shell=True)
    elif platform == "win32":
        if distance_between_thumb_index >= 500:
            call(["setvol +10"], shell=True)
        elif distance_between_thumb_index <= 300:
            call(["setvol -10"], shell=True)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            ih, iw, ic = img.shape
            # for id, lm in enumerate(handLms.landmark):
            #     print(id, lm)
            p1 = (int(handLms.landmark[4].x * iw), int(handLms.landmark[4].y * ih))
            p2 = (int(handLms.landmark[8].x * iw), int(handLms.landmark[8].y * ih))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            legA = abs(p1[0] - p2[0])
            legb = abs(p1[1] - p2[1])

            distance_between_thumb_index = int(math.sqrt(legA**2 + legb**2))
            
            cv2.line(img, p1, p2, (250,0,250), 3)
            cv2.circle(img, (int((p1[0] + p2[0])/2), int((p1[1] + p2[1])/2)), 10, (255,0,255), 3)

            cv2.putText(img, f'{distance_between_thumb_index}', (int((p1[0] + p2[0])/2), int((p1[1] + p2[1])/2)), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

            executeBasedOnOS()

    # frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # displaying frame rate
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)