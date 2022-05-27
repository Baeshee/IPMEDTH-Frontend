import cv2 as cv
import mediapipe as mp
import math

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
        self.lmNames = ["WRIST",
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
                        "PINKY_TIP"]
    
    # Function which takes the photo from the main function
    # and extracts all landmarks and hand features and also
    # drawing the landmarks on the image    
    def staticImage(self, img, draw=True, flipType=True):
        
        # Creates the image and extracting the size and
        # converts it to a centrain color mode
        imageRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imageRGB)
        dHands = []
        h, w, c = img.shape
        
        if self.result.multi_hand_landmarks:
            for hType, lMarks in zip(self.result.multi_handedness, self.result.multi_hand_landmarks):
                myHand = {}
                mylmList = []
                
                # Extracting the x, y and z coordinated form the handlandmarks
                # and saving them to a dictionary
                for id, lm in enumerate(lMarks.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append({'name': self.lmNames[id],
                                    'id': id,
                                    'x_value': px,
                                    'y_value': py,
                                    'z_value': pz})

                myHand["lmList"] = mylmList
                myHand["score"] = hType.classification[0].score
                
                # Checks which hand is being identified
                # Note: if there are 2 hands returns both their hTypes
                # for more explicit distinction
                if flipType:
                    if hType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = hType.classification[0].label
                dHands.append(myHand)
                
                # Draws the landmarks on the image
                if draw:
                    self.drawUtils.draw_landmarks(img, lMarks, self.mpHands.HAND_CONNECTIONS, self.drawStyle.get_default_hand_landmarks_style(),
                    self.drawStyle.get_default_hand_connections_style())
                
        # Returning statement
        if draw:
            return dHands, img
        else:
            return dHands


#def createAnnotedImage(self):    
#         sender = self.sender()
#         side = ""
        
#         if(sender.text() == "Rechter zijde"):
#             self.r_cb.setChecked(True)
#             side = "right"
#         if(sender.text() == "Bovenkant"):
#             self.t_cb.setChecked(True)
#             side = "top"
#         if(sender.text() == "Voorkant"):
#             self.f_cb.setChecked(True)
#             side = "front"
#         if(sender.text() == "Linker zijde"):
#             self.l_cb.setChecked(True)
#             side = "left"
        
#         start_time = dt.now()
#         start_date = start_time.strftime("%d-%m-%Y")
#         hands, img = self.detector.staticImage(cv_img)
#         end_time = dt.now()
#         duration = (end_time - start_time).total_seconds()
        
#         # Create a image where the landmarks are stored
#         cv.imwrite(f"images/PY_testpersoon_{self.pn.value()}_{self.ht.currentText().lower()}_{side}_{start_date}.png", img)
        
#         dict = {}
#         hTypes = []
#         hScore = []
#         lmNames = []
#         lmIds = []
#         xList = []
#         yList = []
#         zList = []
        
#         # Extracting all information that are stored in the variables
#         # so they can be saved to a csv and excel for later use
#         if hands:
#             for h in range(0, len(hands)):
#                 for v in range(0, len(hands[0]['lmList'])):
#                     hTypes.append(hands[h]['type'])
#                     hScore.append(hands[h]['score'])
#                     lmNames.append(hands[h]['lmList'][v]['name'])
#                     lmIds.append(hands[h]['lmList'][v]['id'])
#                     xList.append(hands[h]['lmList'][v]['x_value'])
#                     yList.append(hands[h]['lmList'][v]['y_value'])
#                     zList.append(hands[h]['lmList'][v]['z_value'])        
        
#         dict = {'hand_type': hTypes,
#                 'hand_score': hScore,
#                 'landmark_id': lmIds,
#                 'landmark_name': lmNames,
#                 'x_value': xList,
#                 'y_value': yList,
#                 'z_value': zList,
#                 'total_run_time': duration,
#                 'test_date': dt.now().strftime("%d-%m-%Y"),
#                 'test_time': dt.now().strftime("%H:%M:%S"),
#                 'annoted_image': f"PY_testpersoon_{self.pn.value()}_{self.ht.currentText().lower()}_{side}_{start_date}.png"}
        
#         # Check if there is a csv and a xslx file otherwise
#         # create a new dataframe and save all the values to the
#         # dataframe so they can be saved
        
#         df = pd.DataFrame(dict)
#         df.to_csv(f'results/PY_testpersoon_{self.pn.value()}_{self.ht.currentText().lower()}_{side}_{start_date}.csv', encoding='utf-8', index=False)       