import cv2 as cv
import mediapipe as mp
import math

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
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectCon,
                                        min_tracking_confidence=self.trackCon)
        
        self.lmList = []
        self.lmNames = ["THUMB_CMC",
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
                        "WRIST"]
    
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
        
        if self.result.multi_hand_landmarks:
            for hType, lMarks in zip(self.result.multi_handedness, self.result.multi_hand_landmarks):
                fingers = ["finger_index", "finger_middle", "finger_ring", "finger_pink", "finger_thumb", "wrist"]
                lmrks_loc = []
                
                x_max = 0
                y_max = 0
                x_min = w
                y_min = h
                padding = 30
                
                
                # Checks which hand is being identified
                # Note: if there are 2 hands returns both their hTypes
                # for more explicit distinction
                if flipType:
                    if hType.classification[0].label == "Right":
                        dHands["hand_type"] = "Left"
                    else:
                        dHands["hand_type"] = "Right"
                else:
                    dHands["hand_type"] = hType.classification[0].label
                    
                dHands["hand_score"] = hType.classification[0].score
                
                # Extracting the x, y and z coordinated form the handlandmarks
                # and saving them to a dictionary
                for id, lm in enumerate(lMarks.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    lmrks_loc.append({'x': px, 'y': py, 'z': pz})
                    lmrks = dict(zip(self.lmNames, lmrks_loc))             
                    
                    if px > x_max:
                        x_max = px
                    if px < x_min:
                        x_min = px
                    if py > y_max:
                        y_max = py
                    if py < y_min:
                        y_min = py
                
                
                items = sorted(lmrks.items())
                rst = [dict(items[i:i+4]) for i in range(0, len(items), 4)]
                data = dict(zip(fingers, rst))
                dHands["landmarks"] = data
                
                # Draws the landmarks on the image
                if draw:
                    self.drawUtils.draw_landmarks(img, lMarks, self.mpHands.HAND_CONNECTIONS, self.drawStyle.DrawingSpec(color=(0,255,0)),
                    self.drawStyle.DrawingSpec(color=(255,255,255)))
                
                # Resizes the image to only return a bounding box fitted result
                # img = img[(y_min - padding):(y_max + padding), (x_min - padding):(x_max + padding)]
        # Returning statement
        if draw:
            return dHands, img
        else:
            return dHands
        