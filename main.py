import os

import cv2
import numpy as np
import mediapipe as mp
import math
from multiprocessing import Process

mHands = mp.solutions.hands
hands = mHands.Hands()

mDraw = mp.solutions.drawing_utils


def play():
    os.system('vlc vid.mp4')


def main():
    vid = cv2.VideoCapture(0)

    volumeMute = False

    while True:
        state, frame = vid.read()
        if state:

            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            if results.multi_hand_landmarks:
                for landHand in results.multi_hand_landmarks:
                    x1, y1 = 0, 0
                    x2, y2 = 0, 0
                    for id, lm in enumerate(landHand.landmark):
                        hh, ww, zz = frame.shape
                        x, y = int(lm.x * ww), int(lm.y * hh)
                        if id == 8:
                            cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)
                            x1, y1 = x, y
                        elif id == 4:
                            cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)
                            x2, y2 = x, y

                    d = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                    print('Distance is', d)
                    if d < 25:
                        if volumeMute:
                            os.system('pactl set-sink-mute 1 no')
                            volumeMute = False
                        else:
                            os.system('pactl set-sink-mute 1 yes')
                            volumeMute = True

                    mDraw.draw_landmarks(frame, landHand, mHands.HAND_CONNECTIONS)

            cv2.imshow("Hand Tracking", frame)
            cv2.waitKey(1)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
