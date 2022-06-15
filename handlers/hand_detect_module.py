import cv2 as cv
import mediapipe as mp
import math
import numpy as np

import json
from itertools import islice


class handDetect:
    def __init__(self, mode=False, maxHands=1, detectCon=0.8, trackCon=0.8):
        self.drawUtils = mp.solutions.drawing_utils
        self.drawStyle = mp.solutions.drawing_styles

        self.mode = mode
        self.maxHands = maxHands
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectCon,
            min_tracking_confidence=self.trackCon,
        )

        self.lmList = []
        self.lmNames = [
            "WRIST",
            "THUMB_CMC",
            "THUMB_MCP",
            "THUMB_IP",
            "THUMB_TIP",
            "INDEX_FINGER_MCP",
            "INDEX_FINGER_PIP",
            "INDEX_FINGER_DIP",
            "INDEX_FINGER_TIP",
            "MIDDLE_FINGER_MCP",
            "MIDDLE_FINGER_PIP",
            "MIDDLE_FINGER_DIP",
            "MIDDLE_FINGER_TIP",
            "RING_FINGER_MCP",
            "RING_FINGER_PIP",
            "RING_FINGER_DIP",
            "RING_FINGER_TIP",
            "PINKY_MCP",
            "PINKY_PIP",
            "PINKY_DIP",
            "PINKY_TIP",
        ]

    # Function which takes the photo from the main function
    # and extracts all landmarks and hand features and also
    # drawing the landmarks on the image
    def staticImage(self, img, draw=True, flipType=True):

        # Creates the image and extracting the size and
        # converts it to a centrain color mode
        imageRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imageRGB)
        dHands = {}
        h, w, c = img.shape

        x_max = 0
        y_max = 0
        x_min = w
        y_min = h
        padding = 30

        if self.result.multi_hand_landmarks:
            for hType, lMarks in zip(
                self.result.multi_handedness, self.result.multi_hand_landmarks
            ):
                fingers = [
                    "finger_index",
                    "finger_middle",
                    "finger_ring",
                    "finger_pink",
                    "finger_thumb",
                    "wrist",
                ]
                lmrks_loc = []

                # Checks which hand is being identified
                # Note: if there are 2 hands returns both their hTypes
                # for more explicit distinction
                if flipType:
                    if hType.classification[0].label.lower() == "right":
                        dHands["hand_type"] = "left"
                    else:
                        dHands["hand_type"] = "right"
                else:
                    dHands["hand_type"] = hType.classification[0].label.lower()

                dHands["hand_score"] = hType.classification[0].score

                # Extracting the x, y and z coordinated form the handlandmarks
                # and saving them to a dictionary
                for id, lm in enumerate(lMarks.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    lmrks_loc.append({"x": px, "y": py})

                    if px > x_max:
                        x_max = px
                    if px < x_min:
                        x_min = px
                    if py > y_max:
                        y_max = py
                    if py < y_min:
                        y_min = py

                lmrks = dict(zip(self.lmNames, lmrks_loc))

                items = sorted(lmrks.items())
                rst = [dict(items[i : i + 4]) for i in range(0, len(items), 4)]
                data = dict(zip(fingers, rst))
                dHands["landmarks"] = data

                # Draws the landmarks on the image
                if draw:
                    self.drawUtils.draw_landmarks(
                        img,
                        lMarks,
                        self.mpHands.HAND_CONNECTIONS,
                        self.drawStyle.get_default_hand_landmarks_style(),
                        self.drawStyle.get_default_hand_connections_style(),
                    )

                # Resizes the image to only return a bounding box fitted result
                img_save = img[
                    (y_min - padding) : (y_max + padding),
                    (x_min - padding) : (x_max + padding),
                ]
        # Returning statement
        if draw:
            return dHands, img
        else:
            return dHands
