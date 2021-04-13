import os

import cv2
import mediapipe as mp
import math

mHands = mp.solutions.hands
hands = mHands.Hands()

mDraw = mp.solutions.drawing_utils

def main():
    vid = cv2.VideoCapture(0)

    volumeMute = False

    while True:
        state, frame = vid.read()
        if state:

            '''
            Convert capture image to RGB as mediapipe processes RGB images
            '''
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            '''
            Check for available hands detected
            '''
            if results.multi_hand_landmarks:
                '''
                For each hand detected get x and y coordinate to find distance between two fingures
                i.e with id 4 and 8
                '''
                for landHand in results.multi_hand_landmarks:
                    x1, y1 = 0, 0
                    x2, y2 = 0, 0
                    for id, lm in enumerate(landHand.landmark):
                        hh, ww, zz = frame.shape

                        # Convert from floating point numbers to numbers with range 0 - 255
                        x, y = int(lm.x * ww), int(lm.y * hh)
                        if id == 8:
                            cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)
                            x1, y1 = x, y
                        elif id == 4:
                            cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)
                            x2, y2 = x, y

                    # d is the distance between to fingures, if less than 25 then mute || unmute
                    # computer volume
                    d = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                    print('Distance is', d)
                    if d < 25:
                        if volumeMute:
                            os.system('pactl set-sink-mute 1 no')
                            volumeMute = False
                        else:
                            os.system('pactl set-sink-mute 1 yes')
                            volumeMute = True

                    # Draw hand landmarks to the image
                    mDraw.draw_landmarks(frame, landHand, mHands.HAND_CONNECTIONS)

            cv2.imshow("Hand Tracking", frame)
            cv2.waitKey(1)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
